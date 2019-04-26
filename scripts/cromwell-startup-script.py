import os, requests, subprocess

CROMWELL_VERSION='@CROMWELL_VERSION@'
INSTALL_DIR = os.path.join('opt', 'ccdg', 'cromwell-@CROMWELL_VERSION@')
BIN_DIR = os.path.join(INSTALL_DIR, "bin")
JAR_DIR = os.path.join(INSTALL_DIR, "jar")
CONFIG_DIR = os.path.join(INSTALL_DIR, "config")
PAPI_CONFIG = os.path.join(CONFIG_DIR}, "papi.conf")
GOOGLE_URL = "http://metadata.google.internal/computeMetadata/v1/instance/attributes"

def create_directories():
    print "Create directories..."
    if not os.path.exists(INSTALL_DIR): os.makedirs(INSTALL_DIR)
    if not os.path.exists(BIN_DIR): os.makedirs(BIN_DIR)
    if not os.path.exists(JAR_DIR): os.makedirs(JAR_DIR)
    if not os.path.exists(CONFIG_DIR): os.makedirs(CONFIG_DIR)

def install_packages():
    print "Install pacakges..."

    packages = [
        'curl',
	'default-jdk',
	'default-mysql-client-core',
	'vim',
        ]

    while subprocess.call(['apt-get', 'update']):
        print "Failed to apt-get update. Trying again in 5 seconds"
        time.sleep(5)

    # FIXME needed? apt-get dist-upgrade -y

    while subprocess.call(['apt-get', 'install', '-y'] + packages):
        print "Failed to install packages with apt-get install. Trying again in 5 seconds"
        time.sleep(5)

    print "Install pacakges...DONE"

#-- install_packages

def install_cromwell():
    #curl -OL https://github.com/broadinstitute/cromwell/releases/download/${VERSION}/cromwell-${VERSION}.jar && mv cromwell-${VERSION}.jar ${JAR_DIR}/
    #curl -OL https://github.com/broadinstitute/cromwell/releases/download/${VERSION}/womtool-${VERSION}.jar && mv womtool-${VERSION}.jar ${JAR_DIR}/
    print "Install cromwell..."
    os.chdir(JAR_DIR)
    for name in "cromwell", "womtool":
        jar_basename = name + "-" + CROMWELL_VERSION + "." + "jar"
        if os.path.exists( os.path.join(JAR_DIR, jar_basename) ):
            print "{} already installed...SKIPPING".format(jar_basename)
            continue
        url = "/".join(["https://github.com/broadinstitute/cromwell/releases/download", CROMWELL_VERSION, jar_basename])
        print "Intalling {} from {}".format(jar_basename, url)
        response = requests.get(url)
        if not response.ok: raise Exception("GET failed for {}".format(url))
        with open(jar_basename, "wb") as f:
            f.write(r.content)

    print "Install cromwell...DONE"

#-- install_cromwell

def install_cromwell_config():
    #gsutil cp ${CONFIG} ${LCONFIG}
    #perl -p -i -e "s/cromwell-mysql:3306/${DB_NAME}:3306/g" ${LCONFIG}
    #DB_NAME=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/mysql-database-name -H "Metadata-Flavor: Google")
    papi_conf_path = os.path.join(CONFIG_DIR, 'papi.conf')
    if os.path.exists(papi_conf_path):
        print "Papi/cromwell config already installed at {}".format(papi_conf_path)
        return

    print "Install papi/cromwell config to {}".format(papi_conf_path)
    url = "/".join([GOOGLE_URL, 'papi_conf'])
    response = requests.get(url, headers={'Metadata-Flavor': 'Google'})
    if not response.ok: raise Exception("GET failed for {}".format(url))
    with open(papi_conf_path, 'w') as f:
        f.write(response.content)

#-- install_cromwell_config

def add_cromwell_profile():
    fn = "/etc/profile.d/cromwell.sh"
    print "Installing supernova profile.d script to {}".format(fn)
    if os.path.exists(fn):
        print "Already installed cromwell profile.d config...SKIPPING"
        return

    with open(fn, "w") as f:
        f.write('PATH={}:"${{PATH}}"'.format(BIN_DIR) + "\n")

# verify things
# This will end up in /var/log/syslog or /var/log/daemon.log
#java -version
#java -jar ${JAR_DIR}/cromwell-CROMWELL_VERSION.jar

if __name__ == '__main__':
    create_directories()
    install_packages()
    install_cromwell()
    install_cromwell_config()
    add_cromwell_profile()
    print "Startup script...DONE"
#-- __main__
