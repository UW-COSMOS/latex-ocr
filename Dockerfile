FROM python:2

RUN mkdir -p /home/app/ 

COPY . /home/app/

WORKDIR /home/app/

RUN make install-linux



