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
| ENDPOINT_URL             | The URL endpoint for the S3 object store          | Format is ```http://IP address```                           |        
| BUCKET                   | S3 bucket containing csv files to load            |                                                             |
| CASSANDRA_HOST           | Cassandra host for connecting to the cluster with |                                                             |
| KEYSPACE                 | Cassandra keyspace containing tweet table to load |                                                             | 

# Executing the Code In Container Form

```
docker run <tag name> -env ENDPOINT_URL="http://<IP address>" \
                      -env BUCKET="<S3 bucket name>" \
                      -env CASSANDRA_HOST="<Cassandra host string>" \
                      -env KEYSPACE="<Keyspace name>"
```

# Executing the Code In Native Bash Script Form

```
export ENDPOINT_URL="http://<IP address>"
export BUCKET="<S3 bucket name>"
export CASSANDRA_HOST="<Cassandra host string>"
export KEYSPACE="<Keyspace name>"

./s3_csv_to_cassandra.sh 
```