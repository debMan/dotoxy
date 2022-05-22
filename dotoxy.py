#!/usr/bin/env python

import asyncio

from config import Config


local_server = Config().server
upstream = Config().upstream

UPSTREAM_HOST = upstream.get("host")
UPSTREAM_PORT = upstream.get("port")
UPSTREAM_CN = upstream.get("cn")
UPSTREAM_CAFILE = upstream.get("ca-file")
BIND_ADDRESS = local_server.get("bind-address")
BIND_PORT = local_server.get("bind-port")


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

if __name__ == "__main__":
    # Create the server
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_client, BIND_ADDRESS, BIND_PORT)
    server = loop.run_until_complete(coro)
    # Serve requests until Ctrl+C is pressed
    print('Serving on {}:{}'.format(BIND_ADDRESS, BIND_PORT))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("WARN: KeyboardInterrupt, exiting ...")
    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
