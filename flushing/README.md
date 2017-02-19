# Sensing Bus Flusher
This tutorial followed this link's one: https://cdn-learn.adafruit.com/downloads/pdf/setting-up-a-raspberry-pi-as-a-wifi-access-point.pdf. The main tutorial's objetive is allowed any users can build a flusher node without any problem at all. 

## Required Equipments:
You will need some equipment to build a Flusher Node:
* Raspberry Pi;
* Ethernet Cable;
* A WIFI adapter;
* SD Card;
* SD Card Reader.
## Preparation:
Step 1) You must download some Operatig System. In this tutorial, Raspdian was chosen as OS. You must download it in the following link. 

		https://www.raspberrypi.org/downloads/raspbian/
		
Step 2) Boot the OS into SD Card. Run the following command:

		sudo gzip -dc /home/your_username/image.gz | dd bs=4M of=/dev/sdb
		
Step 3) Connect the Ethernet Cable on Raspberry:

Step 4) Check the Internet connection. Run the command.

		ping 8.8.8.8
		
Step 5) Set up WiFi dongle:
Connect WiFi dongle and restart Raspberry Pi, running the command
		
		sudo reboot
	
	
Now, you can see wlan0 interface after you run the following:
	
		ifconfig -a
		
## Turn Raspberry Pi into a Hotspot:
### Install the softwares:

Step 1) Install the DHCP Server Software:

	sudo apt-get install isc-dhcp-server

Step 2) Configure the isc-dhcp-server:

	Step 2.1) Edit the file /etc/dhcp/dhcpd.conf in your favorite text editor. This tutorial is going to use nano as text editor. Un-comment the word "authoritative":
	Step 2.2) Copy the following lines and paste in the end of file:
	

			subnet 192.168.10.0 netmask 255.255.255.0 {
 			  range 192.168.10.10 192.168.10.20;
 			  option broadcast-address 192.168.10.255;
 			  option routers 192.168.10.1;
 			  default-lease-time 600;
 			  max-lease-time 7200;
 			  option domain-name "local-network";
 			  option domain-name-servers 8.8.8.8, 8.8.4.4;
			}

	Step 2.3) Save this file after this changes:

Step 3)Edit the file /etc/default/isc-dhcp-server in your favorite text editor. This tutorial is going to use nano as text editor. Copy the following lines and paste in the end of file:
		INTERFACES="wlan0"

Step 4) Configure a static ip address for the wireless network:

	Step 4.1) Turn down the wireless interface. Run the following command:
		
		sudo ifdown wlan0


	Step 4.2) Edit the file /etc/network/interfaces in your favorite text editor. This tutorial is going to use nano as text editor. The mus looks like it:

		auto lo
		iface lo inet loopback
		iface eth0 inet dhcp
		allow-hotplug wlan0
		iface wlan0 inet static
		  address 192.168.10.1
		  netmask 255.255.255.0

Step 5) Configuring HostAPD:
 
	Step 5.1) Edit the file /etc/sysctl.conf in your favorite text editor. This tutorial is going to use nano as text editor. Scroll down to the last line of the file and add the following line:

		net.ipv4.ip_forward=1

	Step 5.1) Running the command at the terminal:

		sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

	Step 5.3) Turn up wlan0 interface:
			sudo ifup wlan0

	Step 5.4) Running theses commands at the terminal:
		sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
		sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
		sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
	

Step 6) Starting your wireless router, run theses commands :

		sudo service isc-dhcp-server start
		sudo service hostapd start

Step 7) Reboot Raspberry Pi:

		sudo reboot


















