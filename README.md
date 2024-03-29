# Cromwell Deployment

This repository contains scripts and resources to deploy a [cromwell][0] server and database. Currently implemented for Google Cloud.

[0]: https://github.com/broadinstitute/cromwell
[1]: https://cloud.google.com

## Google Cloud Service Account

A service account is required to run cromwell infrastructure. It is recommended to use a custom one for running these services instead of using the "default" one. The service account will need these roles assigned to it:

* Cloud SQL Admin
  * Full control of Cloud SQL resources.
* Service Usage Consumer
  * Ability to inspect service states and operations, and consume quota and billing for a consumer project.

## Edit `cromwell.yaml`

Update these properties need to be set in the YAML (`resources/google-deployments/cromwell.yaml`) configuration. Check `cromwell.jinja.schema` for additional properties documentation.

### Required Properties

| Property | Notes |
| --- | --- |
| service_account | service account email (or "default") to have authorized on the cromwell VM |
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

## Edit the _PAPI.v2.conf_ [OPTIONAL]

Optionally, edit the `resources/cromwell-configs/PAPI.v2.conf` file to adjust the any of the cromwell server configuration. Do not edit the *DB* section, as it is populated with the Cloud SQL IP and root user password.

## Enable required APIs
Prior to running the deployment, set up billing for your project and enable the required APIs by following this link and selecting the desired project.

Make sure that billing is enabled for your Google Cloud Platform project. [Learn how to enable billing](https://cloud.google.com/billing/docs/how-to/modify-project).

If this is the first time running this in the project, be sure to [enable the following APIs: Genomics API, Compute Engine API, Google Cloud Storage JSON API, Cloud SQL Admin API, Cloud Deployment Manager V2 API](https://console.cloud.google.com/flows/enableapi?apiid=genomics,compute,storage_api,sqladmin,deploymentmanager)

## Create the Deployment

In an authenticated Google Cloud session, enter the `resources/google-deployments` directory. Run the command below to create the deployment named _cromwell1_. The deployemnt name will be prepended to all assoiciated assets.

```
$ gcloud deployment-manager deployments create cromwell1 --config cromwell.yaml
The fingerprint of the deployment is nBuQdHhB0JYSE85Y0hkzjQ==
Waiting for create [operation-1558469542478-5896b777900d3-3b747d21-13cf4243]...done.                              
Create operation operation-1558469542478-5896b777900d3-3b747d21-13cf4243 completed successfully.
NAME                          TYPE                       STATE      ERRORS  INTENT
cromwell1-cloudsql            sqladmin.v1beta4.instance  COMPLETED  []
cromwell1-cromwell            compute.v1.instance        COMPLETED  []
cromwell1-static-ip           compute.v1.address         COMPLETED  []
cromwell1-net                 compute.v1.network         COMPLETED  []
cromwell1-net-ssh-restricted  compute.v1.firewall        COMPLETED  []
cromwell1-subnet              compute.v1.subnetwork      COMPLETED  []
```

### Assests Created

This is list of assets created in the deployment. All assests are preppended with the deployment name and a '-'.

| Assest | Name | Purpose |
| --- | --- | --- |
| static IP | *-static-ip* | An IP for the crowmell server to only allow DB connections to the cloud SQL instance. |
| cromwell server VM | *-cromwell* | The cromwell server. Start workflows, and querythe SQL DB from here. |
| cloud sql | *-cloudsql* | SQL database VM adn Server. |
| network | *network* | network for instances and firewalls |
| subnet | *subnetwork* |subnet for the network|
| firewall | *firewall* |restrict access to the network|

## Verify the `cromwell` deployment

### SSH into the server VM.

In the default parameter case it is: `cromwell1-cromwell`.

```
$ gcloud ssh cromwell1-cromwell
```

### Verify the server is running

```
you@cromwell1-cromwell:~$ ps aux | grep java
root     14565 45.1  1.8 32349732 583008 ?     Ssl  20:16   0:29 /usr/bin/java -Xmx25000M -Dconfig.file=/opt/cromwell-39/config/PAPI.v2.conf -jar /opt/cromwell-39/jar/cromwell-39.jar server
you@cromwell1-cromwell:~$ curl 'http://localhost:8000/engine/v1/version' && echo
{"cromwell":"39"}
```
### Check the cromwell service logs

```
journalctl -u cromwell
```
### Optionally, edit the config and resatart the cromwell service

```
sudo vim /opt/cromwell*/config/PAPI.v2.conf
sudo service cromwell restart
```
# Delete a Deployment

```sh
$ gcloud deployment-manager deployments delete cromwell1
```
# Services

## Cromwell
Location: /etc/systemd/system/cromwell.service
The cromwell server is set up to run as a service on the cromwell VM. Some helpful commands are below, use them on the cromwell VM.
* Check the sevice
```
$ sudo systemctl is-active cromwell
active
```
* View logs
```
$ journalctl -u cromwell
```
* View logs as `tail -f`
```
$ journalctl -u cromwell -f
```
* Restart the service
```
$ sudo systemctl restart cromwell
```
## MySQL
MySQL service is setup as Google "Cloud SQL" instance. For security purposes, it configured to only accept connections from the cromwell server. The host and password are located in the jdbc url in `/opt/cromwell-39/config/PAPI.v2.conf`. 
```
# Log into the cromwell instance
$ gcloud compute ssh cromwell1-cromwell

# Grab the SQL IP from the PAPI.v2.conf
$ MYSQL_IP=$(grep jdbc:mysql /opt/cromwell/config/PAPI.v2.conf | awk -F/ '{print $3}' | awk -F: '{print $1}')
$ echo $MYSQL_IP
1.2.3.4

# Show the mysql password
$ grep password /opt/cromwell/config/PAPI.v2.conf | awk -F= '{print $2}' | sed 's/\s*//g'
cromwell

# Log into the database
$ mysql -h $MYSQL_IP -u root -D cromwell -p
MySQL [cromwell]> 
```
