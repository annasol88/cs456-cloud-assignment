import os
from statistics import mean, stdev
import azure.functions as func
import models
import logging
import sqlalchemy
from sqlalchemy.orm import Session
import dbutils as db


# Define function app 
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# Stub test engine for unit testing so that tests don't modify real data 
__test_db_engine__ = None


"""
Function app method which is executed when the function is triggered with an
http POST request on /record-measurements route
"""
@app.function_name(name="measurement_func")
@app.route(route="record-measurements", methods=["POST"])
def record_measurements(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Measurement func recieved request.')
    
    # Check Turbine serial is provided in the request to proceed
    turbine_serial = req.params.get('serial')
    if turbine_serial is None:
        logging.info('No Turbine serial provided in request.')
        return func.HttpResponse("No Turbine serial provided in request", status_code=400)
    
    # Validate Request Body is in the correct format
    try:
        req_json = req.get_json()
        if len(req_json) == 0:
            logging.info('No Turbine serial provided in request.')
            return func.HttpResponse("No data provided in request.", status_code=400)
        records = []
        for m in req_json:
            records.append(models.Measurement_Record(
                m['wind_speed'], 
                m['pitch'],
                m['power'],
                m['timestamp']
            ))
            
    except TypeError:
        # Return 4000 if invalid request body type
        logging.info('JSON body not provided in request.')
        return func.HttpResponse("JSON body not provided in request.", status_code=400)
    
    except (KeyError, ValueError) as e:
        # return 400 if the JSON schema in the request is not what is expected 
        # Or if timestamps are in an invalid format 
        logging.info('Invalid JSON format in request.')
        return func.HttpResponse("Invalid JSON format in request.", status_code=400)
    
    
    logging.info('Request body valid.')  

    # Use the test engine if it has been set.
    if __test_db_engine__ is not None:
        logging.info('Test DB engine used.') 
        engine = __test_db_engine__

    # Otherwise establish a DB connection uring environment arguments provided
    else:
        connection_string = db.uri()
        connection_args = db.connection_args()
        engine = sqlalchemy.create_engine(
            connection_string,
            connect_args=connection_args,
            future=True)
        
        # Test the connection.
        logging.info('Testing DB Connection.')  
        error_message = db.test_connection(engine)
        if len(error_message) > 0:
            return func.HttpResponse(error_message, status_code=500)

    # Create DB schema if one does not exist.
    models.Base.metadata.create_all(engine)
    session = Session(engine)

    # Verify that a turbine with the provided serial exists in the database.
    statement = sqlalchemy.select(models.Turbine).where(models.Turbine.serial == turbine_serial)
    turbine = session.execute(statement).scalar_one_or_none()

    # Return 404 if turbine does not.
    if turbine is None:
        logging.info("Turbine with serial {0} does not exist".format(turbine_serial))
        return func.HttpResponse("Trubine with serial {0} not found.".format(turbine_serial), status_code=404)
    
    logging.info('Calculating Measurements.')
    # Calculate number of samples.
    n_samples = len(records)
    
    # Calculate measurement to and from times. 
    times = [r.timestamp for r in records]
    samples_from = min(times)
    samples_to = max(times)
    
    # Construct arrays for wind speed, pitch and power data
    # It is assumed that a turbine might be shutdown during a reading
    # Hence None values are remove to provide valid calculations for these properties.
    wind_speeds = [r.wind_speed for r in records]
    pitches = [r.pitch for r in records if r.pitch is not None]
    powers = [r.power for r in records if r.power is not None]
    
    # Calculate mean and stdev values 
    wind_speed_mean = mean(wind_speeds)
    wind_speed_stdev = stdev(wind_speeds)
    
    if len(pitches) > 1:
        pitch_mean = mean(pitches)
        pitch_stdev = stdev(pitches)
    else:
        # Default to None if there are not enough samples to calculate Pitch mean and stdev.
        pitch_mean = None
        pitch_stdev = None
        
    if len(powers) > 1: 
        power_mean = mean(powers)
        power_stdev = stdev(powers)
    else:
        # Default to None if there are not enough samples to calculate Pitch mean and stdev.
        power_mean = None
        power_stdev = None
    
    # Create new measurement object 
    new_measurement = models.Measurement(
        turbine.id, 
        wind_speed_mean, 
        wind_speed_stdev, 
        pitch_mean, 
        pitch_stdev,
        power_mean,
        power_stdev, 
        n_samples,
        samples_from,
        samples_to)
    
    try:
        # Commit new measurement record to DB 
        logging.info('Saving new measurement record.')
        session.add(new_measurement)
        session.commit()
    except Excpetion:
        # Retrurn 500 if DB connection fails while creating new record
        return func.HttpResponse("Failed to log new measurement in DB", status_code=500)

    # Return 201 for successfully logged measurements.
    return func.HttpResponse("Logged Measurements.", status_code=201)
