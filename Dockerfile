FROM python:3.10-alpine

WORKDIR /dotoxy
EXPOSE 53/tcp 53/udp
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY config.example.yml config.yml
COPY . .

ENTRYPOINT [ "/dotoxy/dotoxy.py" ]