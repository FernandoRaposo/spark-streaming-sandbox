### 1. Get Linux
FROM alpine:3.10.2

### 2. Get Java via the package manager
RUN apk update \
&& apk upgrade \
&& apk add --no-cache bash \
&& apk add --no-cache --virtual=build-dependencies unzip \
&& apk add --no-cache curl \
&& apk add --no-cache openjdk8-jre

### 3. Get Python, PIP
RUN apk add --no-cache python3 \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip setuptools \
    && rm -r /usr/lib/python*/ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN echo "alias l='ls -lhA && pwd'" > /root/.bashrc
RUN source /root/.bashrc

RUN apk --update add wget tar bash

RUN wget -nv https://www-eu.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz

RUN tar -xzf spark-2.4.4-bin-hadoop2.7.tgz && \
    mv spark-2.4.4-bin-hadoop2.7 /spark && \
    rm spark-2.4.4-bin-hadoop2.7.tgz

ADD requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

ADD main.py app/main.py
ADD schemas.py app/schemas.py

RUN mkdir app/data

RUN wget -nv https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat -O app/data/routes.dat

ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"

ADD commands.sh commands.sh
RUN ["chmod", "+x", "commands.sh"]
