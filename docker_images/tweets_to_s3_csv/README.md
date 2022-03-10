# Overview

Files for building a docker image to mine tweets via twitter's Tweepy API, sentiment score the tweets and store them as csv files in an S3 bucket.

# Build Instructions

```
docker built . -t <tag name>
```

# Environment Variables

The python code used by the docker container image relies on the following environment variables being set:

| Name                     | Description                               | Notes                                                              |
| ------------------------ | ----------------------------------------- | ------------------------------------------------------------------ |
| ENDPOINT_URL             | The URL endpoint for the S3 object store  | Format is http://IP_address                                        |        
| BEARER_TOKEN             | Token was accessing the twitter API       | Obtained by signing up for a twitter develeper account from [here](https://developer.twitter.com/en/portal/dashboard) |
| AWS_ACCESS_KEY_ID        | Access key for S3 object store.           |                                                                    |
| AWS_SECRET_ACCESS_KEY_ID | Access key SECRET for S3 object store.    |                                                                    |
| BUCKET                   | S3 bucket to store csv files in           |                                                                    |
| MAX_TABLE_SIZE           | Batch size for extracting tweets from API | A value of 10 is recommended                                       |
| S3_PREFIX                |                                           |                                                                    | 

# Executing the Code In Container Form

```
docker run <tag name> -env ENDPOINT_URL="http://<IP address>" \
                      -env BEARER_TOKEN="<bearer token>" \
                      -env AWS_ACCESS_KEY_ID="<AWS Access Key ID>" \
                      -env AWS_SECRET_ACCESS_KEY="<AWS Secret Access Key>" \
                      -env BUCKET="<S3 bucket name>" \
                      -env TWITTER_QUERY="<Twitter query>" \
                      -env MAX_TABLE_SIZE="<max table size>" \
                      -env S3_PREFIX="<S3 prefix>" 
```

# Executing the Code In Native Python Form

```
export ENDPOINT_URL="http://<IP address>"
export BEARER_TOKEN="<bearer token>"
export AWS_ACCESS_KEY_ID="<AWS Access Key ID>"
export AWS_SECRET_ACCESS_KEY="<AWS Secret Access Key>"
export BUCKET="<S3 bucket name>"
export TWITTER_QUERY="<Twitter query>"
export MAX_TABLE_SIZE="<max table size>"
export S3_PREFIX="<S3 prefix>" 

python tweets_to_s3_csv.py 
```
