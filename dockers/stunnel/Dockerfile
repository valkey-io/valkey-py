FROM ubuntu:latest
MAINTAINER ahmedsobeh <ahmedszakaria@gmail.com>


RUN apt-get update && apt-get install -y stunnel

COPY conf /etc/stunnel/conf
COPY keys /etc/stunnel/keys

CMD ["stunnel", "/etc/stunnel/conf/stunnel.conf"]
