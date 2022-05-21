# dot-proxy

The very simple DoT proxy

## TODO

- [x] Make the proxy non-blocking on client side
- [ ] Make the proxy non-blocking oon upstream side
- [ ] Make the proxy configurable (upstream, bind address, port, protocol)
- [ ] Check packet length with the prefixed two byte field which gives the
  message length
- [ ] Handle upstream TLS versions

## References

- https://stackoverflow.com/questions/48506460/python-simple-socket-client-server-using-asyncio
- https://docs.python.org/3/library/asyncio-eventloop.html
- https://stackoverflow.com/questions/63226614/how-to-make-a-tls-connection-using-python
- https://docs.python.org/3/library/socket.html
- https://docs.python.org/3/library/ssl.html
