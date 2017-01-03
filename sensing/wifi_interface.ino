#include <ESP8266WiFi.h>
 
const char* ssid     = "sense";
const char* password = "S3ns1nG_bu5"; 
const char* host = "146.164.69.186";
const char* skpln = "\r\n";
String url = "/";
 
void setup() {
  Serial.begin(115200);
  delay(100);
 
  // We start by connecting to a WiFi network
  /*
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  //*/
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    //Serial.print(".");
  }
 
  //Serial.println("");
  Serial.println("WiFi connected");  
  //Serial.println("IP address: ");
  //Serial.println(WiFi.localIP());
}
 
int value = 0;
 
void loop() {
  delay(5000);
  ++value;
  int data_length = 10;
  const char* data = "username=zurfyx";
  //Serial.print("connecting to ");
  //Serial.println(host);
  
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 50000;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
  
  // We now create a URI for the request
  
  //Serial.print("Requesting URL: ");
  //Serial.println(url);
  
  // This will send the request to the server
  client.print(String("POST ") + url + " HTTP/1.1" + skpln +
               "Host: " + host + skpln + 
               "Connection: close" + skpln + 
               "Content-Type: application/x-www-form-urlencoded" + skpln +
               "Content-Length:" + data_length + skpln + skpln +
               data);
  delay(500);
  
  // Read all the lines of the reply from server and print them to Serial
  while(client.available()){
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }
  
  Serial.println();
  Serial.println("closing connection");
}