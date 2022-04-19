# Overview

Am argo workflow manifest for implementing a two stage data pipeline, that:

- Stores sentiment scored tweets in an S3 bucket in csv file form
- Loads the csv files from the S3 buckets into a Cassandra table

# Prerequisites

- An S3 compatible storage platform, to date this pipeline has been tested with Pure Storage's FlashBlade appliance.
- A bearer token for the twitter's Tweepy V2 API, this is obtained via a twitter developer account.
- Argo Workflows deployed to a Kubernetes cluster, follow [this guide](https://argoproj.github.io/argo-workflows/quick-start/) for the most expediant way of deploying Argo Workflows.
- A Cassandra Cluster configured for username/password authentication.
- A tweet table, substitute the placeholder in the the brackets with your own Cassandra keyspace:
```
CREATE TABLE {keyspace}.tweet (
   tweet_id   bigint PRIMARY KEY
  ,text_body  text
  ,s_neg      decimal 
  ,s_pos      decimal
  ,s_neu      decimal
  ,s_compound decimal);
```

# Build Instructions

1. Create three Kubernetes secrets for the twitter API bearer token, AWS access key id and aws access key secret, substitute the place holders between the angular brackets for actual values:

```
kubectl create secret generic bearer-token --from-literal=bearertoken=<insert_your_bearer_token_value_here> -n <Kubernetes_namespace>
kubectl create secret generic aws-access-key-id --from-literal=awsaccesskeyid=<insert_your_aws_access_key_id_here> -n <Kubernetes_namespace>
kubectl create secret generic aws-access-key-secret --from-literal=awsaccesskeyid=<insert_your_aws_access_key_secret_here> -n <Kubernetes_namespace>
kubectl create secret generic cassandra-username --from-literal=<insert_your_cassandra_username> -n <Kubernetes_namespace>
kubectl create secret generic cassandra-password --from-literal=cassandrapassword=<insert_your_cassandra_password> -n <Kubernetes_namespace>
```

2. Replace the container image name placeholder with the actual name of the image to be used in the tweets-to-s3-csv template, the files for building the container image can be found in [this](https://github.com/chrisadkin/Argo-Data-Pipeline-Gallery/tree/main/docker_images/s3_csv_to_cassandra) folder:

```
- name: tweets-to-s3-csv
    container:
      image: chrisadkin/tweets_to_s3_csv:1.0
```

3. Replace the placeholder values in the workflow.yaml file with actual values in the tweets-to-s3-csv template:

```
      - name: ENDPOINT_URL
        value: "{S3_endpoint_URL}"
      - name: BUCKET
        value: "{S3_bucket_name}"
      - name: TWITTER_QUERY
        value: "({search_text}) lang:en"
```

4. Replace the container image name placeholder with the actual name of the image to be used in the s3-csv-to-cassandra template, the files for building the container image can be found [here](https://github.com/chrisadkin/Argo-Data-Pipeline-Gallery/tree/main/docker_images/s3_csv_to_cassandra):

```
- name: s3-csv-to-cassandra
    dependencies: [tweets-to-s3-csv]
    container:
      image: chrisadkin/s3_csv_to_cassandra:1.0
```

5. Replace the placeholder values in the workflow.yaml file with actual values in the s3-csv-to-cassandra template:

```
      - name: ENDPOINT_URL
        value: "{S3_endpoint_URL}"
      - name: BUCKET
        value: "{S3_bucket_name}"
      .
      .
      .
      - name: CASSANDRA_HOST
        value: "{cassandra_host}"
      - name: KEYSPACE
        value: "{keyspace_name}"
```

6. Deploy the workflow manifest to your Kubernetes cluster:
```
kubectl create -f < path to workflow YAML manifest file > -n <Kubernetes_namespace>
```
