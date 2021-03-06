#!/usr/bin/env bash

ENDPOINT_URL=http://10.225.112.70
BUCKET=mssql-2022-demo-raw

mkdir /root/.aws
echo '[Default]\n'$AWS_ACCESS_KEY_ID'\n'$AWS_SECRET_ACCESS_KEY_ID > /root/.aws/credentials

for f in $(s5cmd --endpoint-url $ENDPOINT_URL ls s3://$BUCKET | awk '/^.*\.(psd)$/ { print $4 }');
do
  s5cmd --endpoint-url $ENDPOINT_URL mv s3://$BUCKET/$f s3://$BUCKET/$(echo $f | sed -e 's/psd/csv/g') 
done
