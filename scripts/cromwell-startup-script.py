import requests, subprocess

# NOTE - Intended for Google's Debian Stretch image
# NOTE - The current wrapper assumes you have at least 25G of RAM (e.g. n1-highmem-4)
# NOTE - This script reads from a bucket. Make sure permissions are set for the VMs service account to allow this.
# NOTE - Cromwell needs to write to a bucket, make sure scopes on the VM are set appropriately
# EXAMPLE (TODO - scopes may be too broad)
# gcloud compute instances create cromwell \
#    --image-project=debian-cloud
#    --image-family=debian-9
#     --metadata-from-file startup-script=startup.sh
#     --metadata cromwell-version=34,cromwell-config=gs://some/gcs/path/to/config,mysql-cromwell-password-file=gs://some_bucket/password.txt \
#     --scopes https://www.googleapis.com/auth/cloud-platform

# Do this from instance metadata
# Make sure to set on instance start up
VERSION=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/cromwell-version -H "Metadata-Flavor: Google")

# Note also that we still need configuration file.
# This should be a bucket URL readable by the service account running this instance
CONFIG=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/cromwell-config -H "Metadata-Flavor: Google")

DB_NAME=$(curl http://metadata.google.internal/computeMetadata/v1/instance/attributes/mysql-database-name -H "Metadata-Flavor: Google")

INSTALL_DIR="/opt/ccdg/cromwell-${VERSION}"
BIN_DIR="${INSTALL_DIR}/bin"
JAR_DIR="${INSTALL_DIR}/jar"
CONFIG_DIR="${INSTALL_DIR}/config"
LCONFIG="${CONFIG_DIR}/jes.conf"

def install_packages():

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

#-- install_packages

def install_cromwell():
    #curl -OL https://github.com/broadinstitute/cromwell/releases/download/${VERSION}/cromwell-${VERSION}.jar && mv cromwell-${VERSION}.jar ${JAR_DIR}/
    #curl -OL https://github.com/broadinstitute/cromwell/releases/download/${VERSION}/womtool-${VERSION}.jar && mv womtool-${VERSION}.jar ${JAR_DIR}/
    if not os.path.exists(JAR_DIR):
        os.makedirs(JAR_DIR)
    os.chdir(JAR_DIR)

    for name in "cromwell", "womtool":
        jar_basename = name + "-" + VERSION + "." + "jar"
        if os.path.exists( os.path.join(JAR_DIR, jar_basename) ):
            print "{} already installed...SKIPPING".format(jar_basename)
            continue
        url = "/".join(["https://github.com/broadinstitute/cromwell/releases/download", VERSION, jar_basename])
        print "Intalling {} from {}".format(jar_basename, url)
        result = requests.get(url)
        if not response.ok: raise Exception("Failed to get {} from URL: {}".format(jar_basename, url))
        with open(jar_basename, "wb") as f:
            f.write(r.content)

    print "Install cromwell...DONE"

#-- install_cromwell

gsutil cp ${CONFIG} ${LCONFIG}
perl -p -i -e "s/cromwell-mysql:3306/${DB_NAME}:3306/g" ${LCONFIG}

# Cromwell server start-up wrapper
# Assumes that you have at least 25G RAM available
cat > ${BIN_DIR}/cromwell-server <<SCRIPT
#!/bin/bash


MYSQL=PW LOG_MODE=standard java -Xmx40000M -Dconfig.file=${LCONFIG} -jar ${JAR_DIR}/cromwell-${VERSION}.jar server 2>&1
SCRIPT
chmod a+x ${BIN_DIR}/cromwell-server


# Include cromwell wrapper in global path for all users
cat > /etc/profile.d/cromwell.sh <<PATHSETTER
#!/bin/bash

PATH=${BIN_DIR}:\$PATH
PATHSETTER

# verify things
# This will end up in /var/log/syslog or /var/log/daemon.log
java -version
java -jar ${JAR_DIR}/cromwell-${VERSION}.jar

if __name__ == '__main__':
    install_packages()
    install_cromwell()
    print "Startup script...DONE"
#-- __main__
