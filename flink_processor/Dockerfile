FROM flink:1.17.1-scala_2.12-java8

# install python3: it has updated Python to 3.9 in Debian 11 and so install Python 3.7 from source
# it currently only supports Python 3.6, 3.7 and 3.8 in PyFlink officially.

RUN apt-get update -y && \
apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libffi-dev liblzma-dev && \
wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz && \
tar -xvf Python-3.8.0.tgz && \
cd Python-3.8.0 && \
./configure --without-tests --enable-shared && \
make -j6 && \
make install && \
ldconfig /usr/local/lib && \
cd .. && rm -f Python-3.8.0.tgz && rm -rf Python-3.8.0 && \
ln -s /usr/local/bin/python3 /usr/local/bin/python && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

# install PyFlink

COPY apache-flink*.tar.gz /
RUN pip3 install --upgrade pip && pip3 install /apache-flink-libraries*.tar.gz && pip3 install /apache-flink*.tar.gz && pip3 install kafka-python

COPY kafka_2.12-*/libs/*.jar /opt/flink/lib/

# Download connector libraries
RUN wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-json/1.17.1/flink-json-1.17.1.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-kafka/1.17.1/flink-connector-kafka-1.17.1.jar;
