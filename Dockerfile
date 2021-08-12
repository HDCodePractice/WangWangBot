FROM python:latest

RUN apt-get update && apt upgrade -y
RUN cd /
COPY . /WangWangBot/
RUN cd WangWangBot
WORKDIR /WangWangBot
RUN apt-get install -y make
RUN SODIUM_INSTALL=system pip3 install pynacl
RUN pip3 install -U -r requirements.txt
WORKDIR /data
CMD python3 /WangWangBot/main.py