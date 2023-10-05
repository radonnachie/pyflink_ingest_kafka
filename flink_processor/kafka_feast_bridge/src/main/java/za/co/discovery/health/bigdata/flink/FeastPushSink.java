package za.co.discovery.health.bigdata.flink;

import java.util.Properties;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.StandardCharsets;
import java.io.OutputStream;
import java.net.HttpURLConnection;

import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;

public class FeastPushSink extends RichSinkFunction<String> {
  private final URL url;
  private final String pushPayloadJsonPrefix;

  public FeastPushSink(Properties properties) throws Exception {
    this.url = new URL (properties.get("service.url").toString());
    System.out.println(this.url);
    String pushSourceName = properties.get("source.name").toString();
    String pushDirection = properties.get("direction").toString();
    StringBuilder sb = new StringBuilder();
    sb.append("{\"push_source_name\": \"");
    sb.append(pushSourceName);
    sb.append("\", \"to\": \"");
    sb.append(pushDirection);
    sb.append("\", \"df\": ");
    this.pushPayloadJsonPrefix = sb.toString();
  }

  @Override
  public void invoke(String json) throws Exception {
    StringBuilder sb = new StringBuilder();
    sb.append(this.pushPayloadJsonPrefix);
    sb.append(json);
    sb.append("}");
    String json_payload = sb.toString();

    HttpURLConnection con = (HttpURLConnection) this.url.openConnection();
    con.setRequestMethod("POST"); // PUT is another valid option
    con.setDoOutput(true);

    byte[] out = json_payload.getBytes(StandardCharsets.UTF_8);
    int length = out.length;

    con.setFixedLengthStreamingMode(length);
    con.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
    con.connect();
    try(OutputStream os = con.getOutputStream()) {
        os.write(out);
    }

    // con.setRequestMethod("POST");
    // con.setRequestProperty("Content-Type", "application/json");
    // con.setDoOutput(true);
    // con.setRequestProperty("charset", "utf-8");
    // con.setRequestProperty("Content-Length", Integer.toString(json_payload.length()));
    // try(OutputStream os = con.getOutputStream()) {
    //     byte[] input = json_payload.getBytes("utf-8");
    //     os.write(input);//, 0, input.length);
    // }
  }
}
