#!/usr/bin/env python

import asyncio, socket, ssl
# from time import sleep

BIND_ADDRESS = ""
BIND_PORT = 12345  # Port to listen on (non-privileged ports are > 1023)
UPSTREAM_HOST = '1.1.1.1'
UPSTREAM_PORT = 853
UPSTREAM_CN = 'cloudflare-dns.com'
# UPSTREAM_CAFILE=None

# # TODO: Fix this to run in async
# async def upstream(query, host, port, cn, cafile=None):
#     purpose = ssl.Purpose.SERVER_AUTH
#     context = ssl.create_default_context(purpose, cafile=cafile)
#     raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # raw_sock.setblocking(False)
#     raw_sock.connect((host, port))
#     ssl_sock = context.wrap_socket(raw_sock, server_hostname=cn)
#     ssl_sock.sendall(query)
#     response = ssl_sock.recv(1024)
#     return response

# async def handle_client(reader, writer):
#     query = await reader.read(1024)
#     addr = writer.get_extra_info('peername')
#     print(f"Received message from {addr!r}")
#     if not query:
#         return
#     asyncio.sleep(1)
#     response = await query
#     # response = await asyncio.gather(
#     #     asyncio.to_thread(
#     #         upstream, query, UPSTREAM_HOST, UPSTREAM_PORT,  UPSTREAM_CN
#     #     ))
#     # response = await upstream(
#     #     query,
#     #     UPSTREAM_HOST,
#     #     UPSTREAM_PORT,
#     #     UPSTREAM_CN
#     # )
#     writer.write(response)
#     await writer.drain()
#     print("Close the connection")
#     writer.close()

# async def run_server():
#     server = await asyncio.start_server(handle_client, BIND_ADDRESS, BIND_PORT)
#     async with server:
#         await server.serve_forever()

# asyncio.run(run_server())


async def pipe(reader, writer):
    try:
        while not reader.at_eof():
            writer.write(await reader.read(1024))
    finally:
        writer.close()


async def handle_client(local_reader, local_writer):
    try:
        remote_reader, remote_writer = await asyncio.open_connection(
            UPSTREAM_HOST,
            UPSTREAM_PORT,
            ssl=True,
            server_hostname=UPSTREAM_CN)
        pipe1 = pipe(local_reader, remote_writer)
        pipe2 = pipe(remote_reader, local_writer)
        await asyncio.gather(pipe1, pipe2)
    finally:
        local_writer.close()


# Create the server
loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_client, BIND_ADDRESS, BIND_PORT)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
