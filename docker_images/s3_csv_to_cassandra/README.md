# Overview

Files for building a docker image to load sentiment scored tweets stored as csv files in an S3 bucket into Cassandra.

# Build Instructions

```
docker built . -t <tag name>
```

# Environment Variables

The bash script used by the docker container image relies on the following environment variables being set:

| Name                     | Description                                       | Notes                                                       |
| ------------------------ | ------------------------------------------------- | ----------------------------------------------------------- |
| AWS_ACCESS_KEY_ID        | AWS access key id for accessing the S3 bucket     |                                                             |
| AWS_SECRET_ACCESS_KEY    | AWS secret access key for accessing the S3 bucket |                                                             |
| ENDPOINT_URL             | The URL endpoint for the S3 object store          | For AWS use: http://s3.REGION_GOES_HERE.amazonaws.com       |   
| BUCKET                   | S3 bucket containing csv files to load            |                                                             |
| CASSANDR_USER            | Username for connecting to cluster with           |                                                             |
| CASSANDRA_PASSW          | Password for connecting to cluster with           |                                                             |
| CASSANDRA_IP             | Cassandra host IP address                         |                                                             |
| CASSANDRA_PORT           | Cassandra host port                               | The default of 9042 works in most cases                     |
| KEYSPACE                 | Keyspace to create for tweet table                |                                                             | 
| TABLE                    | Name of tweet table to create                     |                                                             | 

# Executing the Code In Container Form

```
docker run <tag name> -e AWS_ACCESS_KEY_ID="<Access key for bucket containing CSV files>" \
                      -e AWS_SECRET_ACCESS_KEY="<Secret access key for bucket containing CSV files>" \
                      -e ENDPOINT_URL="<endpoint URL>" \
                      -e BUCKET="<S3 bucket name>" \
                      -e CASSANDRA_USER="<Username>" \
                      -e CASSANDRA_PASSW="<Password>" \
                      -e CASSANDRA_IP="<Cassandra host IP address>" \
                      -e CASSANDRA_PORT="<Cassandra host port>" \
                      -e KEYSPACE="<Keyspace name>" \
                      -e TABLE="<Table name>"
```

# Executing the Code In Native Bash Script Form

```
export AWS_ACCESS_KEY_ID="<Access key for bucket containing CSV files>"
export AWS_SECRET_ACCESS_KEY="<Secret access key for bucket containing CSV files>"  
export ENDPOINT_URL="<endpoint URL>"
export BUCKET="<S3 bucket name>"
export CASSANDRA_USER="<Username>"
export CASSANDRA_PASSW="<Password>"
export CASSANDRA_IP="<Cassandra host IP address>"
export CASSANDRA_PORT="<Cassandra host port>"
export KEYSPACE="<Keyspace name>"
export TABLE="<Table name>"

python3 s3_csv_to_cassandra.py 
```
