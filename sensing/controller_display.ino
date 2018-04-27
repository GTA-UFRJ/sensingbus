/**
*Author: Pedro Henrique Cruz Caminha
*Universidade Federal do Rio de Janeiro
*Departamento de Engenharia Eletrica
*Project: Sensing Bus
*Subject: The sensing layer controller module
*********************************
To be flashed to an Arduino.

This software reads data from the sensors and sends it to the Wireless Interface.

*/

/*** Pinout used on a 8-way cable:
Function      Pin   WireColor
GND           GND   DarkBrown
RainSensor    D6    LightBrown
TempHumSensor D7    LightGreen
WiFiRx        D4    LightBlue
WiFiTx        D5    DarkBlue
Vcc           Vcc   Orange
Light         A3    White
Empty         -     DarkGreen
*** Display ***
SCL (display) A5
SDA (display) A4

The GPS is a shield, not connected through cable.
*/

#include <avr/pgmspace.h>
#include <SoftwareSerial.h>
#include <SD.h>

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#include "TinyGPS++.h"
#include "DHT.h"

#define NODE_ID 1 //The network id of the present device

#define DEBUG true
#define SERIAL_BAUD_RATE 9600

#define GPS_RX 2
#define GPS_TX 3
#define GPS_BAUD_RATE 9600

#define WIFI_TX 4
#define WIFI_RX 5
#define WIFI_BAUD_RATE 38400

#define DHTPIN 7
#define DHTTYPE DHT11

#define REQUEST "?"
#define CLEAR_TO_SEND ":"
#define END_OF_FILE "#"
#define WIFI_FREQ 10
#define WIFI_TIMEOUT 10

#define SEPARATOR ","

#define DELAY_TIME 50

#define PIN_LIGHT A3
#define SD_CHIP_SELECT 10
#define PIN_RAIN A1


const char string_0[] PROGMEM = "A.TXT";
const char string_1[] PROGMEM = "node_id=";
const char string_2[] PROGMEM = "&type=data";
const char string_3[] PROGMEM = "&header=datetime,lat,lng,"; // This string is broken in 2 so the buffer is not very big
const char string_4[] PROGMEM = "light,temperature,humidity,rain";
const char string_5[] PROGMEM = "&load=";


const char* const string_table[] PROGMEM = {string_0, string_1, string_2,
                                            string_3, string_4, string_5
                                           };

const char debug_0[] PROGMEM = "Searching for GPS";
const char debug_1[] PROGMEM = "GPS Found!";
const char debug_2[] PROGMEM = "Asking for wifi";
const char debug_3[] PROGMEM = "Waiting WiFi";
const char debug_4[] PROGMEM = "Sending Data";
const char debug_5[] PROGMEM = "WiFi available";
const char debug_6[] PROGMEM = "File Restarted!";
const char debug_7[] PROGMEM = "DHT failure";
const char debug_8[] PROGMEM = "WiFi not available";
const char debug_9[] PROGMEM = "Data sent";
const char debug_10[] PROGMEM = "Storing info";
const char debug_11[] PROGMEM = "File failure";
const char debug_12[] PROGMEM = "File start failure";
const char debug_13[] PROGMEM = "                ";

const char* const debug_table[] PROGMEM = {debug_0, debug_1, debug_2,
                                           debug_3, debug_4, debug_5,
                                           debug_6, debug_7, debug_8,
                                           debug_9, debug_10, debug_11,
                                           debug_12, debug_13
                                          };


char buffer[40];

//DateTime is in DDMMYYHHMMSSCC format
TinyGPSPlus gps;
DHT dht(DHTPIN, DHTTYPE);

//Start display in address 0x27
LiquidCrystal_I2C lcd(0x3F,2,1,0,4,5,6,7,3, POSITIVE);

int wifi_count = 0;

SoftwareSerial gpsSerial(GPS_RX, GPS_TX);
SoftwareSerial wifiSerial(WIFI_RX, WIFI_TX);

void start_file() {
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
  SD.remove(buffer);
  File data_file = SD.open(buffer, FILE_WRITE);
  data_file.close();
}

void print_debug(int i) {
  lcd.setCursor(0,1);
  strcpy_P(buffer, (char*)pgm_read_word(&(debug_table[13])));
  lcd.print(buffer);
  lcd.setCursor(0,1);
  strcpy_P(buffer, (char*)pgm_read_word(&(debug_table[i])));
  lcd.print(buffer);  
}

