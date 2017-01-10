//Code: GPS Logger
//Changes : PEDROCRUZ


// Não está confirmado:
// Função         GND         Chuva     vazio       TMP       CL        DA      Vcc    Luz
// Cor do fio  marrom  marrom claro  verde esc verde cla azul esc  azul cla  laranja branco
// Arduino                    3                         5      SCL      SDA               A3
//Função          COR Arduino
//GND   marrom escuro     GND
//Chuva  marrom claro      D6
//Vazio  verde escuro       -
//Temp    verde claro      D7
//CL      azul escuro     SCL
//DA       azul claro     SDA
//Vcc         laranja     Vcc
//Luz          branco      A3

#include <avr/pgmspace.h>
#include <SoftwareSerial.h>
#include <SD.h>

#include "TinyGPS++.h"
#include "DHT.h"

#define DEBUG true
#define SERIAL_BAUD_RATE 9600

#define GPS_RX 2
#define GPS_TX 3
#define GPS_BAUD_RATE 9600

#define WIFI_TX 4
#define WIFI_RX 5
#define WIFI_BAUD_RATE 57600

#define DHT11_PIN 7
#define DHTPIN 7
#define DHTTYPE DHT11

//This is the network id of the present device
#define NODE_ID 1

#define request "?"
#define clear_to_send ":"
#define end_of_file "#"
#define wifi_freq 10
#define wifi_timeout 100

#define SEPARATOR ","

#define DELAY_TIME 500

#define PIN_LIGHT A1
#define SD_CHIP_SELECT 10
#define PIN_RAIN 3


const char string_0[] PROGMEM = "log.txt";
const char string_1[] PROGMEM = "node_id=";
const char string_2[] PROGMEM = "&type=data";
const char string_3[] PROGMEM = "&header=datetime,lat,lng,light,temperature,humidity,rain";
const char string_4[] PROGMEM = "&load=";


const char* const string_table[] PROGMEM = {string_0, string_1, string_2,
                                            string_3, string_4
                                           };

#if DEBUG
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

const char* const debug_table[] PROGMEM = {debug_0, debug_1, debug_2,
                                           debug_3, debug_4, debug_5,
                                           debug_6, debug_7, debug_8,
                                           debug_9
                                          };
#endif

char buffer[65];

//DateTime is in DDMMYYHHMMSSCC format
TinyGPSPlus gps;
DHT dht(DHTPIN, DHTTYPE);

int iteration = 0;

SoftwareSerial gpsSerial(GPS_RX, GPS_TX);
SoftwareSerial wifiSerial(WIFI_RX, WIFI_TX);

void start_file() {
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
  SD.remove(buffer);
  if (SD.begin(SD_CHIP_SELECT)) {
    strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
    File data_file = SD.open(buffer, FILE_WRITE);
    data_file.close();
  }
}

#if DEBUG
void print_debug(int i) {
  strcpy_P(buffer, (char*)pgm_read_word(&(debug_table[i])));
  Serial.println(buffer);
}
#endif

void setup() {
  Serial.begin(SERIAL_BAUD_RATE);
  wifiSerial.begin(WIFI_BAUD_RATE);
  gpsSerial.begin(GPS_BAUD_RATE);  // gps begins after wifi because it is used first
  //dht.begin();

  pinMode(10, OUTPUT);

  start_file();
  delay(DELAY_TIME);

#if DEBUG
  print_debug(0); //Searching for GPS
#endif

  // collecting GPS data
  while (!gps.time.isUpdated()) {
    while (gpsSerial.available()) {
      gps.encode(gpsSerial.read());
    }
  }

#if DEBUG
  print_debug(1); //GPS Found!
#endif
}

void send_data() {
#if DEBUG
  print_debug(4);
#endif

  //Create the message
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[1]))); //node_id=
  wifiSerial.print(String(buffer) + NODE_ID);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[2]))); //&type=data
  wifiSerial.print(buffer);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[3]))); //&header=datetime,lat,lng,light,temperature,humidity,rain
  wifiSerial.print(buffer);

  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[4]))); //&load=
  wifiSerial.print(buffer);

  //Send the whole file
  strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
  File data_file = SD.open(buffer);
  char a;
  while (data_file.available()) {
    a = char(data_file.read());
    wifiSerial.write(a);
    delay(5);
    //Serial.write(a);
  }
  wifiSerial.write(end_of_file);
  data_file.close();

  //Remove the file and create a new
  start_file();

#if DEBUG
  print_debug(9);
#endif
}

void loop() {

  iteration++;
  if (iteration % wifi_freq == 0) {

#if DEBUG
    print_debug(2); //Asking for WiFi
#endif

    // Check for connection
    wifiSerial.listen();
    wifiSerial.print(request);
    int index = 0;
    while (!wifiSerial.available() || !wifiSerial.isListening()) {
      Serial.println("Waiting WiFi");
      index++;
      if (index > wifi_timeout)
        break;
      delay(100);
    }

#if DEBUG
    if (wifiSerial.available()) {
      print_debug(5); //WiFi available
    } else {
      print_debug(8); //WiFi not available
    }
#endif
    String wifiIn("");
    while (wifiSerial.available()) {
      delay(100);
      wifiIn += String(char (wifiSerial.read()));
    }
    if (wifiIn == clear_to_send) {
      send_data();
    }
  }

  // collecting GPS data
  gpsSerial.listen();
  while (!gps.time.isUpdated()) {
    while (gpsSerial.available()) {
      gps.encode(gpsSerial.read());
    }
  }

#if DEBUG
  if (isnan(dht.readTemperature()) || isnan(dht.readHumidity()) ) {
    print_debug(7); //DHT failure
  }
#endif

  // separating GPS data
  if (gps.time.isUpdated()) {
#if DEBUG
    print_debug(1); //GPS Found!
#endif

    String data_string = //String(iteration) + SEPARATOR +
      String(gps.date.value()) + String(gps.time.value()) + SEPARATOR +
      String(gps.location.lat(), 10) + SEPARATOR +
      String(gps.location.lng(), 10) + SEPARATOR +
      String(analogRead(PIN_LIGHT)) + SEPARATOR +
      String(dht.readTemperature()) + SEPARATOR +
      String(dht.readHumidity()) + SEPARATOR +
      String(digitalRead(PIN_RAIN)) +
      "\n";
    strcpy_P(buffer, (char*)pgm_read_word(&(string_table[0])));
    File data_file = SD.open(buffer, FILE_WRITE);
    if (data_file) {
      data_file.print(data_string);
      data_file.close();
    }
  }
}