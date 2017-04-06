/**
*Author: Pedro Henrique Cruz Caminha
*Universidade Federal do Rio de Janeiro
*Departamento de Engenharia Eletrica
*Project: Sensing Bus
*Subject: Throughput tests with an ESP8266
*********************************
To be flashed to an ESP8266.

This software sends data to a flushing node.

The Controller must be flashed with sensing/tests/throughput_with_HTTP.ino.
*/
#include <ESP8266WiFi.h>

const char* ssid     = "<ssid>";  //replace with the ssid of the network
const char* password = "<password>";  //replace this with the password of the network
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
          client.print(dataString);
        }
      } else {
        Serial.write(wait_to_send);
      }
    }
  }
}
