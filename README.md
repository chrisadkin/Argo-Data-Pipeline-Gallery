# Overview

This repo contains a number of Docker images that can be incorporated into an Argo workflows based data pipelines to showcase:

- Portworx data services
- SQL Server 2022 S3 object virtualization

# High Level Build Instructions

- The README file for each workflow contains instructions for deploying the workflow
- Each subdirectory under the [docker_images](https://github.com/chrisadkin/Argo-Data-Pipeline-Gallery/tree/main/docker_images) folder contains the files neccessary for building the images used by each workflow

# Available Images

[tweets_to_s3_csv](https://github.com/chrisadkin/Argo-Data-Pipeline-Gallery/blob/main/docker_images/tweets_to_s3_csv/README.md)

leverages the Tweepy API via Python in order to extract tweets, sentiment score the tweets and store them in csv file form in an S3 bucket.

[s3_csv_to_cassandra](https://github.com/chrisadkin/Argo-Data-Pipeline-Gallery/tree/main/docker_images/s3_csv_to_cassandra)

Loads csv files containing sentiment scored tweets into a table in a Cassandra keyspace.

[s3_csv_to_postgresql](https://github.com/chrisadkin/Argo-Data-Pipeline-Gallery/tree/main/docker_images/s3_csv_to_postgresql)

Loads csv files containing sentiment scored tweets into a table in a PostgreSQL database.

# Available Workflows

[tweets_to_s3_csv](https://github.com/chrisadkin/Argo-Data-Pipeline-Gallery/tree/main/workflows/tweets_s3_to_cassandra)
Argo workflow manifest that loads sentiment scored tweets into Cassandra via an S3 bucket.
