#!/usr/bin/env bash

mkdir ~/.aws
echo '[default]\nAWS_ACCESS_KEY_ID = '$AWS_ACCESS_KEY_ID'\nAWS_SECRET_ACCESS_KEY = '$AWS_SECRET_ACCESS_KEY > ~/.aws/credentials

for f in $(s5cmd --endpoint-url $ENDPOINT_URL ls s3://$BUCKET | awk '/^.*\.(csv)$/ { print $4 }');
do
  s5cmd --endpoint-url $ENDPOINT_URL cat s3://$BUCKET/$f | /opt/mssql-tools/bin/bcp tweet in /dev/stdin -S $SERVER -d $DATABASE -U $USERNAME -P $PASSWORD -q -c -t ,
  s5cmd --endpoint-url $ENDPOINT_URL mv s3://$BUCKET/$f s3://$BUCKET/$(echo $f | sed -e 's/csv/psd/g') 
done
