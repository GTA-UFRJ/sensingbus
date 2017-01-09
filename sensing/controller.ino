//Code: GPS Logger
//Changes : PEDROCRUZ

#include <avr/pgmspace.h>
#include <SoftwareSerial.h>
#include <SD.h>

#include "TinyGPS++.h"
#include "dht.h"

#define DEBUG true
#define SERIAL_BAUD_RATE 9600

#define GPS_RX 2
#define GPS_TX 3
#define GPS_BAUD_RATE 9600

#define WIFI_TX 4
#define WIFI_RX 5
#define WIFI_BAUD_RATE 38400

#define DHT11_PIN 5
//This is the network id of the present device
#define NODE_ID 1

const char* request = "?";
const char* clear_to_send = ":";
const char* wait_to_send = "!";
const char* end_of_file = "#";
const int wifi_freq = 10;
const int wifi_timeout = 10000;

const char string_0[] PROGMEM = "log.txt";
const char string_1[] PROGMEM = "datetime,lat,lng,light,temperature,humidity,pollution,rain";
const char string_2[] PROGMEM = ";";
const char string_3[] PROGMEM = "node_id=";
const char string_4[] PROGMEM = "&type=data";
const char string_5[] PROGMEM = "&header=datetime,lat,lng,light,temperature,humidity,pollution,rain";
const char string_6[] PROGMEM = "&load=";


const char* const string_table[] PROGMEM = {string_0, string_1, string_2, string_3,
                                            string_4, string_5, string_6};

#if DEBUG
const char debug_0[] PROGMEM = "Searching for GPS";
const char debug_1[] PROGMEM = "GPS Found!";
const char debug_2[] PROGMEM = "Asking for wifi";
const char debug_3[] PROGMEM = "Waiting WiFi";
const char debug_4[] PROGMEM = "Sending Data";
const char debug_5[] PROGMEM = "WiFi available";
const char debug_6[] PROGMEM = "File Restarted!";

const char* const debug_table[] PROGMEM = {debug_0, debug_1, debug_2, debug_3, debug_4, debug_5, debug_6};
#endif

char buffer[70];

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
int iteration = 0;

SoftwareSerial gpsSerial(GPS_RX, GPS_TX);
SoftwareSerial wifiSerial(WIFI_RX, WIFI_TX);

void start_file(){
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
  SD.remove(buffer);
  if(SD.begin(SDChipSelect)){
    strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
    File data_file = SD.open(buffer, FILE_WRITE);
    data_file.close();
  }
}

void print_debug(int i){
  strcpy_P(buffer, (char*)pgm_read_word(&(debug_table[i])));
  Serial.println(buffer);
}

void setup(){
    Serial.begin(SERIAL_BAUD_RATE); 
    wifiSerial.begin(WIFI_BAUD_RATE);
    gpsSerial.begin(GPS_BAUD_RATE);  // gps begins after wifi because it is used first
    
    pinMode(10, OUTPUT);
    
    start_file();
    delay(delay_time);

    #if DEBUG
    print_debug(0); //Searching for GPS
    #endif
    
    // collecting GPS data
    /*while (!gps.time.isUpdated()){      
      while(gpsSerial.available()){
          gps.encode(gpsSerial.read());
      }
    }*/

    #if DEBUG
    print_debug(1); //GPS Found!
    #endif

}

void send_data(){
  #if DEBUG
  print_debug(4);
  #endif
  
  //Create the message
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[3]))); //node_id=
  wifiSerial.print(String(buffer) + NODE_ID);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[4]))); //&type=data
  wifiSerial.print(buffer);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[5]))); //&header=datetime,lat,lng,light,temperature,humidity,pollution,rain
  wifiSerial.print(buffer);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[6]))); //&load=
  wifiSerial.print(buffer);

  //Send the whole file
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
  File data_file = SD.open(buffer);
  char a;
  while (data_file.available()) {
      a = char(data_file.read());
      wifiSerial.write(a);
      delay(5);
      Serial.write(a);
  }
  wifiSerial.write(end_of_file);
  data_file.close();
  
  //Remove the file and create a new
  start_file();
}

void loop(){
    iteration++;

    if (iteration % wifi_freq == 0){
      // Check for connection
      char index = 0;
      String dataString = "";
      #if DEBUG
      print_debug(2); //Asking for WiFi
      #endif
      
      wifiSerial.listen();
      wifiSerial.print(request);
      
      #if DEBUG
      print_debug(2); //Asking for WiFi
      #endif
  
      int timeout = 0;
      while(!wifiSerial.available()){
        timeout++;
        if (timeout > wifi_timeout)
          break;
        delay(10);  
        #if DEBUG
        //print_debug(3); //Waiting WiFi
        #endif
      }

      #if DEBUG
      if(wifiSerial.available()){
        print_debug(5); //WiFi available
      }
      #endif
      
      while(wifiSerial.available()){
        delay(100);
          dataString += String(char (wifiSerial.read()));
          index++;
          if(index>200)
              break;
      }
      Serial.println(dataString);
      if (dataString == clear_to_send){
        send_data();
      }
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
        String data_string = //String(iteration) + separator +
                             String(gps.date.value()) + String(gps.time.value()) + separator +
                             String(gps.location.lat(),10) + separator +
                             String(gps.location.lng(),10) + separator +
                             String(analogRead(pinLight)) + separator +
                             String(DHT.temperature) + separator +
                             String(DHT.humidity) + separator +
                             String(analogRead(pinPollution)) + separator +
                             String(digitalRead(pinRain)) +
                             "\n";
        strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
        File data_file = SD.open(buffer, FILE_WRITE);
        if(data_file){
            data_file.print(data_string);
            data_file.close();
        }        
        //delay(delay_time);   
    }

}