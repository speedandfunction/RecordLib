**************************
Webapp Interface
**************************

docker-compose
===============

The easiest way to use `RecordLib` is to run the web intercace. 

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