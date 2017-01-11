# sensing_bus
Urban Sensing Through Bus-Based Mobility

This project is a bus-based sensing platform for Smart Cities. In a broader view, sensor nodes, embbeded onto buses, gather data about the city. Such data is delivered to users using access points mounted into the bus stops of the city. Data is presented to users using a cloud service. The whole schema is shown below: 

<img src="img/bus_distribution.png" alt="System layers" width="20%" height="20%" align="middle"/>

It is abstracted in three layers: sensing, flushing, and publishing. These layers are mapped into the architecture of the current project.

## Architecture
This project has three main components, as shown:

<img src="img/layers.png" alt="System layers" width="20%" height="20%" align="middle"/>

The Sensing layer is responsible for gathering raw data from the city. It is composed by wireless sensor nodes embbeded onto urban buses of public transportation.

The Flushing layer receives raw data directly from the Sensing layer and sends it to the Publishing layer, through the Internet. It is composed by access points, mounted on bus stops.

The Publishing layer receives data from all the nodes in the Flushing layer and serves data to the users, using an API and a web interface. This layer is composed by a server running on a distributed cloud.

Each component is explained in detail throughout the next sections

## Sensing layer
The Sensing layer is a mobile wireless sensor network that gathers data from the city, using buses as mobility platform. Every node in this network is capable of gathering data, storing it and send it to the Flushing layer.

## The Sensing Node

The sensing 
Technology: Arduino + ESP8266

## The Flushing Node
Technology: Raspberry Pi

## The Publishing Node
Technology: Django

## References
- http://www.gta.ufrj.br/ftp/gta/TechReports/CPCC16.pdf
