import os
import sqlalchemy

"""
This is a utility package used for common actions for connecting to a Maria DB
This is used in both MeasurementFnc and TurbineSvc
"""


"""
Fetches or constructs a a DB connection URI based on the environment variables provided
"""
def uri() -> sqlalchemy.engine.url.URL:
    # check for DB connection string if provided and use that as the uri
    connection_str = os.environ.get("DB_CONNECTION_STRING", default="")
    if len(connection_str) != 0:
        return connection_str

    # construct DB connect url based on the environment 
    url = sqlalchemy.engine.url.URL.create(
        drivername = "mariadb+mariadbconnector",
        username = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        host = os.environ.get("DB_SERVER"),
        port = os.environ.get("DB_PORT"),
        database = os.environ.get("DB_NAME", default="turbine_monitor"))

    return url


"""
Appends an ssl ca connection argument if a certificate is provided in environment variables
"""
def connection_args() -> dict:
    connection_args = {}

    # Check ssl cert is provided in environment varibales
    ssl_cert_file = os.environ.get("DB_SSL_CERT", default=None)
    if ssl_cert_file is not None:
        # Add to connection args if present
        connection_args.update({
            'ssl': {'ca': ssl_cert_file}
        })

    return connection_args


"""
For testing a connection between and sqlalchemy DB engine
Returns error if connection fails
"""
def test_connection(engine: sqlalchemy.Engine) -> str:
    try:
        engine.connect()
        con = engine.connect()
        con.close()
    except sqlalchemy.exc.OperationalError as err:
        return f"DB connection error: {err.__cause__}"
    return ""