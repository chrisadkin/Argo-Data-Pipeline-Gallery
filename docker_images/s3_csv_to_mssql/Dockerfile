FROM ubuntu:20.04

RUN apt update && apt upgrade -y
RUN apt-get update && apt-get install openssl wget sysstat locales git curl ca-certificates gnupg2 -y --no-install-recommends

ARG cert_location=/usr/local/share/ca-certificates
RUN openssl s_client -showcerts -connect github.com:443 </dev/null 2>/dev/null|openssl x509 -outform PEM > ${cert_location}/github.crt
RUN openssl s_client -showcerts -connect proxy.golang.org:443 </dev/null 2>/dev/null|openssl x509 -outform PEM >  ${cert_location}/proxy.golang.crt
RUN update-ca-certificates  

RUN cd /tmp && wget -c https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz && tar -xvf go1.14.2.linux-amd64.tar.gz
RUN mv /tmp/go /usr/local/go
ENV GOROOT=/usr/local/go
ENV GOPATH=$HOME/go
ENV PATH=$GOPATH/bin:$GOROOT/bin:$PATH
RUN /usr/local/go/bin/go get -u github.com/peak/s5cmd

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | tee /etc/apt/sources.list.d/msprod.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

WORKDIR /app
ADD . /app
RUN chmod a+x *.sh
ENTRYPOINT ["./s3_csv_to_mssql.sh"]
