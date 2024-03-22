from statistics import mean, stdev
import azure.functions as func
import models
import logging
import sqlalchemy
from sqlalchemy.orm import Session
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
__test_db_engine__ = sqlalchemy.create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)


def database_uri() -> sqlalchemy.engine.url.URL:
    url = os.environ.get("DB_CONNECTION_STRING", default="")
    if len(url) != 0:
        return url

    url = sqlalchemy.engine.url.URL.create(
        drivername = os.environ.get("DB_DRIVER", default="mariadb+mariadbconnector"),
        username = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        host = os.environ.get("DB_SERVER"),
        port = os.environ.get("DB_PORT"),
        database = os.environ.get("DB_NAME", default="turbine_monitor"))

    return url


def database_connection_args() -> dict:
    connection_args = {}

    ssl_cert_file = os.environ.get("DB_SSL_CERT", default=None)
    if ssl_cert_file is not None:
        connection_args.update({
            'ssl': {'ca': ssl_cert_file}
        })

    return connection_args


def test_connection(engine: sqlalchemy.Engine) -> str:
    try:
        engine.connect()
        con = engine.connect()
        con.close()
    except sqlalchemy.exc.OperationalError as err:
        return f"DB connection error: {err.__cause__}"
    return ""


@app.function_name(name="measurement_func")
@app.route(route="record-measurements", methods=["POST"])
def record_measurements(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Measurement func recieved request.')

    turbine_serial = req.params.get('serial')
    if turbine_serial is None:
        return func.HttpResponse("Turbine serial not provided.", status_code=400)
    
    try:
        req_json = req.get_json()
        records = []
        for m in req_json:
            records.append(models.Measurement_Record(
                m['wind_speed'], 
                m['pitch'],
                m['power'],
                m['timestamp']
            ))
    except TypeError:
        return func.HttpResponse("JSON body not provided.", status_code=400)
    except (KeyError, ValueError) as e:
        return func.HttpResponse("Invalid JSON format.", status_code=400)
        
    # Use the test engine if it has been set.
    if __test_db_engine__ is not None:
        engine = __test_db_engine__

    # Create a database connection.
    else:
        connection_string = database_uri()
        connection_args = database_connection_args()
        engine = sqlalchemy.create_engine(connection_string,
                                          connect_args=connection_args,
                                          echo=False, future=True)
        # Test the connection.
        error_message = test_connection(engine)
        if len(error_message) > 0:
            return func.HttpResponse(error_message,
                                     status_code=500)

    session = Session(engine)
    statement = sqlalchemy.select(models.Turbine).where(models.Turbine.serial == turbine_serial)
    turbine = session.execute(statement).scalar_one_or_none()

    if turbine is None:
        logging.info("Turbine with serial {0} does not exist".format(turbine_serial))
        return func.HttpResponse("Trubine with serial {0} not found.".format(turbine_serial), status_code=404)
    
    logging.info(records)
    n_samples = len(records)
    samples_from = min(r.timestamp for r in records)
    samples_to = max(r.timestamp for r in records)
    
    #TODO - use arrays for properties
    #TODO - handle null pitc and power
    wind_speed_mean = mean(r.wind_speed for r in records)
    wind_speed_stdev = stdev(r.wind_speed for r in records)
    power_mean = mean(r.power for r in records)
    power_stdev = stdev(r.power for r in records)
    pitch_mean = mean(r.pitch for r in records)
    pitch_stdev = stdev(r.pitch for r in records)
    
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
    
    session.add(new_measurement)
    session.commit()

    return func.HttpResponse("Logged Measurements.", status_code=201)
