import os
import sqlalchemy

def uri(connection_str) -> sqlalchemy.engine.url.URL:
    if len(connection_str) != 0:
        return url

    url = sqlalchemy.engine.url.URL.create(
        drivername = os.environ.get("DB_DRIVER", default="mariadb+mariadbconnector"),
        username = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        host = os.environ.get("DB_SERVER"),
        port = os.environ.get("DB_PORT"),
        database = os.environ.get("DB_NAME", default="turbine_monitor"))

    return url


def connection_args() -> dict:
    connection_args = {}

    ssl_cert_file = os.environ.get("DB_SSL_CERT", default=None)
    if ssl_cert_file is not None:
        connection_args.update({
            'ssl': {'ca': ssl_cert_file}
        })

    return connection_args