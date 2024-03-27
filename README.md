# Running Services locally

The following Environment variables need to be set before the docker compose can be run:

```
$env:DB_ROOT_PASSWORD="test"
$env:DB_WEB_USER="webapp"
$env:DB_WEB_PASSWORD="<replace me>"
$env:DB_FUNC_USER="funcapp"
$env:DB_FUNC_PASSWORD="<replace me>"
$env:DB_NAME="turbine_monitor"
```

The database will mount the db directory volume which contains an init script that will initialise the DB with the correct users.
The passwords for webapp and funcapp should be updated accordingly.


To run container:

`docker compose up`

To stop containers

`Ctrl + C`

To clean up all images and volumes:

`docker system prune --volumes`


# Acknowledgements

It is acknowledged that a better solution would use docker secrets rather than passing these directly as environment variables.

An attempt was also made to configure SSL DB connections using self signed CA and trough mounting a .cnf file to the mariadb instance.
Commented out fragments of these attempts may have been left throughout the project with the intention to revisit with no success.