package za.co.discovery.health.bigdata.flink;

import java.util.Properties;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
// import org.apache.flink.streaming.util.serialization.SimpleStringSchema;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.flink.api.common.serialization.SimpleStringSchema;

// import org.apache.flink.api.common.serialization.DeserializationSchema;
// import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.connector.kafka.source.reader.deserializer.KafkaRecordDeserializationSchema;
// import org.apache.flink.util.Collector;
// import org.apache.kafka.clients.consumer.ConsumerRecord;
// import org.apache.kafka.common.TopicPartition;
// import org.apache.kafka.common.serialization.Deserializer;

import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;


public class KafkaFeastBridge {

  private static final Logger LOG = LogManager.getLogger(KafkaFeastBridge.class);

  public static Properties getFeastPushProperties(ParameterTool params) {
    return getPrefixScopedProperties(params, "feast.push.");
  }

  public static Properties getKafkaProperties(ParameterTool params) {
    return getPrefixScopedProperties(params, "kafka.");
  }

  public static Properties getPrefixScopedProperties(ParameterTool params, String prefix) {
    Properties properties = new Properties();
    for (String key : params.getProperties().stringPropertyNames()) {
      if (key.startsWith(prefix)) {
        properties.setProperty(key.substring(prefix.length()), params.get(key));
      }
    }

    LOG.info("### '{}' parameters:", prefix);
    for (String key : properties.stringPropertyNames()) {
      LOG.info("'{}'' param: {}={}", prefix, key, properties.get(key));
    }
    return properties;
  }

  public static void main(String[] args) throws Exception {
    StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
    ParameterTool params = ParameterTool.fromPropertiesFile(args[0]);
        
    KafkaSource<String> rawKafkaSource = KafkaSource.<String>builder()
        .setBootstrapServers(params.getRequired("kafka.bootstrap.servers"))
        .setTopics(params.getRequired("kafka.topic.source"))
        // .setDeserializer(KafkaRecordDeserializationSchema.valueOnly(StringDeserializer.class))
        .setValueOnlyDeserializer(new SimpleStringSchema())
        // .setValueOnlyDeserializer(new FeastPushSchema(topic))
        // .setStartingOffsets(OffsetsInitializer.latest())
        // .setProperties(getKafkaProperties(params))
        .build();

    DataStream<String> kafkaStream = env
        .fromSource(rawKafkaSource, WatermarkStrategy.noWatermarks(), "Kafka Push Source")
        .uid("kafka-push-source");
    // kafkaStream.print();
    kafkaStream.addSink(new FeastPushSink(getFeastPushProperties(params))).name("Feast Push Sink");

    env.execute(params.getRequired("flink.job.title"));
  }
}
