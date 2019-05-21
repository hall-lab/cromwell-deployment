# Cromwell Deployer (`cromployer`)

This repository contains scripts and resources to deploy a [cromwell][0] server and database. Currently implemented for Google CLoud.

_(Documentation still in progress)_

[0]: https://github.com/broadinstitute/cromwell
[1]: https://cloud.google.com

# Configuring the Cromwell Deployment for Google Cloud

## Edit the Cromwell YAML Configuration File

Update these properties need to be set in the YAML (*resources/google-deployments/cromwell.yaml*) configuration. Check _cromwell.jinja.schema_ for indivdual properties documentation.

### Required Cromwell Properties
| Property | Notes |
| --- | --- |
| service_account | service account email to have authorized on the supernova VM |
| region & zone | area to run instances, should match data location region/zone |
| cromwell_version | cromwell to use |
| cromwell_cloudsql_password | mysql root db password to use | 

### Optional Supernova Properties

FIXME OPTS
| Property | Notes |
| --- | --- |
| cromwell_server_machine_type | |

## Create the Deployment

In an authenticated Google Cloud session, enter the _resources/google-deployments_ directory. Run the command below to create the deployment named _supernova1_. The deployemnt name will be prepended to all assoiciated assets.
```
$ gcloud deploymewnt manager deployments create cromwell1 --config cromwell.yaml
The fingerprint of the deployment is nBuQdHhB0JYSE85Y0hkzjQ==
Waiting for create [operation-1558469542478-5896b777900d3-3b747d21-13cf4243]...done.                              
Create operation operation-1558469542478-5896b777900d3-3b747d21-13cf4243 completed successfully.
NAME               TYPE                       STATE      ERRORS  INTENT
cromwell1-cloudsql   sqladmin.v1beta4.instance  COMPLETED  []
cromwell1-cromwell   compute.v1.instance        COMPLETED  []
cromwell1-static-ip  compute.v1.address         COMPLETED  []
```
## Confirm Deployment and Start a Cromwell Workflow
SSH into the _cromwell1-cromwell_ VM.
```
$ gcloud ssh cromwell1-cromwell
```
FIXME DOC
```
[you@cromwell1-cromwell ~]$ 
```
