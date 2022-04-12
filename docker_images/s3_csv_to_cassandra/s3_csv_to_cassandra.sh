#!/usr/bin/env bash

for f in $(s5cmd --endpoint-url $ENDPOINT_URL ls s3://$BUCKET | awk '/^.*\.(csv)$/ { print $4 }');
do
  s5cmd --endpoint-url $ENDPOINT_URL cat s3://$BUCKET/$f | cassandra-loader -f stdin -user $USERNAME -pw $PASSWORD -host $CASSANDRA_HOST -schema "$KEYSPACE.tweet(tweet_id, text_body, s_neg, s_pos, s_neu, s_compound)"
  s5cmd --endpoint-url $ENDPOINT_URL mv s3://$BUCKET/$f s3://$BUCKET/$(echo $f | sed -e 's/csv/psd/g') 
done
