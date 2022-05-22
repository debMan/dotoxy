#!/usr/bin/env python
# echo-server.py

import ssl
import socket
from threading import Thread

BIND_ADDRESS = ""
BIND_PORT = 1234  # Port to listen on (non-privileged ports are > 1023)
UPSTREAM_HOST='1.1.1.1'
UPSTREAM_PORT=853
UPSTREAM_CN = 'cloudflare-dns.com'
# UPSTREAM_CAFILE=None


def upstream(query, host, port, cn, cafile=None):
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile=cafile)
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((host, port))
    print('Connected to host {} and port {} to query DNS'.format(host, port))
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=cn)
    ssl_sock.sendall(query)
    response = ssl_sock.recv(1024)
    return response

def handle_client(connection):
    # while True:
        query = connection.recv(1024)
        if not query:
            # break
            return
        response = upstream(
            query, 
            UPSTREAM_HOST, 
            UPSTREAM_PORT, 
            UPSTREAM_CN
        )
        connection.sendall(response)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((BIND_ADDRESS, BIND_PORT))
    s.listen(10)
    while True:
        conn, addr = s.accept()
        host, port = addr
        with conn:
            # print('Incomming connection from {} and port {}'
            #       .format(host, port))
            # TODO: make thread
            Thread(target=handle_client(conn), daemon=True).start()
            # TODO: Kill thread