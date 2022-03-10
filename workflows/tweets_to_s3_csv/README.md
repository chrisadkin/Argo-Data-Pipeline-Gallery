# Overview

Am argo workflow manifest for implementing a simple single task data pipeline.

# Build Instructions

1. Create three Kubernetes secrets for the twitter API bearer token, AWS access key id and aws access key secret, substitute the place holders between the angular brackets for actual values:

```
kubectl create secret generic bearer-token --from-literal=bearertoken=<insert_your_bearer_token_value_here>
kubectl create secret generic aws-access-key-id --from-literal=awsaccesskeyid=<insert_your_aws_access_key_id_here>
kubectl create secret generic aws-access-key-secret --from-literal=awsaccesskeyid=<insert_your_aws_access_key_secret_here>
```

2. 



