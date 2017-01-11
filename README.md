# sensing_bus
Urban Sensing Through Bus-Based Mobility

This project is a bus-based sensing platform for Smart Cities. It is abstracted in three layers: sensing, flushing, and publishing. These layers are mapped into the architecture of the current project.

## Architecture
This project has three main components, as shown:
<img src="img/layers.png" alt="System layers" width="20%" height="20%"/>

The Sensing layer is responsible for gathering raw data from the city. It is composed by wireless sensor nodes embbeded onto urban buses of public transportation.

The Flushing layer receives raw data directly from the Sensing layer and sends it to the Publishing layer, through the Internet. It is composed by access points, mounted on bus stops.

The Publishing layer receives data from all the nodes in the Flushing layer and serves data to the users, using an API and a web interface. This layer is composed by a server running on a distributed cloud.

Each component is explained in detail throughout the next sections
## The Sensing Node
Technology: Arduino + ESP8266

## The Flushing Node
Technology: Raspberry Pi

## The Publishing Node
Technology: Django

## References
- http://www.gta.ufrj.br/ftp/gta/TechReports/CPCC16.pdf
