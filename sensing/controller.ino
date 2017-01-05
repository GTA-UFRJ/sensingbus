//Code: GPS Logger
//Changes : PEDROCRUZ

#include <avr/pgmspace.h>
#include <SoftwareSerial.h>
#include <SD.h>

#include "TinyGPS++.h"
#include "dht.h"

#define SERIAL_BAUD_RATE 9600

#define GPS_RX 2
#define GPS_TX 3
#define GPS_BAUD_RATE 9600

#define WIFI_TX 4
#define WIFI_RX 5
#define WIFI_BAUD_RATE 9600

#define DHT11_PIN 5
//This is the network id of the present device
#define NODE_ID 1

const char string_0[] PROGMEM = "log.txt";
const char string_1[] PROGMEM = "datetime,lat,lng,light,temperature,humidity,pollution,rain";
const char string_2[] PROGMEM = ";";
const char string_3[] PROGMEM = "ready";
const char string_4[] PROGMEM = "node_id=";
const char string_5[] PROGMEM = "&type=data";
const char string_6[] PROGMEM = "&header=datetime,lat,lng,light,temperature,humidity,pollution,rain";
const char string_7[] PROGMEM = "&load=";
const char string_8[] PROGMEM = "Searching for GPS";
const char string_9[] PROGMEM = "GPS Found!";

const char* const string_table[] PROGMEM = {string_0, string_1, string_2, string_3, 
                                            string_4, string_5, string_6, string_7,
                                            string_8, string_9};

char buffer[60];

//DateTime is in DDMMYYHHMMSSCC format
TinyGPSPlus gps;
dht DHT;

const char* separator = ",";

const int delay_time = 500;

const int pinLight = A1;
const int pinPollution = 8;
const int pinRain = 3;

const int SDChipSelect = 10;

String dateTime;

SoftwareSerial gpsSerial(GPS_RX, GPS_TX);
SoftwareSerial wifiSerial(WIFI_RX, WIFI_TX);

void start_file(){
  if(SD.begin(SDChipSelect)){
    strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
    File data_file = SD.open(buffer, FILE_WRITE);
    data_file.close();
  }
}

void setup(){
    Serial.begin(SERIAL_BAUD_RATE); 
    wifiSerial.begin(WIFI_BAUD_RATE);
    gpsSerial.begin(GPS_BAUD_RATE);  // gps begins after wifi because it is used first
    
    pinMode(10, OUTPUT);
    
    start_file();
    delay(delay_time);

    strcpy_P(buffer, (char*)pgm_read_word(&(string_table[8])));
    Serial.println(buffer);
    // collecting GPS data
    while (!gps.time.isUpdated()){      
      while(gpsSerial.available()){
          gps.encode(gpsSerial.read());
      }
    }
    strcpy_P(buffer, (char*)pgm_read_word(&(string_table[9])));
    Serial.println(buffer);
    gpsSerial.end(); 
}

void send_data(){
  Serial.println("Sending data");
  //Create the message
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[4])));
  wifiSerial.println(String(buffer) + NODE_ID);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[5])));
  wifiSerial.println(buffer);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[6])));
  wifiSerial.println(buffer);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[6])));
  wifiSerial.println(buffer);

  //Send the whole file
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
  File data_file = SD.open(buffer);
  while (data_file.available()) {
      wifiSerial.write(data_file.read());
  }
  data_file.close();
  
  //Remove the file and create a new
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
  SD.remove(buffer);
  start_file();
}

void loop(){
    // Check for connection
    char index = 0;
    String dataString = "";
    wifiSerial.listen();
    wifiSerial.print("r");
    while(!wifiSerial.available()){}
    
    while(wifiSerial.available()){
      delay(100);
        dataString += String(char (wifiSerial.read()));
        index++;
        if(index>200)
            break;
    }
    Serial.println(dataString);
    strcpy_P(buffer, (char*)pgm_read_word(&(string_table[3])));
    if (dataString == buffer){
      send_data();
    }

    // collecting GPS data
    gpsSerial.listen();
    while (!gps.time.isUpdated()){      
      while(gpsSerial.available()){
          gps.encode(gpsSerial.read());
      }
    }
    // separating GPS data
    if (gps.time.isUpdated()){
        int chk = DHT.read11(DHT11_PIN);
        String data_string = String(gps.date.value()) +
                             String(gps.time.value()) + separator +
                             String(gps.location.lat(),10) + separator +
                             String(gps.location.lng(),10) + separator +
                             String(analogRead(pinLight)) + separator +
                             String(DHT.temperature) + separator +
                             String(DHT.humidity) + separator +
                             String(analogRead(pinPollution)) + separator +
                             String(digitalRead(pinRain)) +
                             "\n";
        Serial.print(data_string);
        strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
        File data_file = SD.open(buffer, FILE_WRITE);
        if(data_file){
            data_file.print(data_string);
            data_file.close();
        }        
        delay(delay_time);   
    }

}