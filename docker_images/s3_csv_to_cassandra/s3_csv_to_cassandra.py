#!/usr/bin/env python3

import os
from pathlib import Path
from io import StringIO
import pandas as pd
import boto3
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def main():
    s3_conn = boto3.resource(service_name          = 's3',
                             aws_access_key_id     = os.getenv('AWS_ACCESS_KEY_ID'),
                             aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'),
                             endpoint_url          = os.getenv('ENDPOINT_URL'))

    bucket = s3_conn.Bucket(os.getenv('BUCKET'))

    auth_provider = PlainTextAuthProvider(username = os.getenv('CASSANDRA_USER'), \
                                          password = os.getenv('CASSANDRA_PASSW'))

    cluster = Cluster([os.getenv('CASSANDRA_IP')], \
                      port          = os.getenv('CASSANDRA_PORT'),
                      auth_provider = auth_provider)

    session = cluster.connect()

    keyspace        = os.getenv('KEYSPACE')
    table           = os.getenv('TABLE')

    query = f'''
        CREATE KEYSPACE IF NOT EXISTS {keyspace}
        WITH REPLICATION = {{ 
            'class' : 'SimpleStrategy', 
            'replication_factor' : 1 
        }};
    '''

    session.execute(query)

    query = f'''
        CREATE TABLE IF NOT EXISTS {keyspace}.{table} (
            tweet_id   bigint,
            text_body  text,
            s_neg      decimal, 
            s_pos      decimal,
            s_neu      decimal,
            s_compound decimal,
            PRIMARY KEY (tweet_id)
        );
    '''

    session.execute(query)

    query = 'INSERT INTO ' + keyspace + '.' + table + \
            ' (tweet_id,text_body,s_neg,s_pos,s_neu,s_compound) VALUES (?,?,?,?,?,?)'

    prepared = session.prepare(query)

    for obj in bucket.objects.all():
        if obj.key.endswith('.csv'):
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
                session.execute(prepared, (row.tweet_id  , row.text,
                                           row.s_negative, row.s_neutral,
                                           row.s_positive, row.s_compound))

            s3_conn.Object(os.getenv('BUCKET'), \
                           Path(obj.key).stem + ".psd").copy_from(CopySource=obj.key)
            s3_conn.Object(os.getenv('BUCKET'), obj.key).delete()

    cluster.shutdown()

if __name__ == "__main__":
    main()
