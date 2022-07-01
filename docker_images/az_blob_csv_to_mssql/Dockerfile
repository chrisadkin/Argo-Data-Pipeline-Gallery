FROM mcr.microsoft.com/mssql-tools:latest
USER root
RUN apt-get update
RUN apt-get install -y python3-pip python3-dev wget unixodbc-dev libffi-dev
RUN wget https://bootstrap.pypa.io/pip/3.5/get-pip.py
RUN python3 get-pip.py --ignore-installed
RUN pip3 install pandas pyodbc azure-storage-blob	
WORKDIR /app
ADD . /app
RUN chmod a+x *.py
ENTRYPOINT ["/app/az_blob_csv_to_mssql.py"]
