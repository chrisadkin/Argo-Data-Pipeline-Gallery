# Overview

A collection of docker images (one initially) that can be incorporated into an Argo workflow in order to create data pipilines.

# Prerequisites

Running the examples in this repo requires access to a Kubernetes cluster to which Argo workflow deployed, refer to the [Argo workflow quick start guide](https://argoproj.github.io/argo-workflows/quick-start/) for the fastest means of deploying Argo workflow.

# Available Images

[tweets_to_s3_csv](https://github.com/chrisadkin/Argo-Data-Pipeline-Gallery/blob/main/docker_images/tweets_to_s3_csv/README.md) - leverages the Tweepy API via Python in order to extract tweets, sentiment score the tweets and store them in csv file form in an S3 bucket

# Available Workflows

[tweets_to_s3_csv](https://github.com/chrisadkin/Argo-Data-Pipeline-Gallery/tree/main/workflows/tweets_to_s3_csv) - sample workflow manifest that leverages the tweets_to_s3_csv image as the entry point task.
