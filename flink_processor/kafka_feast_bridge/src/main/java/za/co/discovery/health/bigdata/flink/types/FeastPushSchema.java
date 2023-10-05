package za.co.discovery.health.bigdata.flink.types;

import org.apache.flink.api.common.typeinfo.TypeHint;
import org.apache.flink.api.common.typeinfo.TypeInformation;

import java.io.IOException;

public class FeastPushSchema extends JsonKafkaSerializationSchema<FeastPush> {

	public FeastPushSchema(String topic) {
		super(topic);
	}

	@Override
	public FeastPush deserialize(byte[] message) {
		try {
			return OBJECT_MAPPER.readValue(message, FeastPush.class);
		} catch (IOException e) {
			return null;
		}
	}

	@Override
	public TypeInformation<FeastPush> getProducedType() {
		return new TypeHint<FeastPush>() {
		}.getTypeInfo();
	}
}
