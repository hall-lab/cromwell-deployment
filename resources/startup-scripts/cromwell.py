#!/usr/bin/env python

import os, requests, subprocess, sys

CROMWELL_CLOUDSQL_PASSWORD='@CROMWELL_CLOUDSQL_PASSWORD@'
CROMWELL_VERSION='@CROMWELL_VERSION@'
INSTALL_DIR = os.path.join(os.path.sep, 'opt', 'ccdg', 'cromwell-' + CROMWELL_VERSION)
BIN_DIR = os.path.join(INSTALL_DIR, "bin")
JAR_DIR = os.path.join(INSTALL_DIR, "jar")
CONFIG_DIR = os.path.join(INSTALL_DIR, "config")
GOOGLE_URL = "http://metadata.google.internal/computeMetadata/v1/instance/attributes"

def create_directories():
    print("Create directories...")
    if not os.path.exists(INSTALL_DIR): os.makedirs(INSTALL_DIR)
    if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)
    if not os.path.exists(JAR_DIR): os.makedirs(JAR_DIR)
    if not os.path.exists(CONFIG_DIR): os.makedirs(CONFIG_DIR)

def install_packages():
    print("Install pacakges...")

    packages = [
        'curl',
        'default-jdk',
        'default-mysql-client-core',
        'python-pip',
        'less',
        'vim',
        ]

    while subprocess.call(['apt-get', 'update']):
        print("Failed to apt-get update. Trying again in 5 seconds")
        time.sleep(5)

    while subprocess.call(['apt-get', 'install', '-y'] + packages):
        print("Failed to install packages with apt-get install. Trying again in 5 seconds")
        time.sleep(5)

    subprocess.check_call(['pip', 'install', 'jinja2'])

    print("Install pacakges...DONE")

#-- install_packages

def install_cromwell():
    #curl -OL https://github.com/broadinstitute/cromwell/releases/download/${VERSION}/cromwell-${VERSION}.jar && mv cromwell-${VERSION}.jar ${JAR_DIR}/
    #curl -OL https://github.com/broadinstitute/cromwell/releases/download/${VERSION}/womtool-${VERSION}.jar && mv womtool-${VERSION}.jar ${JAR_DIR}/
    print("Install cromwell...")
    os.chdir(JAR_DIR)
    for name in "cromwell", "womtool":
        jar_basename = name + "-" + CROMWELL_VERSION + "." + "jar"
        jar_fn = os.path.join(JAR_DIR, jar_basename)
        if os.path.exists(jar_fn):
            print("{} already installed...SKIPPING".format(jar_basename))
            continue
        url = "/".join(["https://github.com/broadinstitute/cromwell/releases/download", CROMWELL_VERSION, jar_basename])
        print("Intalling {} from {}".format(jar_basename, url))
        response = requests.get(url)
        if not response.ok: raise Exception("GET failed for {}".format(url))
        with open(jar_fn, "wb") as f:
            f.write(response.content)

    print("Install cromwell...DONE")

#-- install_cromwell

def install_cromwell_config():
    #gsutil cp ${CONFIG} ${LCONFIG}
    #perl -p -i -e "s/cromwell-mysql:3306/${DB_NAME}:3306/g" ${LCONFIG}
    #DB_NAME=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/mysql-database-name -H "Metadata-Flavor: Google")
    fn = os.path.join(CONFIG_DIR, 'PAPI.v2.conf')
    if os.path.exists(fn):
        print("Already installed cromwell profile.d config...SKIPPING")
    sys.stderr.write("Install cromwell PAPI v2 config...")
    from jinja2 import Template
    papi_template = Template( _fetch_instance_info(name='papi-v2-conf') )
    ip = _fetch_instance_info(name='cloudsql-ip')
    params = { "ip": ip, "password": CROMWELL_CLOUDSQL_PASSWORD }
    with open(fn, 'w') as f:
        f.write( papi_template.render(cloudsql=params) )

#-- install_cromwell_config

def add_cromwell_profile():
    fn = os.path.join(os.path.sep, 'etc', 'profile.d', 'cromwell.sh')
    print("Installing supernova profile.d script to {}".format(fn))
    if os.path.exists(fn):
        print("Already installed cromwell profile.d config...SKIPPING")
        return

    with open(fn, "w") as f:
        f.write('PATH={}:"${{PATH}}"'.format(BIN_DIR) + "\n")

#-- add_cromwell_profile

def add_and_start_cromwell_service():
    _fetch_and_save_instance_info(name='cromwell-service', fn=os.path.join(os.path.sep, 'etc', 'systemd', 'system', 'cromwell.service'))
    print("Start cromwell service...")
    subprocess.check_call(['systemctl', 'daemon-reload'])
    subprocess.check_call(['systemctl', 'start', 'cromwell'])

#-- add_cromwell_service

def _fetch_and_save_instance_info(name, fn):
    if os.path.exists(fn):
        print("Already installed {} to {} ... SKIPPING".format(name, fn))
        return
    print("Install {} ...".format(fn))
    content = _fetch_instance_info(name)
    with open(fn, 'w') as f:
        f.write(content)

#-- _fetch_and_save_instance_info

def _fetch_instance_info(name):
    url = "/".join([GOOGLE_URL, name])
    response = requests.get(url, headers={'Metadata-Flavor': 'Google'})
    if not response.ok: raise Exception("GET failed for {}".format(url))
    return response.content

#-- _fetch_instance_info

def configure_cromwell_database():
    sys.stderr.write("Configure cromwell database...\n")

    cloudsql_name = _fetch_instance_info('cloudsql-name')
    sys.stderr.write("Updating root password...\n")
    rv = subprocess.call(["gcloud", "sql", "users", "set-password", "root", "--instance", cloudsql_name, "--password", CROMWELL_CLOUDSQL_PASSWORD, "--host", "%"])
    if rv != 0: raise Exception("Failed to update mysql root user password!")

    cloudsql_ip = _fetch_instance_info('cloudsql-ip')
    sys.stderr.write("Creating cromwell database...\n")
    lenv = os.environ.copy()
    lenv['MYSQL_PWD'] = CROMWELL_CLOUDSQL_PASSWORD
    rv = subprocess.call(['mysql', '-h', cloudsql_ip, '-u', 'root', '-e', 'CREATE DATABASE IF NOT EXISTS cromwell;'], env=lenv)
    if rv != 0: raise Exception("Failed to create the mysql cromwell database")

#-- configure_cromwell_database

if __name__ == '__main__':
    create_directories()
    install_packages()
    install_cromwell()
    install_cromwell_config()
    add_cromwell_profile()
    add_and_start_cromwell_service()
    configure_cromwell_database()
    print("Startup script...DONE")

#-- __main__
