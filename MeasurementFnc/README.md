# Deploying MeasurementFnc
It is assumed that the TurbineSvc has been deployed prior to this so the following instructions will use the resource group and container registry already created.

A student account will also be used for this exercise so the following commands should be run before proceeding: ```az login``` and to login then ```az account set -s "Azure for Students"```

## Deploy container image
If the same terminal is still used from deploying the TurbineSvc the variable for the registry name should still be set. This can be verified by running:

```$cr```

Which should return the name of the container registry that was previously created. If not this should be set.

You will need docker deskyop installed and running and be inside the MeasurementFnc directory by running```cd <your path>/solution/MeasurementFnc```

You will need to login to the container registry if not already:

```az acr login --name $cr```

To build and tag the image inside the dockerfile run:

```
docker build --tag measurement-fnc/funcapp:1 .
```

Then push this to the registry by running the following:

```
docker image tag measurement-fnc/funcapp:1 crturbinemonitoring.azurecr.io/measurement-fnc/funcapp:1
```
```
docker push crturbinemonitoring.azurecr.io/measurement-fnc/funcapp:1
```

Then verify it has been pushed successfully by checking:

```
az acr repository list --name $cr
```

which should return an array containing the measurement-fnc/funcapp image name.

## Deploy image to function app
Again if the same terminal is used from deploying the turbineSvc the required variables should already be set for: `$username` `$password` `$rg` If not this will need to be done, refer to TurbineSvc/README.md for details.


Function apps require an azure storage account for persisiting metadata about them.
This can be created by running the following:

```
$sa = "stturbinemonitoring"
```
```
az storage account create --name $sa --resource-group $rg --location uksouth --sku Standard_LRS --kind StorageV2 --allow-blob-public-access false
```

Function apps cannot be deployed to a Free tier app service plan. Therefore, you need to create a basic Tier service plan to deploy the function onto by running the following:

```
$masp = "plan-measurment"
```
```
az appservice plan create --location uksouth --resource-group $rg --name $masp --sku B1 --is-linux --no-wait
```

Note: Having microservices on different app service plans is also a good practice to allow them to be scaled independently.

The function app can now be created with the following: 

```
$funcname = "func-measurementfnc"
```
```
az functionapp create --name $funcname --storage-account $sa --plan $masp --resource-group $rg --functions-version 4 --image crturbinemonitoring.azurecr.io/measurement-fnc/funcapp:1 --registry-password $password --registry-username $username --disable-app-insights
```

# Testing deployed MeasurementFnc
The function app has the same design as the turbine service allowing a DB connection string to either be provided or constructed. Refer to TurbineSvc.README.md for more information.

## Running Web App

The app can therefore be configured to either:

### 1. Connect to sqlite in memory DB

```
az functionapp config appsettings set --name $funcname --resource-group $rg --settings DB_CONNECTION_STRING=sqlite:///:memory:
```

### 2. Connect to existing DB Server

```
az functionapp config appsettings set --name $funcname --resource-group $rg --settings DB_NAME=turbine_monitor DB_HOST=<replace-me> DB_USER=<replace-me> DB_PASSWORD=<replace-me> 
```

## Testing app functionality
The postman collection in the root /solution directory also contains a route to trigger the function. This will require an environment variable for fnc_uri which should correspond to the hostname returned from:

```
az functionapp show --resource-group $rg --name $funcapp
```

This should be https://func-measurementfnc.azurewebsites.net where func-measurementfnc corresponds to $funcapp.

Provided the Turbine svc is running anc connected to the same DB as the function you should be able to test end-to-end functionality of the app. 
