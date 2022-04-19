# Overview

Am argo workflow manifest for implementing a two stage data pipeline, that:

- Stores sentiment scored tweets in an S3 bucket in csv file form
- Loads the csv files from the S3 buckets into a Cassandra table

# Prerequisites

- An S3 compatible storage platform, to date this pipeline has been tested with Pure Storage's FlashBlade appliance.
- A bearer token for the twitter's Tweepy V2 API, this is obtained via a twitter developer account.
- Argo Workflows deployed to a Kubernetes cluster, follow [this guide](https://argoproj.github.io/argo-workflows/quick-start/)
  for the most expediant way of deploying Argo Workflows.
- The [Argo Workflows CLI](https://argoproj.github.io/argo-workflows/cli/)
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

1. Create three Kubernetes secrets for the twitter API bearer token, AWS access key id and aws access key secret, substitute the place holders
   between the angular brackets for actual values:

```
kubectl create secret generic bearer-token --from-literal=bearertoken=<insert_your_bearer_token_value_here> -n <Kubernetes_namespace>
kubectl create secret generic aws-access-key-id --from-literal=awsaccesskeyid=<insert_your_aws_access_key_id_here> -n <Kubernetes_namespace>
kubectl create secret generic aws-access-key-secret --from-literal=awsaccesskeyid=<insert_your_aws_access_key_secret_here> -n <Kubernetes_namespace>
kubectl create secret generic cassandra-username --from-literal=<insert_your_cassandra_username> -n <Kubernetes_namespace>
kubectl create secret generic cassandra-password --from-literal=cassandrapassword=<insert_your_cassandra_password> -n <Kubernetes_namespace>
```

2. Create a parameters.yaml file as follows, replace the placeholders in the excerpt below with the values intended for use by the data pipeline:

```
tweets_to_S3_csv_image: "< image name >" 
S3_endpoint_URL: "< URL >"
S3_bucket: "< bucket name >"
twitter_query: "< twitter query >"
max_table_size: "< max table size, the value 10 is a good default >"
S3_csv_to_cassandra_image: "< image name >"
cassandra_host: "< cassandra host >"
keyspace: "< keyspace name >"
```

3. Deploy the workflow manifest to your Kubernetes cluster:
```
argo submit < path to workflow.yaml file > -n < Kubernetes namespace > --parameter-file < path to parameters.yaml file >
```
