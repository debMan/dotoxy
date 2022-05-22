# *dotoxy*: A simple DoT proxy

The very simple DoT proxy. which proxies plain DNS queries to an upstream DoT
provider.

## Introduction

This service listens on a TCP address and port and proxies the plain DNS
queries to an upstream using sockets on python in an async manner. The script
utilizes simple pipes which connect the local's read stream to the provider's
write stream and the local's write stream to the provider's read stream.

## Usage

### Local

``` bash
git clone https://github.com/debMan/dotoxy.git
cd dotoxy
dotoxy --help
```

### Docker

``` bash
# local build
git clone https://github.com/debMan/dotoxy.git
docker image build -t dotoxy dotoxy
docker container run -d -p 53:53 dotoxy:latest

# or from Docker Hub
docker container run -d -p 53:53 idebman/dotoxy:latest
```

## Configurations

Use the `config.yml` file or environment variables to configure *dotoxy*. The
`config.example.yml` can help you, default values are added. Refer to
[Configurations references](#configurations-references).

## Security concerns

Some of the common security concerns to be considered:

- Rate limiting incoming requests to prevent requests flooding and DOS attacks
- Whitelisting client addresses to prevent abuse of the service

## Deployment

The service is ready for deployments on container orchestrator platforms like
**Kubernetes**. As it's stateless, horizontal scaling is simple.

## Missing improvements

- [x] Make the proxy non-blocking on the client-side
- [x] Make the proxy non-blocking on the upstream side
- [ ] Add UDP support
- [x] Make the proxy configurable (upstream, bind address, port, TLS versions,
  etc) with environment variables and config file
- [ ] Check packet length with the prefixed two-byte field which gives the
  message length
- [ ] Add IPv6 support
- [ ] Add multiple upstream support
- [ ] Add Prometheus exporter endpoint to monitor runtime status
- [ ] Add `setup.py` and convert the service to a PyPI package

## Configurations references

The absolute path to the config file can be set by `CONFIG_ADDRESS` environment
variable.

| `yml` key           | type   | env                    | default              | description                                                         |
| ------------------- | ------ | ---------------------- | -------------------- | ------------------------------------------------------------------- |
| upstream.host       | string | `UPSTREAM__HOST`       | `1.1.1.1`            | Upstream server (usually IP) address                                |
| upstream.port       | int    | `UPSTREAM__PORT`       | `853`                | Upstream DoT TCP port                                               |
| upstream.cn         | string | `UPSTREAM__CN`         | `cloudflare-dns.com` | Upstream server common name (domain name) to verify its certificate |
| upstream.ca-file    | string | `UPSTREAM__CA_FILE`    | Undefined            | Path to local CA to verify upstream's certificate                   |
| server.bind-address | string | `SERVER__BIND_ADDRESS` | `0.0.0.0`            | Local interface for binding the server to                           |
| upstream.bind-port  | int    | `SERVER__BIND_PORT`    | `53`                 | Local port for binding the server to                                |

## References

- <https://stackoverflow.com/questions/48506460/python-simple-socket-client-server-using-asyncio>
- <https://docs.python.org/3/library/asyncio-eventloop.html>
- <https://stackoverflow.com/questions/63226614/how-to-make-a-tls-connection-using-python>
- <https://docs.python.org/3/library/socket.html>
- <https://docs.python.org/3/library/ssl.html>
- <https://stackoverflow.com/questions/46413879/how-to-create-tcp-proxy-server-with-asyncio>
- Some snippets available in the [samples](sample) directory
