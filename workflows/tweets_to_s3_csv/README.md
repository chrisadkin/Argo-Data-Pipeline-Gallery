# Overview

Am argo workflow manifest for implementing a simple single task data pipeline.

# Build Instructions

1. Create three Kubernetes secrets for the twitter API bearer token, AWS access key id and aws access key secret, substitute the place holders between the angular brackets for actual values:

```
kubectl create secret generic bearer-token --from-literal=bearertoken=<insert_your_bearer_token_value_here>
kubectl create secret generic aws-access-key-id --from-literal=awsaccesskeyid=<insert_your_aws_access_key_id_here>
kubectl create secret generic aws-access-key-secret --from-literal=awsaccesskeyid=<insert_your_aws_access_key_secret_here>
```

2. Replace the docker image name place holder with the actual name of the image to be used:

```
- name: tweets-to-s3-csv
    container:
      image: {{ docker image name }}
```

3. Replace the place holder values in the workflow.yaml file with actual values:

```
      - name: ENDPOINT_URL
        value: "http://{{ IP address }}"
      - name: BUCKET
        value: "{{ S3 bucket name }}"
      - name: TWITTER_QUERY
        value: "{{ twitter query }}"
      - name: MAX_TABLE_SIZE
        value: "{{ twitter API batch size }}"
```

4. Deploy the workflow manifest to your Kubernetes cluster:
```
kubectl create -f < path to workflow YAML manifest file > -n < Kubernetes namespace >
```

5. Open the argo GUI to verify that workflow has executed without any issues:


6. Inspect your S3 buckets for tweet CSV files, there is a variety of tools for doing this, this screenshot comes from Cyber Duck

