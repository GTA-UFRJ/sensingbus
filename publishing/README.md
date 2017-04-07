#Sensing Bus Publisher


## Instalation
The Publisher Node is a server running on a virtual machine instantiated on a Openstack cloud service. 
To install the publisher node, just instantiate a virtual machine on a cloud service.
**Make sure the server's URL is the same configured on the flushing nodes.**

#### Openstack Cloud
We recommend use an [Openstack](https://docs.openstack.org/mitaka/) platform to build your cloud. The current version is Ocata, but the tool was developed on Mitaka version.

You can use this [image](http://gloria.gta.ufrj.br/vm-templates/) to instantiate your publication node.


## Development
To develop on the Publisher Node, it is necessary to clone the repository.
  
  ```
  git clone https://github.com/pedrocruz/sensing_bus.git
  ```

Then, the requirements must be installed. It is recommended that a virtual environment is created outside the repository:

  ```
  pip install virtualenv  
  virtualenv venv  
  source venv/bin/activate
  ```
  
Now, with the environment active, install the requirements:

  ```
  pip install -r sensing_bus/publishing/requirements.txt
  ```

After that, the development can start as a regular Django project.

### Setting Apache server

To set the Apache server, follow the instructions to setup a Django application as a wsgi application https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/modwsgi/

A template of apache configuration file can be found [here](https://github.com/pedrocruz/sensing_bus/blob/master/publishing/installation-templates/apache2.conf).

## Certificate Authority

You can follow this [tutorial](https://jamielinux.com/docs/openssl-certificate-authority/introduction.html) to create yout own Certificate Authority.

#### Generating User Keys

Your flushing node has to generate a public key and a request for certificate and send those to the CA. The CA will generate a certificate allowing the node to communicate with the publishing node.

Do the following command on the flushing node:

```
openssl genrsa -out <your path>/keys/www.sensingbus.gta.ufrj.br.key.pem 2048
```

Give reading permission to other users in your public key

```
chmod 400 <path_maneiro>/www.sensingbus.gta.ufrj.br.key.pem
```

Generate a certificate request. Configure [this](https://github.com/pedrocruz/sensing_bus/blob/master/publishing/installation-templates/openssl.cnf) openssl.cnf file for this step:

```
openssl req -config openssl.cnf \
      -key <your-path>/keys/intermediate/www.sensingbus.gta.ufrj.br.key.pem \
      -new -sha256 -out <your-path>/keys/intermediate/www.sensingbus.gta.ufrj.br.csr.pem
```

Send these file to your CA and authorize user.

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
