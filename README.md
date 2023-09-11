`docker compose up`

Inside the jobmanager container:

```
$ cd /work/feature_store
$ feast apply
$ /opt/flink/bin/flink run -py /work/run.py -d
```