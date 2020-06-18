**************************
Webapp Interface
**************************

docker-compose
===============

The easiest way to use `RecordLib` is to run the web interface. 

The quickest way to start up the webapp is to run

.. code-block:: bash

   yarn install
   make docker-build-up

This will start up the app using the configuration of `deployment/docker-compose-build.yml`. This method will
use default configuration values (not suitable for production, though!).


Visit `localhost:3000` and log in.

If this is your first time running the app, it will initialize with a default superuser. 
The username will be the value of the environment variable, `ADMIN_USERNAME`. The password will be
generated randomly and logged to the console. 

The initial admin password will appear like this in the docker-compose console output:

.. code-block:: bash

   migration_1   | Temp admin admin2: JCS5eQKgojBtCS4XxaG_fc9aE1QG9MIZPHu72hUN

Now you can try searching for public criminal records and analyzing records for expungeable arrests. 

**This method won't work well for development.**. You'd have to rebuild the app image after every time you make a change to the code. 

To develop the app, you'll want a local installation

Local installation
====================

Installing locally without using containers has a few steps and a few dependencies to satisfy.

Postgres
---------

We'll need a Postgres database set up. Install Postgres and create a database and a user for Recordlib.

.. code-block:: bash
   me$ sudo apt install postgresql postgresql-contrib
   me$ sudo su - postgres
   postgres@home$ psql
   postgres=$ CREATE DATABASE recordlibdev;
   postgres=# \q
   postgres@home$ createuser --interactive --pwprompt
   ...
   postgres@home$ psql
   postgres=# grant ALL on DATABASE recordlibdev to recordlibdev;
   postgres=# \q 


Python
-------

You'll need python 3.7 and pipenv installed. See https://pipenv-fork.readthedocs.io/en/latest/install.html. 

Install the python dependencies and create a virtual environement with `pipenv install`


