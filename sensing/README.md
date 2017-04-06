# SensingBus Sensing Node

This is the installation manual of a SensingBus sensing node.

The required equipment is:

| Module                 | Device         | Manufacturer    |
|------------------------|----------------|-----------------|
| Controller             | Arduino UNO R3 | Arduino         |
| GNSS Receiver          | GS-96U7        | Guangzhou Xintu |
| SD Card Interface      | GS-96U7        | Guangzhou Xintu |
| Wireless Interface     | ESP8266        | Espressif       |

The following sensors are present on the sensor bank:

| Sensor                 | Device         | Manufacturer    |
|------------------------|----------------|-----------------|
| Humidity               | DHT11          | DFRobot         |
| Temperature            | DHT11          | DFRobot         |
| Light Intensity        | GL5528         | GBK Robotics    |
| Rain Intensity         | YL-38          | 100y            |


The connections of components to the Controller are:

| Arduino port   | Device             | Device port |
|----------------|--------------------|-------------|
| D2             | GNSS Module        | Tx          |
| D3             | GNSS Module        | Rx          |
| D4             | Wireless Interface | Rx          |
| D5             | Wireless Interface | Tx          |
| D7             | Temperature sensor | -           |
| D10            | Memmory Unit       | Chip select |
| A1             | Rain sensor        | -           |
| A1             | Luminosity sensor  | -           |


Change the source /sensing_bus/sensing/wifi_interface.ino to have the ssid and password of the network to be used to communicate with the Flushing layer.

Flash the Controller with the source in /sensing_bus/sensing/controller.ino and the Wireless Interface with /sensing_bus/sensing/wifi_interface.ino.

The code in /sensing_bus/sensing/controller.ino has debug messages that can be accessed by the Arduino's serial ports (D0 and D1). These mesages can help the testing of the code.
