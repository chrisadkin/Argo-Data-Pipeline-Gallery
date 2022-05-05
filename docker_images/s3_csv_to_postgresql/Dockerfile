FROM python:latest

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip3 install psycopg2
RUN pip3 install boto3 pandas
WORKDIR /app
ADD . /app
RUN chmod a+x *.py
ENTRYPOINT ["/app/s3_csv_to_postgresql.py"]
