# PyFlink

In order to enable PyFlink, the flink image needs to be extended.

1. Get tar.gz files from:
   - https://pypi.org/project/apache-flink/#files
   - https://pypi.org/project/apache-flink-libraries/#files
   - https://kafka.apache.org/downloads (Scala 2.12)
2. Extract the kafka_2.12-*.tgz in this directory.
3. Finally, uncomment the related section of the Dockerfile.