void setup() {
  Serial.begin(SERIAL_BAUD_RATE);
  wifiSerial.begin(WIFI_BAUD_RATE);
  gpsSerial.begin(GPS_BAUD_RATE);  // gps begins after wifi because it is used first

  // Start lcd
  lcd.begin (16,2);
  lcd.setBacklight(HIGH);

  pinMode(10, OUTPUT);
  if (!SD.begin(SD_CHIP_SELECT)){
    print_debug(12);
  }

  print_debug(0); //Searching for GPS

  // collecting GPS data
  while (!gps.time.isUpdated()) {
    while (gpsSerial.available()) {
      gps.encode(gpsSerial.read());
    }
  }

  print_debug(1); //GPS Found!
}

void start_message() {
  //Create the message
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

void send_data() {
  print_debug(4);

  //Send the whole file
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
  File data_file = SD.open(buffer);
  String a;
  int i = 0;

  while (data_file.available()) {
    start_message();
    while (data_file.available()) {
      i++;
      a = data_file.readStringUntil('\n');
      wifiSerial.print(a + "\n");
      delay(5);
      if (i > 20) {
        wifiSerial.write(END_OF_FILE);
        start_message();
      }
    }
    delay(DELAY_TIME);
    if (!start_connection()){
      break;
    }
  }
  wifiSerial.write(END_OF_FILE);
  data_file.close();

  //Remove the file and create a new
  start_file();

  print_debug(9);
}

bool start_connection() {
  // Check for connection
  wifiSerial.listen();
  wifiSerial.print(REQUEST);
  int index = 0;
  while (!wifiSerial.available() || !wifiSerial.isListening()) {
    print_debug(3); //Waiting WiFi
    index++;
    if (index > WIFI_TIMEOUT)
      break;
    delay(DELAY_TIME);
  }

  String wifiIn("");
  while (wifiSerial.available()) {
    delay(DELAY_TIME);
    wifiIn += String(char (wifiSerial.read()));
  }
  return (wifiIn == CLEAR_TO_SEND);
}

void loop() {
  wifi_count++;
  if (wifi_count > WIFI_FREQ) {
    wifi_count = 0;
    print_debug(2); //Asking for WiFi
    if (start_connection()) {
      send_data();
      print_debug(5); //WiFi available
    } else {
      print_debug(8); //WiFi not available
    }
  }

  // collecting GPS data
  gpsSerial.listen();
  while (!gps.time.isUpdated()) {
    while (gpsSerial.available()) {
      gps.encode(gpsSerial.read());
    }
  }

  if (isnan(dht.readTemperature()) || isnan(dht.readHumidity()) ) {
    print_debug(7); //DHT failure
  }

  // separating GPS data
  if (gps.time.isUpdated()) {
    //print_debug(1); //GPS Found!

    lcd.setCursor(0,0);
    strcpy_P(buffer, (char*)pgm_read_word(&(debug_table[13])));
    lcd.print(buffer);
    lcd.setCursor(0,0);  
    lcd.print(String(analogRead(PIN_LIGHT)) + SEPARATOR +
              String(dht.readTemperature(),0) + "C" + SEPARATOR +
              String(dht.readHumidity(),0) + "%" + SEPARATOR +
              String(analogRead(PIN_RAIN)));
    //Serial.println("DAte:" + String(gps.date.value()) +","+ String(gps.time.value()));
    String data_string = String(gps.date.value()) + String(gps.time.value()) + SEPARATOR +
      String(gps.location.lat(), 5) + SEPARATOR +
      String(gps.location.lng(), 5) + SEPARATOR +
      String(analogRead(PIN_LIGHT)) + SEPARATOR +
      String(dht.readTemperature()) + SEPARATOR +
      String(dht.readHumidity()) + SEPARATOR +
      String(analogRead(PIN_RAIN)) +
      "\n";
    strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
    File data_file = SD.open(buffer, FILE_WRITE);
    if (data_file) {
      data_file.print(data_string);
      Serial.print(data_string);
       print_debug(10); //Printing file
      data_file.close();
    }else {
        print_debug(11); //File failure
     }
  }
}
