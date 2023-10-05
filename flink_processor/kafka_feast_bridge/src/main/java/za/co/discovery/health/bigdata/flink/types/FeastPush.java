package za.co.discovery.health.bigdata.flink.types;

import java.util.Objects;

import javax.management.Query;

public class FeastPush {
	
	public String pushSourceName;
	public Object df;
	public String to;

	public FeastPush() {}

	public FeastPush(
		String pushSourceName,
		Object df,
		String to
	) {
		this.pushSourceName = pushSourceName;
		this.df = df;
		this.to = to;
	}

	@Override
	public String toString() {
		return "FeastPush{" +
				"pushSourceName=" + pushSourceName +
				", df=" + df +
				", to='" + to + '\'' +
				'}';
	}
}
