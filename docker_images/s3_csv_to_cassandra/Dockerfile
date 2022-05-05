FROM python:latest
  
RUN pip3 install boto3 pandas cassandra-driver 
WORKDIR /app
ADD . /app
RUN chmod a+x *.py
ENTRYPOINT ["/app/s3_csv_to_cassandra.py"]
