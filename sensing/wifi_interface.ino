#include <ESP8266WiFi.h>

PROGMEM const char post_line[] = "POST 192.168.0.1 HTTP/1.1 \nHost: 192.168.0.1 \nConnection: close \nContent-Type: application/x-www-form-urlencoded \nContent-Length:";

const char* ssid     = "sense";
const char* password = "S3ns1nG_bu5";
const char* host = "192.168.0.1";
const int httpPort = 50000;
const char* skpln = "\r\n";
const String request = "?";
const char* clear_to_send = ":";
const char* wait_to_send = "!";
const String end_of_file = "#";
String url = "/";

void setup() {
  Serial.begin(38400);
  pinMode(2, OUTPUT);

  // We start by connecting to a WiFi network
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void loop() {
  delay(500);
  bool connected = false;
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  if (!client.connect(host, httpPort)) {
    connected = false;
  } else {
    connected = true;
  }

  // Wait for data input
  char a;
  while (Serial.available()) {
    a = Serial.read();
    if (String(a) == request) {
      if (connected) {
        delay(50); // Delay problem
        String temp = "";
        String dataString = "";
        Serial.write(clear_to_send);
        while (!Serial.available()) {}
        // Receive data from serial
        while (true) {
          if (Serial.available()) {
            temp = String(char(Serial.read()));
            if (temp == request) {
              Serial.write(clear_to_send);
            }
            if (temp == end_of_file) {
              break;
            }
            dataString += temp;
          }
        }
        if (dataString.length() > 0) {
          // This will send the request to the server
          client.print(String(FPSTR(post_line)) + dataString.length() + "\n\n" + dataString);
        }
      } else {
        Serial.write(wait_to_send);
      }
    }
  }
}