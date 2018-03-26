# SensingBus Flushing Node
 The main tutorial's objetive is to allow any users can build a flusher node without any problem at all. 

## Installation Guide

### Required Equipments:
Equipment needed to build a flusher node:
* Raspberry Pi;
* Ethernet Cable;
* A WIFI adapter;
* SD Card;
* SD Card Reader.
### Preparation:

Download the flushing image from this [link](http://gloria.gta.ufrj.br/vm-templates/SensingBusOS.gz) or follow the steps bellow. To install the image on raspberry, follow [these](https://www.raspberrypi.org/documentation/installation/installing-images/) instructions.

Step 1) Download some Operational System. In this tutorial, Raspdian was chosen as OS. Download it in the following link. 

		https://www.raspberrypi.org/downloads/raspbian/
		
Step 2) Boot the OS into SD Card. Run the following command:

		sudo gzip -dc /home/your_username/image.gz | dd bs=4M of=/dev/sdb
		
Step 3) Connect the Ethernet Cable on Raspberry:

Step 4) Check the Internet connection. Run the command.

		ping 8.8.8.8
		
Step 5) Set up Wi-Fi dongle:
Connect Wi-Fi dongle and restart Raspberry Pi, running the command
		
		sudo reboot
	
	
Now, see wlan0 interface after you run the following:
	
		ifconfig -a
		
## Turn Raspberry Pi into a Hotspot:
This tutorial followed this link's one: https://cdn-learn.adafruit.com/downloads/pdf/setting-up-a-raspberry-pi-as-a-wifi-access-point.pdf.

### Install the software:

Step 1) Install software onto the Raspberry Pi that it will act as a access point. Attention: Internet connection needed to do this step:

		sudo update
		sudo apt-get install isc-dhcp-server
		sudo apt-get install hostapd
		
Step 2) Install a iptables manager too:
		
		sudo apt-get install iptables-persistent
		
Type "YES" to both configuration screens.

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
		  address 192.168.0.1
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
		wpa_passphrase=<password>
		wpa_key_mgmt=WPA-PSK
		wpa_pairwise=CCMP
		wpa_group_rekey=86400
		ieee80211n=1
		wme_enabled=1
		
Step 3) In this file, edit the variable wpa_passphrase to some password which it will be Wi-Fi's password.

Step 4) Say to Raspberry Pi where to find this configuration file. Run that command to edit the file /etc/default/hostapd.

Find the line:
		
		#DAEMON_CONF="" 

Edit it to say :
		
		DAEMON_CONF="/etc/hostapd/hostapd.conf" 
Step 5) Run that command to edit the file /etc/default/hostapd.

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
		
### Reboot Raspberry Pi/etc/hotsapd/hostapd.conf
Step 1) Run the command 
		
		sudo reboot
		
### Test the WiFi connection:

### Running flusher script:
Step 1) Download the file flushing/fog_agent.py in the https://github.com/pedrocruz/sensing_bus.

### Generate a key and certificate:
This tutorial followed this link's one: https://jamielinux.com/docs/openssl-certificate-authority/sign-server-and-client-certificates.html. This section explains how to sign server and client certificates

Step 1) Create a key

		cd /root/ca
		openssl genrsa -aes256 \
			-out intermediate/private/www.example.com.key.pem 2048
		chmod 400 intermediate/private/www.example.com.key.pem
		
Step 2) Use the private key to create a certificate signing request (CSR)

		cd /root/ca
		openssl req -config intermediate/openssl.cnf \
      			-key intermediate/private/www.example.com.key.pem \
      			-new -sha256 -out intermediate/csr/www.example.com.csr.pem

Step 3) Enter pass phrase. Fill the other blanks.

Step 4) Create a certificate

		cd /root/ca
		openssl ca -config intermediate/openssl.cnf \
		      -extensions server_cert -days 375 -notext -md sha256 \
		      -in intermediate/csr/www.example.com.csr.pem \
		      -out intermediate/certs/www.example.com.cert.pem
		chmod 444 intermediate/certs/www.example.com.cert.pem

Step 5) Verify the certificate
		
		openssl x509 -noout -text \
		      -in intermediate/certs/www.example.com.cert.pem
		      
Step 6) Use the CA certificate to verify that the new carticate might be trustful.

		openssl verify -CAfile intermediate/certs/ca-chain.cert.pem \
      			intermediate/certs/www.example.com.cert.pem
			
Step 7) Deploy the certificate. The following files needs to be available

		ca-chain.cert.pem
		www.example.com.key.pem
		www.example.com.cert.pem

### Edit the file fog_agent.py:

Step 1) Change the variable MEASUREMENTS_URL to Publishing URL.

Step 2) Change the variable PRIMARY_KEY to the address of the file of key generated in section "Generate a key and a certificate".

Step 3) Change the variable LOCAL_CERTIFICATE to the address of the file of certificate generated in section "Generate a key and a certificate".

### Run fog_agent.py

## Installation Guide:

Step 1) Download the SensingBusOS image in the following link: 

		https://www.dropbox.com/s/557oetnzkeg8mpv/SensingBusOS.gz?dl=0

Step 2) Edit the file /etc/hotsapd/hostapd.conf. Change the variable wpa_passphrase to some password which it will be Wi-Fi's password.

### Follow the instructions of section "Generate a key and a certificate".

### Follow the instructions of section "Edit the file fog_agent.py".

### Run fog_agent.py



# Fog Management:

This function allows the system's administrator manage what application or
even or data analysis it's necessary to improve accuracy or to improve quality
of datas. There is two folders inside folder flushing. manager_fog and
manage_fog_user, the first one is about the crips will be run on fog. The last
one is about the scripts which administrator must run.

The main idea is the administrator of network can transfer scripts to the flushing nodes. The transferency of data use scp protocol to do it. The flushing nodes receives this files, then implements this new function to analyze the data from sensing nodes. The main advantage of use a fog manager that the administrator can change this function any time, so a fogmanagement makes the system more flexible. At the momento, there is two function ready. The first one implements meia of average measurements. This function receives the data from sensing nodes, average the measurmentes the sends to the cloud. The second function delete impossible measures. 



## Detalhes do Funcionamento:
O administrator executa o script adm.py. Este script recebe o nome o modulo
a ser enviado para a fog. Modifica o nome para um nome padrao, envia por scp
e retorna ao nome original do arquivo. Nesta pasta manager_fog_user o admin
tem acesso a todos os modulos disponiveis e pode adicionar outros mais. 
Apos o envio do arquivo. este arquivo e importado e executado pelo fog.
Dessa maneira, o admin pode escolher e trocar os modulos e as analise de dados
a ser executada pela fog.













