FROM python:3-alpine
LABEL authors="Juan Manuel Aidar"

RUN apk update
RUN apk add git
RUN git clone https://github.com/jaidar2003
WORKDIR /estadistica2.git
RUN pip install -r requirements.txt

CMD [ "sh", "-c"]

# Path: requirements.txt
