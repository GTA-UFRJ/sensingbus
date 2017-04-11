# SensingBus Publisher

## Instalation
The Publisher Node is a server running on a virtual machine instantiated on a Openstack cloud service. 
To install the publisher node, just instantiate a virtual machine on a cloud service.
**Make sure the server's URL is the same configured on the flushing nodes.**

### Hardware Requirements:

Openstack requires at least 2 nodes, a Controller and a Virtual Machine Server, to build a cloud. Read [this](https://docs.openstack.org/mitaka/install-guide-ubuntu/overview.html#example-architecture) for more details.
Basically, the minimun requirements are:

* Dual-core CPU
* 8 GB RAM
* 2 network ports (1 Gigabit)
* 100 GB disk
* Physical console access

#### Openstack Cloud Installation
Read this [documentation](https://docs.openstack.org/mitaka/) to install a Openstack cloud. The current software version is Ocata, but the SensingBus system was developed on Mitaka version.

Openstack has a modular archtecture. The SensingBus system requires only the following modules:

* Identity (Keystone)
* Image (Glance)
* Compute (Nova)
* Networking (Neutron) - *Self-Service Network*
* Dashboard (Horizon)

#### Publication Node Installation
Upload this [image](http://gloria.gta.ufrj.br/vm-templates/publishing-node-image) to your cloud. Follow these [instructions](https://docs.openstack.org/user-guide/dashboard-manage-images.html) to upload a image. 
Just instantiate a virtual machine, generating a [key pair](https://docs.openstack.org/mitaka/install-guide-ubuntu/launch-instance.html#generate-a-key-pair), selecting the publication node image and a flavor with the minimum requirements:

* 1 VCPUS
* 5 GB RAM
* 5 GB Disk

All this can be done through the web interface. Optionally, follow [these](https://docs.openstack.org/mitaka/install-guide-ubuntu/launch-instance-selfservice.html) instructions to instantiate a virtual machine.

Remember to [allow ssh](https://docs.openstack.org/mitaka/install-guide-ubuntu/launch-instance.html#add-security-group-rules) on security group rules.

The installation is complete. Now, a few configuration steps are required.

## Configuration

### Setting Apache server

To set the Apache server, follow these instructions to setup Django as a wsgi application https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/modwsgi/.

A template of apache configuration file can be found [here](https://github.com/pedrocruz/sensing_bus/blob/master/publishing/installation-templates/apache2.conf).

Add this to the end of apache.conf. Replace <SERVER-ADRESs> and <public-IP> with the public IP address of the publishing node. Replace <YOU-PATH> with the appropriate PATH for your environment.

```
ServerName <SERVER-ADRESs>

## Sensing_Bus config
Alias /media/ /var/www/<public-IP>/media/
Alias /static /var/www/<public-IP>/static/

<Directory /var/www/<public-IP>/static>
Require all granted
</Directory>

<Directory /var/www/<public-IP>/static>
Require all granted
</Directory>

WSGIScriptAlias / <YOUR-PATH>/sensing_bus/publishing/sensing_bus/sensing_bus/wsgi.py
WSGIPythonPath <YOUR-PATH>/sensing_bus/publishing/sensing_bus:/home/ubuntu/venv/lib/python2.7/site-packages

<Directory <YOUR-PATH>/sensing_bus/publishing/sensing_bus/sensing_bus >
<Files wsgi.py>
Require all granted
</Files>
```

Create a Certificate Authority to validate users (flushing nodes). For security, Apache server is configured to accept data insertion only of trusted users.

## Certificate Authority

Follow this [tutorial](https://jamielinux.com/docs/openssl-certificate-authority/introduction.html) to create a Certificate Authority.

#### Generating User Keys

Notice that flushing nodes are seem as users by the publishing node.

The flushing node has to generate a public key and a request for certificate and send those to the CA. The CA will generate a certificate allowing the node to communicate with the publishing node.

Do the following command on the flushing node:

```
openssl genrsa -out <your path>/keys/www.sensingbus.gta.ufrj.br.key.pem 2048
```

Give reading permission to other users in your public key:

```
chmod 400 <path_maneiro>/www.sensingbus.gta.ufrj.br.key.pem
```

Configure [this](https://github.com/pedrocruz/sensing_bus/blob/master/publishing/installation-templates/openssl.cnf) openssl.cnf file, replacing <YOUR-PATH> with the adequate to your environment.

```
[ CA_default ]
# Directory and file locations.
dir               = <YOUR-PATH>/ssl/ca/intermediate
```
Especify some localty defaults:

```
[ req_distinguished_name ]

#countryName_default             = Country Name (2 letter code)
#stateOrProvinceName_default     = State or Province Name
#localityName_default            = Locality Name
#0.organizationName_default      = Organization Name
#organizationalUnitName_default  = Organizational Unit Name
#emailAddress_default            = Email Address
```

Generate a certificate request. 

```
openssl req -config openssl.cnf \
      -key <your-path>/keys/intermediate/www.sensingbus.gta.ufrj.br.key.pem \
      -new -sha256 -out <your-path>/keys/intermediate/www.sensingbus.gta.ufrj.br.csr.pem
```

Send these files to the CA and authorize the user.

#### Authorizing Users

The following steps must be followed in your CA.
After receiving a certificate request, the CA must authorize the user.

```
openssl ca -config <your-path>/keys/intermediate/openssl.cnf \
      -extensions usr_cert -notext -md sha256 \
      -in <your-path>/keys/intermediate/csr/sensingbus.gta.ufrj.br.csr.pem \
      -out <your-path>/keys/intermediate/certs/sensingbus.gta.ufrj.br.cert.pem
```

Verify if the certificate is valid:

```
 openssl verify -CAfile intermediate/certs/ca-chain.cert.pem \
      intermediate/certs/bob@example.com.cert.pem
 ```

The publishing node web interface must be  working on https:\\"virtual-machine-public-address".

Note that ""virtual-machine-public-address" must be replaced.
