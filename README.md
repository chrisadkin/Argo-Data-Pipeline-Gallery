# Overview

A collection of docker images (one initially) that can be incorporated into an Argo workflow in order to create data pipilines.

# Available Images

tweets_to_s3_csv - leverages the Tweepy API via Python in order to extract tweets, sentiment score the tweets and store them in csv file form in an S3 bucket

# Available Workflows

(tweets_to_s3_csv)[https://github.com/chrisadkin/Argo-Data-Pipeline-Gallery/tree/main/workflows/tweets_to_s3_csv] - sample workflow manifest that leverages the tweets_to_s3_csv image as the entry point task.
