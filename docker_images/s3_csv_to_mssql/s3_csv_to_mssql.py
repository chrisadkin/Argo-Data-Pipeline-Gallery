#!/usr/bin/env python3

import os
import pyodbc
from pathlib import Path
from io import StringIO
import pandas as pd
import boto3

def main():
    s3_conn = boto3.resource(service_name          = 's3',
                             aws_access_key_id     = os.getenv('AWS_ACCESS_KEY_ID'),
                             aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'),
                             endpoint_url          = os.getenv('ENDPOINT_URL'))

    bucket = s3_conn.Bucket(os.getenv('BUCKET'))

    server   = os.getenv('SQL_INSTANCE') 
    database = os.getenv('DATABASE') 
    username = os.getenv('USERNAME') 
    password = os.getenv('PASSWORD') 
    conn     = pyodbc.connect("DRIVER={{SQL Server}}; \
                               SERVER={0}; \
                               DATABASE={1}; \
                               UID={2}; \
                               PWD={3}".format(server, database, username, password))
    cursor = conn.cursor()

    csv_file_count = 0
    tweets_loaded  = 0

    for obj in bucket.objects.all():
        if obj.key.endswith('.csv'):
            print('loading file ' + obj.key)
            res = s3_conn.Object(os.getenv('BUCKET'), obj.key).get()
            csv = res['Body'].read()
            csv_string_io = StringIO(str(csv, 'UTF-8'))
            data_frame = pd.read_csv(csv_string_io,
                                     sep=",",
                                     header=None,
                                     names=['tweet_id'  , 'text',
                                            's_negative', 's_neutral',
                                            's_positive', 's_compound'])

            for row in data_frame.itertuples():
                query = 'INSERT INTO tweets' + \
                        ' (tweet_id, text_body, s_neg, s_pos, s_neu, s_compound) \
                          VALUES (%d, %s, %d, %d, %d, %d)' \	
                        % (row.tweet_id, row.text, \
                           row.s_negative, row.s_neutral, \
                           row.s_positive, row.s_compound)
                cursor.execute(query) 
                tweets_loaded += 1 
            csv_file_count += 1

            copy_source = {
                'Bucket': os.getenv('BUCKET') ,
                'Key': obj.key 
            }

            s3_conn.meta.client.copy(copy_source, Bucket = os.getenv('BUCKET'), Key = Path(obj.key).stem + ".psd")
            s3_conn.Object(os.getenv('BUCKET'), obj.key).delete()  

    if csv_file_count == 0:
        print ('No csv files found')
    else:
        print (str(tweets_loaded) + ' tweets loaded')

if __name__ == "__main__":
    main()
