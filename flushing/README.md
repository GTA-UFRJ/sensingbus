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

Step 1) You must install softwares onto the Raspberry Pi that it will act as a access point. Attention: You need Internet connection to do this step:

		sudo update
		sudo apt-get install isc-dhcp-server
		sudo apt-get install hostapd
		
Step 2) Install a iptables manager too:
		
		sudo apt-get install iptables-persistent
		
You have to say "YES" to both configuration screens.

### Set up DHCP Server:

Step 1) Edit the file /etc/dhcp/dhcpd.conf in your favorite text editor. This tutorial is going to use nano as text editor. Run the following command to edit the file:

		sudo nano /etc/dhcp/dhcpd.conf
		
Find the following lines that say:

		option domain-name "example.org";
		option domain-name-servers ns1.example.org, ns2.example.org;
		
Add a "#" in the beginning of the lines to say:

		#option domain-name "example.org";
		#option domain-name-servers ns1.example.org, ns2.example.org;
Find the lines that say:

		# If this DHCP server is the official DHCP server for the local
		# network, the authoritative directive should be uncommented.
		#authoritative;
		
Remove "#" of the word authoritative:

		# If this DHCP server is the official DHCP server for the local
		# network, the authoritative directive should be uncommented.
		authoritative;
		
After it, in the end of the file add the following lines:	

			subnet 192.168.0.0 netmask 255.255.255.0 {
 			  range 192.168.0.10 192.168.0.50;
 			  option broadcast-address 192.168.0.255;
 			  option routers 192.168.0.1;
 			  default-lease-time 600;
 			  max-lease-time 7200;
 			  option domain-name "local";
 			  option domain-name-servers 8.8.8.8, 8.8.4.4;
			}

Step 2) Save this file after this changes:

Step 3)Edit the file /etc/default/isc-dhcp-server in your favorite text editor. This tutorial is going to use nano as text editor. Copy the following lines and paste in the end of file:
	
			INTERFACES="wlan0"
			
### Set up wlan0 for a static IP address: 

Step 1) Turn down the wireless interface. Run the following command:
		
		sudo ifdown wlan0


Step 4.2) Edit the file /etc/network/interfaces in your favorite text editor. This tutorial is going to use nano as text editor. The file must looks like it:

		auto lo
		iface lo inet loopback
		iface eth0 inet dhcp
		allow-hotplug wlan0
		iface wlan0 inet static
		  address 192.168.10.1
		  netmask 255.255.255.0

### Configure Access Point:

Step 1) Create a new file by running the command:
		
		sudo nano /etc/hotsapd/hostapd.conf
Step 2) Paste the following lines in this new file:

		interface=wlan0
		driver=nl80211
		ssid=sense
		country_code=US
		hw_mode=g
		channel=6
		macaddr_acl=0
		auth_algs=1
		ignore_broadcast_ssid=0
		wpa=2
		wpa_passphrase=S3ns1nG_bu5
		wpa_key_mgmt=WPA-PSK
		wpa_pairwise=CCMP
		wpa_group_rekey=86400
		ieee80211n=1
		wme_enabled=1

Step 3) Now you have to say to Raspberry Pi where to find this configuration file. Run that command to edit the file /etc/default/hostapd.

Find the line:
		
		#DAEMON_CONF="" 

Edit it to say :
		
		DAEMON_CONF="/etc/hostapd/hostapd.conf" 
Step 4) Run that command to edit the file /etc/default/hostapd.

Find the line:
		
		DAEMON_CONF= 

Edit it to say :
		
		DAEMON_CONF=/etc/hostapd/hostapd.conf

### Configure Network Address Translation

Step 1) Edit the file /etc/sysctl.conf in your favorite text editor. This tutorial is going to use nano as text editor. Scroll down to the last line of the file and add the following line:

		net.ipv4.ip_forward=1

Step 2) Running the command at the terminal:

		sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

Step 3) Turn up wlan0 interface:
			sudo ifup wlan0

Step 4) Running theses commands at the terminal:
		sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
		sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
		sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
	
### Starting your wireless router:
Step 1) Starting your wireless router, run theses commands :

		sudo service hostapd start
		sudo service isc-dhcp-server start

Step 2) Make it so it runs every time on boot:

		sudo update-rc.d hostapd enable
		sudo update-rc.d isc-dhcp-server enable
### Reboot Raspberry Pi
Step 1) Run the command 
		
		sudo reboot
		
### Test the WiFi connection:



















