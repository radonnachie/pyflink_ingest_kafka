import requests
import json

from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common import Types, SimpleStringSchema
from pyflink.datastream.formats.json import JsonRowDeserializationSchema


def push(json_str):
    requests.post(
        url="http://feast_service:8888/push",
        data=json.dumps({
            "push_source_name": "whcaent_ent_push_source",
            "df": json.loads(json_str),
            "to": "online"
        }),
        headers={
            "Content-Type": "application/json"
        }
    )
    return []


# jar files expected to be in "/opt/flink/lib/"
env = StreamExecutionEnvironment.get_execution_environment()

# deserialization_schema = JsonRowDeserializationSchema.Builder() \
#     .type_info(Types.ROW([
#         Types.INT(),  # entity_no
#         Types.STRING(),  # title
#         Types.STRING(),  # firstname
#         Types.STRING(),  # surname
#         Types.STRING(),  # date_of_birth
#         Types.STRING(),  # sys_eff_to
#         Types.STRING(),  # sys_eff_from
#     ])) \
#     .build()

kafkaSource = KafkaSource \
    .builder() \
    .set_bootstrap_servers('kafka_broker:9092') \
    .set_topics('TEST_FEAST') \
    .set_value_only_deserializer(SimpleStringSchema()) \
    .build()
    # .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \

ds = env.from_source(
    kafkaSource,
    WatermarkStrategy.no_watermarks(),
    source_name="kafka_TEST_FEAST"
)

ds.flat_map(push)
env.execute("kafkaread")
