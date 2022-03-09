FROM python:latest
  
RUN pip3 install boto3 pandas nltk tweepy uuid numpy
WORKDIR /app
ADD . /app
RUN chmod a+x *.py
ENTRYPOINT ["tweets_to_s3_csv.py"]
