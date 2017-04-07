#Sensing Bus Publisher


## Instalation
The Publisher Node is a server running on a virtual machine instantiated on a {Openstack}(https://docs.openstack.org/mitaka/) cloud service. 
To install the publisher node, just instantiate the virtual machine on the cloud service.
Make sure the server's URL is the same configured on the flushing nodes.


## Development
To develop on the Publisher Node, it is necessary to clone the repository.
  
  ```
  git clone <repo_url>
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

______________________________________________________________

### Project organization

The project is named sensing_bus an has an app named publisher, responsible for the web pages.

### Backend Anotation

To write data on the server, the fog node must be authenticated through the API.

### Database

To generate the database dump, run:

```
python manage.py dumpdata -e contenttypes ><filename.json>/debug-e.json
```

There is a small database demo dump, located at http://gta.ufrj.br/~cruz/sensing_bus/

To use it, save it into a file and run:

```
./manage.py loaddata <file_name.json>
```
