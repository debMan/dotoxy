FROM python:3.10-alpine

WORKDIR /dot-proxy
EXPOSE 53/tcp 53/udp

COPY . .

ENTRYPOINT [ "/dot-proxy/tcp.py" ]