/**
*Author: Pedro Henrique Cruz Caminha
*Universidade Federal do Rio de Janeiro
*Departamento de Engenharia Eletrica
*Project: Sensing Bus
*Subject: Throughput tests with an arduino
*********************************
To be flashed on an Arduino.

This software creates a file on the SD card. After, it reads the memmory card and asks the ESP8266 to send it.

The ESP8266 must be flashed with sensing/ESP_no_HTTP.ino.
*/
#include <avr/pgmspace.h>
#include <SoftwareSerial.h>
#include <SD.h>

#define NODE_ID 1 //The network id of the present device

#define DEBUG false // Set true if 
#define SERIAL_BAUD_RATE 9600

#define GPS_RX 2
#define GPS_TX 3
#define GPS_BAUD_RATE 9600

#define WIFI_TX 4
#define WIFI_RX 5
#define WIFI_BAUD_RATE 38400

#define request "?"
#define clear_to_send ":"
#define end_of_file "#"
#define wifi_freq 10
#define wifi_timeout 20

#define BATCH_SIZE 5

#define DELAY_TIME 150

#define SD_CHIP_SELECT 10

#define HEADER_SIZE 82

const char string_0[] PROGMEM = "log.txt";
const char string_1[] PROGMEM = "\n\nnode_id=";
const char string_2[] PROGMEM = "&type=data";
const char string_3[] PROGMEM = "&header=datetime,lat,lng,"; // This string is broken in 2 so the buffer is not very big
const char string_4[] PROGMEM = "light,temperature,humidity,rain";
const char string_5[] PROGMEM = "&load=";
const char string_6[] PROGMEM = "POST 192.168.0.1 HTTP/1.1";
const char string_7[] PROGMEM = " \nHost: 192.168.0.1 ";
const char string_8[] PROGMEM = "\nConnection: keep-alive ";
const char string_9[] PROGMEM = "\nContent-Type: application/x-www";
const char string_10[] PROGMEM = "-form-urlencoded \nContent-Length: ";



const char* const string_table[] PROGMEM = {string_0, string_1, string_2,
                                            string_3, string_4, string_5,
                                            string_6, string_7, string_8,
                                            string_9, string_10
                                           };

char buffer[40];
SoftwareSerial wifiSerial(WIFI_RX, WIFI_TX);
String filename("log.txt");
unsigned long filesize;

void start_file() {
  if (SD.begin(SD_CHIP_SELECT)) {
    SD.remove(filename);
    File data_file = SD.open(filename, FILE_WRITE);
    
    for (int i = 0; i < 200; i ++) {
      data_file.print(String(i) + ",aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n");
    }
    data_file.close();
    data_file = SD.open(filename, FILE_WRITE);
    filesize = data_file.size();
    Serial.println("File size = " + String(filesize) + "bytes");
  }
}


void start_message(int content_length) {
  //Create the http header
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[6]))); //POST 192.168.0.1 HTTP/1.1
  wifiSerial.print(String(buffer));

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[7]))); // \nHost: 192.168.0.1 
  wifiSerial.print(String(buffer));
  
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[8]))); //\nConnection: keep-alive 
  wifiSerial.print(String(buffer));
  
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[9]))); //\nContent-Type: application/x-www
  wifiSerial.print(String(buffer));
  
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[10]))); //-form-urlencoded \nContent-Length:
  wifiSerial.print(String(buffer) + content_length);

  //Create the data message
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[1]))); //node_id=
  wifiSerial.print(String(buffer) + NODE_ID);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[2]))); //&type=data
  wifiSerial.print(buffer);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[3]))); //&header=datetime,lat,lng,
  wifiSerial.print(buffer);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[4]))); //light,temperature,humidity,rain
  wifiSerial.print(buffer);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[5]))); //&load=
  wifiSerial.print(buffer);
}

bool send_data() {
  wifiSerial.listen();
  while (!wifiSerial.isListening()) {}
  //Send the whole file
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
  File data_file = SD.open("log.txt");
  
  while (data_file.available()) {
    if(!start_connection()){
      break;
    }
    String a;
    int i = 0;
    while (data_file.available() and i < BATCH_SIZE) {      
      i++;
      a += data_file.readStringUntil('\n') + "\n";
      
    }
    start_message(a.length() + HEADER_SIZE);
    wifiSerial.print(a);
    wifiSerial.write(end_of_file);
    delay(500);
  }
  data_file.close();
}

bool start_connection() {
  // Check for connection
  wifiSerial.listen();
  while (!wifiSerial.isListening()) {}
  wifiSerial.print(request);
  int index = 0;
  while (!wifiSerial.available()) {
#if DEBUG
    print_debug(3);
#endif
    index++;
    if (index > wifi_timeout)
      break;
    delay(5);
  }

  String wifiIn("");
  while (wifiSerial.available()) {
    delay(DELAY_TIME);
    wifiIn += String(char (wifiSerial.read()));
  }
  return (wifiIn == clear_to_send);
}
void setup() {
  Serial.begin(SERIAL_BAUD_RATE);
  wifiSerial.begin(WIFI_BAUD_RATE);

  pinMode(10, OUTPUT);
  Serial.println("Start");
  start_file();
  Serial.println("File started");
  delay(DELAY_TIME);

}

void loop() {
  unsigned long t_start = millis();
  send_data();
  unsigned long t_end = millis();
  float elapsed = (t_end - t_start)/1000.0;
  Serial.println("Elapsed seconds = " + String(elapsed));
  float throughput = float(filesize)/elapsed;
  Serial.println("Throughput = " + String(throughput));
}
