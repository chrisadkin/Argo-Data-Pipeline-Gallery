#!/usr/bin/env python3

import os
from io import StringIO
from pathlib  import Path
import psycopg2
import pandas as pd
import boto3
from psycopg2 import sql

def main():
    table            = os.getenv('TABLE')

    s3_conn = boto3.resource(service_name          = 's3',
                             aws_access_key_id     = os.getenv('AWS_KEY'),
                             aws_secret_access_key = os.getenv('AWS_SECRET'),
                             endpoint_url          = os.getenv('AWS_ENDPOINT'))

    bucket = s3_conn.Bucket(os.getenv('BUCKET'))

    connection = psycopg2.connect(user     = os.getenv('POSTGRESQL_USER'),
                                  password = os.getenv('POSTGRESQL_PASSW'),
                                  host     = os.getenv('POSTGRESQL_HOST'),
                                  port     = os.getenv('POSTGRESQL_PORT'),
                                  database = os.getenv('DATABASE'))

    cursor = connection.cursor()
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")

    query = f'''
        CREATE TABLE IF NOT EXISTS { os.getenv('TABLE') } (
            tweet_id   bigint,
            text_body  text,
            s_neg      numeric(4,2), 
            s_pos      numeric(4,2),
            s_neu      numeric(4,2),
            s_compound numeric(4,2),
            PRIMARY KEY (tweet_id)
        );
    '''

    cursor.execute(query)

    csv_file_count = 0
    tweets_loaded  = 0

    for obj in bucket.objects.all():
        if obj.key.endswith('.csv'):
            res = s3_conn.Object(os.getenv('BUCKET'), obj.key).get()
            csv = res['Body'].read()
            csv_string_io = StringIO(str(csv, 'UTF-8'))
            data_frame  = pd.read_csv(csv_string_io, sep=",", header=None,
                                      names=['tweet_id', 'text',
                                             's_negative', 's_neutral',
                                             's_positive', 's_compound'])
            print("Loading file: " + obj.key)
            for row in data_frame.itertuples():
                cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s)")
                        .format(sql.Identifier(table)),
                        [row.tweet_id, row.text,
                        row.s_negative, row.s_neutral,
                        row.s_positive, row.s_compound])
                connection.commit()
                tweets_loaded += 1

            csv_file_count += 1

            copy_source = {
                'Bucket': os.getenv('BUCKET'),
                'Key'   : obj.key
            }

            s3_conn.meta.client.copy(copy_source,
                                     Bucket = os.getenv('BUCKET'),
                                     Key    = Path(obj.key).stem + ".psd")
            s3_conn.Object(os.getenv('BUCKET'), obj.key).delete()

    if connection:
        cursor.close()
        connection.close()

    if csv_file_count == 0:
        print ('No csv files found')
    else:
        print (str(tweets_loaded) + ' tweets loaded')

if __name__ == "__main__":
    main()
