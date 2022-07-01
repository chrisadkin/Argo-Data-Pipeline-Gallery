#!/usr/bin/env python3

import os
import pyodbc
import platform
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from pathlib import Path
from io import StringIO
import pandas as pd

def main():
    connect_str = os.getenv('AZURE_CONNECT_STR')
    container   = os.getenv('CONTAINER')

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container)
    blob_list = container_client.list_blobs()

    if platform.platform().find("macOS") != -1:
        driver   = '/usr/local/opt/msodbcsql18/lib/libmsodbcsql.18.dylib'
    
    if platform.platform().find("Ubuntu") != -1:
        driver   = '/opt/microsoft/msodbcsql/lib64/libmsodbcsql-13.1.so.9.1'

    server   = os.getenv('SQL_INSTANCE') 
    database = os.getenv('DATABASE') 
    username = os.getenv('SQLUSER') 
    password = os.getenv('PASSWORD') 

    conn = pyodbc.connect('DRIVER='+driver+
                          ';SERVER=tcp:'+server+
                          ';PORT=1433;DATABASE='+database+
                          ';UID='+username+
                          ';PWD='+ password+
                          ';TrustServerCertificate=yes;')
    cursor = conn.cursor()

    csv_file_count  = 0
    tweets_loaded   = 0                                    
    tweets_rejected = 0                                    

    for blob in blob_list:
        csv = blob_service_client.get_blob_client(container, blob).download_blob().readall()
        csv_string_io = StringIO(str(csv, 'UTF-8'))
        data_frame = pd.read_csv(csv_string_io,
                                 sep    = ",",
                                 header = None,
                                 names  = [ 'tweet_id'  , 'text',
                                            's_negative', 's_neutral',
                                            's_positive', 's_compound'])

        for row in data_frame.itertuples():
            query = 'INSERT INTO tweets' \
                    ' (tweet_id, tweet_body, s_neg, s_pos, s_neu, s_compound) \
                      VALUES (%d, \'%s\', %d, %d, %d, %d)' \
                    % (row.tweet_id  , row.text, \
                       row.s_negative, row.s_neutral, \
                       row.s_positive, row.s_compound)
            try:
                cursor.execute(query) 
                conn.commit()
                tweets_loaded += 1
            except Exception:
                tweets_rejected += 1
                pass

        csv_file_count += 1

    if csv_file_count == 0:
        print ('No csv files found')
    else:
        print (str(tweets_loaded)   + ' tweets loaded')
        print (str(tweets_rejected) + ' tweets rejected')

if __name__ == "__main__":
    main()
