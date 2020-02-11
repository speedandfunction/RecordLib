# Expungement Generator v2

## docker-compose

The quickest way to start up the webapp is to run

`make docker-up`.

This will start up the app using the configuration of `deployment/docker-compose.yml`, using 
default configuration values (not suitable for production, though!).

If this is your first time running the app, it will initialize with a default superuser. 
The username will be the value of the environment variable, `ADMIN_USERNAME`. The password will be
generated randomly and logged to the console. 

The initial admin passwork will look like this:

.. code-block: bash
   migration_1   | Temp admin admin2: JCS5eQKgojBtCS4XxaG_fc9aE1QG9MIZPHu72hUN
 