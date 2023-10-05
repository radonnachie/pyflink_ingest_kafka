package za.co.discovery.health.bigdata.flink.types;

import org.apache.flink.api.common.serialization.DeserializationSchema;
import org.apache.flink.api.common.serialization.SerializationSchema;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonKafkaSerializationSchema<T> implements SerializationSchema<T>, DeserializationSchema<T>  {
	
    protected static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    protected final String topic;

    protected JsonKafkaSerializationSchema(String topic) {
        this.topic = topic;
    }

    @Override
    public boolean isEndOfStream(T nextElement) {
        return false;
    }

    @Override
    public byte[] serialize(T obj) {
        try {
            return OBJECT_MAPPER.writeValueAsBytes(obj);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }	
}
