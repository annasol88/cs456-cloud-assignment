# Deploying TurbineSvc
To deploy anything to Azure through windows PS you must first ensure you are logged in.
To check, you can run the following command in a windows powershell terminal:
```az account list```

If nothing displays, type: 
```az login```
and follow the prompts or redirect to login. 

It is assumed that a student account is used for this exercise so the following command is run to set it as the default subscription:
```az account set -s "Azure for Students"```

## Create Container Registry
A container registry along with a resource group need to be created since a student account is used. Note: if using a teaching subscription, the existing container registry and resource group can be used.

First create a resource group run the following:

```
$rg = "rg-turbine-monitoring"
```

```
az group create --location uksouth --name $rg
```

Then create container registry by running:

```
$cr = "crturbinemonitoring"
```

```
az acr create --location uksouth --resource-group $rg --name $cr --sku Basic
```

the name 'crturbinemonitoring' must be unique in azure so can be replaced if necessary. 

## Deploy Container Image
To deploy the turbine web service you must ensure you are in the correct directory by navigating to TurbineSvc from your current location: ```cd <your path>/solution/TurbineSvc```

You will need docker desktop installed and running to complete the next steps.

You will also need to login to the container registry created in the previous step by running:

```az acr login --name $cr```

To build and tag the image inside the dockerfile run:

```
docker build --tag turbine-svc/webapp:1 .
```

the container name is derived using the reccommended format: `<project-name>/<image-name>:<version>` which can be changed at your own discretion.

To push this to the registry run the following:

```
docker image tag turbine-svc/webapp:1 crturbinemonitoring.azurecr.io/turbine-svc/webapp:1
```

```
docker push crturbinemonitoring.azurecr.io/turbine-svc/webapp:1
```

Once executed, it can be verified that the image has been pushed successfully by running:

```
az acr repository list --name $cr
```

which should return an array containing the turbine-svc/webapp image name.

## Deploy Image to App Service
To deploy the app from the container registry to a web app you will need an app service plan.
Note: The teaching subscription will have an available app service plan that can be used instead.

Create an app service plan by running:

```
$tasp = "plan-turbine"
```

```
az appservice plan create --location uksouth --resource-group $rg --name $tasp --sku FREE --is-linux --no-wait
```

To deploy the container image onto a webapp you will need to pass credentials of the container registry into the request.
To do so remote admin access to the registry needs to be enabled by running:

```
az acr update -n $cr --admin-enabled true
```

To use username and password values when creating a web app you will need to fetch and store them as variables using the following commands:

```
$username = (az acr credential show --resource-group $rg --name $cr --query 'username') -replace '\"', '' 
```

```
$password = (az acr credential show --resource-group $rg --name $cr --query passwords[0].value) -replace '\"', '' 
```

windows -replace is used to remove the surrounding "" returned from the request.

Now a web app can be created by running the following:

```
$appname = "app-turbinesvc"
```

```
az webapp create --name $appname --resource-group $rg --plan $tasp --deployment-container-image-name crturbinemonitoring.azurecr.io/turbine-svc/webapp:1 --docker-registry-server-password $password --docker-registry-server-user $username
```

# Testing deployed TurbineSvc
The web app will not currently work because it depends on environment variables to be provided in order to setup the database connection.

Also, by default azure web apps also listen to PORT 80 rather than 5000 which is what we expect in the container so this will need to be updated in app settings also (shown below) 

## Running Web App
The webapp is designed to accept a DB connection URI argument ``DB_CONNECTION_STRING`` or construct one based on the following attributes:

``DB_USER`` - the user accessing the DB.

``DB_PASSWORD`` - the assword of the user accessing the DB.

``DB_SERVER`` - the server the DB is running on.

``DB_PORT`` - the port that the DB server is listening on.

``DB_NAME`` - the name of the database that will be queried (defaults to: turbine_monitor)

This provides 2 options:

### 1. Connect webapp to sqlite in memory DB

This can be done by updating the app settings as follows:
```
az webapp config appsettings set --name $appname --resource-group $rg --settings PORT=5000 DB_CONNECTION_STRING=sqlite:///:memory:
```

### 2. Connect to existing DB Server
For this configuration the app settings need to be updated as follows:

```
az webapp config appsettings set --name $appname --resource-group $rg --settings PORT=5000 DB_NAME=turbine_monitor DB_HOST=<replace-me> DB_USER=<replace-me> DB_PASSWORD=<replace-me>
```

where the DB_HOST DB_USER and DB_PASSWORD should be replaced accordingly.

## Testing app functionality
The root folder /solution includes a postman collection that contains all the relevant routes for testing the app: `TurbineMonitor.postman_collection.json`

This can be dragged and dropped into Postman.

You will need to create a variable for webapp_uri and set it to the hostname that the app is deployed onto which can be found in the object returned after running:

```
az webapp show --resource-group $rg --name $webapp
```

This should be https://app-turbinesvc.azurewebsites.net where app-turbinesvc is whatever $webapp was set to.

You can then proceed to testing each of these routes to verify the app works as expected.

The best way to test end-to-end functionality is by having the measurment function running simultaneously. Note however, this is not possible using an in memory sqlite configuration since the apps will point to their own (in memory) data source.