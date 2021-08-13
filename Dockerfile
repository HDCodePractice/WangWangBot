FROM python:latest

RUN apt-get update && \
    apt upgrade -y && \
    apt-get install -qy curl && \
    apt-get install -qy libsodium-dev && \
    curl -fsSL https://get.docker.com | sh && \
    (curl -Ls https://cli.doppler.com/install.sh || wget -qO- https://cli.doppler.com/install.sh) | sh
RUN cd /
COPY . /WangWangBot/
RUN cd WangWangBot
WORKDIR /WangWangBot
RUN SODIUM_INSTALL=system pip install pynacl
RUN pip3 install -U -r requirements.txt
WORKDIR /data
ENTRYPOINT [ "doppler", "run", "--" ]
CMD ["python3", "/WangWangBot/main.py"]