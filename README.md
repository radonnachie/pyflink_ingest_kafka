# Use

> NOTE: the datetimes pushed from kafka are coming out as NaT...

See the [flink_processor/README.md](./flink_processor/README.md) for some downloads that must be present there.

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

## Initiate the pyflink job
`docker exec -it ffpk_jobmanager /opt/flink/bin/flink run -py /work/run.py -d`

Check the features:

`docker exec -it -w /work/feature_store ffpk_feast_service python /work/get_features.py`
