# Use

`docker compose up -d`

## Test the pushservice

Push 2 features with entity numbers `999998, 999999` exclusively to the online store:

`docker exec -it ffpk_jobmanager curl -X POST --data "@/work/push_request_payload.json" -H "Content-type: application/json" http://feast_service:8888/push`

View the offline and online features (note that the 2 pushed are the only ones evident online and aren't evident offline):

`docker exec -it -w /work/feature_store ffpk_feast_service python /work/get_features.py`

Or use the feast service's endpoint:

`docker exec -it ffpk_feast_service curl -X POST --data "@/work/online_features_request_payload.json" http://localhost:8888/get-online-features`

<details><summary>Optionally materialize all the historical features</summary>

`docker exec -it -w /work/feature_store ffpk_feast_service feast materialize "2000-01-01 15:00" "2001-01-01 12:00"`
</details>

## Initiate the job

<details><summary>Java</summary>

Package the job (from within `flink_processor/kafka_feast_bridge`):

`docker run --rm --name kafka_feast_bridge -v .:/work/ -w /work/ maven:3.3-jdk-8 mvn clean package`

Copy the packaged jar and configuration file across:

```
docker cp flink_processor/kafka_feast_bridge/target/kafka_feast_bridge-1.0-SNAPSHOT.jar ffpk_jobmanager:/work/
docker cp flink_processor\kafka_feast_bridge\src/main/java/\za\co\discovery\health\bigdata\flink\config\job.properties ffpk_jobmanager:/work/
```

Queue the job across:

`docker exec -it -w /work/ ffpk_jobmanager flink run -d kafka_feast_bridge-1.0-SNAPSHOT.jar /work/job.properties`
</details>


<details><summary>PyFlink</summary>

See the [flink_processor/README.md](./flink_processor/README.md) for changes that must be made to the flink image.

`docker exec -it ffpk_jobmanager /opt/flink/bin/flink run -py /work/run.py -d`
</details>

Check the features:

`docker exec -it -w /work/feature_store ffpk_feast_service python /work/get_features.py`

The `online_features` section should have values populated that aren't in the `offline_features` section.
