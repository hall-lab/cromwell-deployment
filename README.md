# Cromwell Deployer (`cromployer`)

This repository contains scripts and resources to deploy a [cromwell][0] server and database. Currently implemented for Google CLoud.

_(Documentation still in progress)_

[0]: https://github.com/broadinstitute/cromwell
[1]: https://cloud.google.com

# Getting Started

    git clone https://github.com/hall-lab/cromwell-deployment
    cd cromwell-deployment

# Setup the Configuration Files

## Edit `cromwell.yaml`

Update these properties need to be set in the YAML (`resources/google-deployments/cromwell.yaml`) configuration. Check `cromwell.jinja.schema` for indivdual properties documentation.

### Required Properties

| Property | Notes |
| --- | --- |
| service_account | service account email to have authorized on the cromwell VM |
| region & zone | area to run instances, should match data location region/zone |
| cromwell_version | cromwell to use |
| cromwell_cloudsql_password | mysql root db password to use | 

### Optional Properties

| Property | Notes (Default) |
| --- | --- |
| cromwell_server_machine_type |  cromwell server VM type (n1-standard-8) |
| cromwell_server_boot_disk_size | cromwesll server VM boot disk size (10 GB) |
| cromwell_cloudsql_instance_type | cloud sql instance type (db-n1-standard-8) |
| cromwell_cloudsql_initial_size | cloud sql disk size (1000 GB) |

## Create the Deployment

In an authenticated Google Cloud session, enter the `resources/google-deployments` directory. Run the command below to create the deployment named _cromwell1_. The deployemnt name will be prepended to all assoiciated assets.

```
$ gcloud deployment-manager deployments create cromwell1 --config cromwell.yaml
The fingerprint of the deployment is nBuQdHhB0JYSE85Y0hkzjQ==
Waiting for create [operation-1558469542478-5896b777900d3-3b747d21-13cf4243]...done.                              
Create operation operation-1558469542478-5896b777900d3-3b747d21-13cf4243 completed successfully.
NAME               TYPE                       STATE      ERRORS  INTENT
cromwell1-cloudsql   sqladmin.v1beta4.instance  COMPLETED  []
cromwell1-cromwell   compute.v1.instance        COMPLETED  []
cromwell1-static-ip  compute.v1.address         COMPLETED  []
```

## Verify the `cromwell` deployment

### SSH into the server VM.

In the default parameter case it is: `cromwell1-cromwell`.

```
$ gcloud ssh cromwell1-cromwell
```

### Verify the server 

```
you@cromwell1-cromwell:~$ ps aux | grep java
root     14565 45.1  1.8 32349732 583008 ?     Ssl  20:16   0:29 /usr/bin/java -Xmx25000M -Dconfig.file=/opt/ccdg/cromwell-39/config/PAPI.v2.conf -jar /opt/ccdg/cromwell-39/jar/cromwell-39.jar server
you@cromwell1-cromwell:~$ curl 'http://localhost:8000/engine/v1/version' && echo
{"cromwell":"39"}
```


# Delete a Deployment

```sh
gcloud deployment-manager delete cromwell1
```

