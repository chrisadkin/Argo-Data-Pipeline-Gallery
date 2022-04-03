FROM ubuntu:22.04

RUN apt update && apt upgrade -y
RUN apt-get update && apt-get install ca-certificates openssl wget sysstat locales git curl -y --no-install-recommends

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

RUN wget https://download.java.net/java/GA/jdk17/0d483333a00540d886896bac774ff48b/35/GPL/openjdk-17_linux-x64_bin.tar.gz
RUN tar xvf openjdk-17_linux-x64_bin.tar.gz
RUN mv jdk-17 /opt/
ENV JAVA_HOME=/opt/jdk-17
ENV PATH=$PATH:$JAVA_HOME/bin 

RUN cd /usr/local/bin && wget https://github.com/brianmhess/cassandra-loader/releases/download/v0.0.27/cassandra-loader
RUN chmod 777 /usr/local/bin/cassandra-loader

RUN mkdir /root/.aws
COPY credentials /root/.aws/

WORKDIR /app
ADD . /app
RUN chmod a+x *.sh
ENTRYPOINT ["./s3_csv_to_cassandra.sh"]
