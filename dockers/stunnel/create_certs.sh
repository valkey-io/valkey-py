#!/bin/bash

set -e

CONFIG_FILE=$(realpath "$(dirname "$0")")/openssl.cnf

DESTDIR=$(dirname "$0")/keys
test -d ${DESTDIR} || mkdir ${DESTDIR}
cd ${DESTDIR}

which openssl &>/dev/null
if [ $? -ne 0 ]; then
   echo "No openssl binary present, exiting."
   exit 1
fi

openssl genrsa -out ca-key.pem 2048 &>/dev/null

openssl req -new -x509 -nodes -days 365000 \
   -key ca-key.pem \
   -out ca-cert.pem \
   -config "$CONFIG_FILE" \
   -extensions v3_ca \
   -subj "/CN=valkey-py-ca"

openssl req -newkey rsa:2048 -nodes \
   -keyout server-key.pem \
   -out server-req.pem \
   -config "$CONFIG_FILE" \
   -extensions v3_req \
   -subj "/CN=valkey-py-server"

openssl x509 -req -days 365000 -set_serial 01 \
   -in server-req.pem \
   -out server-cert.pem \
   -CA ca-cert.pem \
   -CAkey ca-key.pem \
   -extfile "$CONFIG_FILE" \
   -extensions v3_req

openssl req -newkey rsa:2048 -nodes \
   -keyout client-key.pem \
   -out client-req.pem \
   -config "$CONFIG_FILE" \
   -extensions v3_req \
   -subj "/CN=valkey-py-client"

openssl x509 -req -days 365000 -set_serial 01 \
   -in client-req.pem \
   -out client-cert.pem \
   -CA ca-cert.pem \
   -CAkey ca-key.pem \
   -extfile "$CONFIG_FILE" \
   -extensions v3_req

echo "Keys generated in ${DESTDIR}:"
ls
