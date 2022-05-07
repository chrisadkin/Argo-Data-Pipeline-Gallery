# Overview

Files for building a docker image to load sentiment scored tweets stored as csv files in an S3 bucket into a table in a PostgreSQL database.

# Build Instructions

```
docker built . -t <tag name>
```

# Environment Variables

The bash script used by the docker container image relies on the following environment variables being set:

| Name                     | Description                                        | Notes                                                       |
| ------------------------ | -------------------------------------------------- | ----------------------------------------------------------- |
| AWS_ACCESS_KEY_ID        | AWS access key id for accessing the S3 bucket      |                                                             |
| AWS_SECRET_ACCESS_KEY    | AWS secret access key for accessing the S3 bucket  |                                                             |
| ENDPOINT_URL             | The URL endpoint for the S3 object store           | For AWS use: http://s3.REGION_GOES_HERE.amazonaws.com       |   
| BUCKET                   | S3 bucket containing csv files to load             |                                                             |
| POSTGRESQL_USER          | Username for connecting to the instance with       |                                                             |
| POSTGRESQL_PASSW         | Password for connecting to the instance with       |                                                             |
| POSTGRESQL_HOST          | Name or IP address of the PostgreSQL host          |                                                             |
| POSTGRESQL_PORT          | Port for connecting to the PostgreSQL instance with| The default of 9042 works in most cases                     |
| DATABASE                 | Database to create the tweet table in              | This must be created prior to executing the container       |
| TABLE                    | Name of tweet table to create                      |                                                             | 

# Executing the Code In Container Form

```
docker run <tag name> -e AWS_ACCESS_KEY_ID="<Access key for bucket containing CSV files>" \
                      -e AWS_SECRET_ACCESS_KEY="<Secret access key for bucket containing CSV files>" \
                      -e ENDPOINT_URL="<endpoint URL>" \
                      -e BUCKET="<S3 bucket name>" \
                      -e POSTGRESQL_USER="<Username>" \
                      -e POSTGRESQL_PASSW="<Password>" \
                      -e POSTGRESSQL_HOST="<PostgreSQL host / IP address>" \
                      -e POSTGRESQL_PORT="<PostgreSQL port>" \
                      -e DATABASE="<Database name>" \
                      -e TABLE="<Table name>"
```

# Executing the Code In Native Bash Script Form

```
export AWS_ACCESS_KEY_ID="<Access key for bucket containing CSV files>"
export AWS_SECRET_ACCESS_KEY="<Secret access key for bucket containing CSV files>"  
export ENDPOINT_URL="<endpoint URL>"
export BUCKET="<S3 bucket name>"
export POSTGRESQL_USER="<Username>"
export POSTGRESQL_PASSW="<Password>"
export POSTGRESSQL_HOST="<PostgreSQL host / IP address>"
export POSTGRESQL_PORT="<PostgreSQL port>"
export DATABASE="<Database name>"
export TABLE="<Table name>"

python3 s3_csv_to_postgresql.py 
```
