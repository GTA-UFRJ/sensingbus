#include <ESP8266WiFi.h>
 
const char* ssid     = "sense";
const char* password = "S3ns1nG_bu5"; 
const char* host = "146.164.69.186";
const int httpPort = 50000;
const char* skpln = "\r\n";
const char* request = "?";
const char* clear_to_send = ":";
const char* wait_to_send = "!";
String url = "/";
 
void setup() {
  Serial.begin(9600);
  delay(100);
 
  // We start by connecting to a WiFi network
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    //Serial.println("Searching WiFi");
  }
}

void loop() {
  delay(500);
  bool connected = false;
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  
  if (!client.connect(host, httpPort)) {
    connected=false;
  } else {
    connected = true;
  }

  char a;
  while(Serial.available()){
    a = Serial.read();
    if (String(a) == String(request)){
      if(connected){
        Serial.write(clear_to_send);

        while(!Serial.available()){}
         // Receive data from serial
        char index = 0;
        char temp = 0;
        String dataString = "";
        while(Serial.available()){
          delay(100);
          temp = Serial.read();
          dataString += String(temp);
          index++;
        }
        if (dataString.length() > 0){
        // This will send the request to the server
        client.print(String("POST ") + url + " HTTP/1.1" + skpln +
                     "Host: " + host + skpln + 
                     "Connection: close" + skpln + 
                     "Content-Type: application/x-www-form-urlencoded" + skpln +
                     "Content-Length:" + dataString.length() + skpln + skpln +
                     dataString);
        }    
      }else{
        Serial.write(wait_to_send);
      }
    }
  }

  // Read all the lines of the reply from server and print them to Serial
  /*while(client.available()){
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }
  
  Serial.println();
  Serial.println("closing connection");*/
}