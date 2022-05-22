#!/usr/bin/env python

import asyncio, socket, ssl

BIND_ADDRESS = ""
BIND_PORT = 12345  # Port to listen on (non-privileged ports are > 1023)
UPSTREAM_HOST='1.1.1.1'
UPSTREAM_PORT=853
UPSTREAM_CN = 'cloudflare-dns.com'
# UPSTREAM_CAFILE=None

# TODO: Fix this to run in async
async def upstream(query, host, port, cn, cafile=None):
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile=cafile)
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # raw_sock.setblocking(False)
    raw_sock.connect((host, port))
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=cn)
    ssl_sock.sendall(query)
    response = ssl_sock.recv(1024)
    return response

async def handle_client(reader, writer):
    query = await reader.read(1024)
    addr = writer.get_extra_info('peername')
    print(f"Received message from {addr!r}")
    if not query:
        return
    # response = await asyncio.gather(
    #     asyncio.to_thread(
    #         upstream, query, UPSTREAM_HOST, UPSTREAM_PORT,  UPSTREAM_CN
    #     ))
    response = await upstream(
        query,
        UPSTREAM_HOST,
        UPSTREAM_PORT,
        UPSTREAM_CN
    )
    writer.write(response)
    await writer.drain()
    print("Close the connection")
    writer.close()

async def run_server():
    server = await asyncio.start_server(handle_client, BIND_ADDRESS, BIND_PORT)
    async with server:
        await server.serve_forever()

asyncio.run(run_server())