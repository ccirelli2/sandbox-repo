"""
Module with function to connect to an external datasource (other than a flat file)
"""
import logging
import os
import sys
from datetime import datetime
import warnings
import mysql.connector
from decouple import config as d_config

# Declare Directories
DIR_ROOT = d_config("DIR_ROOT")
DIR_DATA = d_config("DIR_DATA")
DIR_SRC = d_config("DIR_SRC")
sys.path.append(DIR_ROOT)
sys.path.append(DIR_SRC)

# import Project Modules
from src.utilities import my_timeit

# Package Settings
logging.basicConfig(level=logging.INFO)

# Functions
@my_timeit
def mysql_connect(host: str, user_name: str, password: str, database: str) -> mysql.connector.connect:
    """

    Args:
        database:
        host:
        user_name:
        password:
    """
    my_conn = mysql.connector.connect(
        host=host,
        user=user_name,
        password=password,
        database=database
    )
    if my_conn:
        logging.info(f"Connection established successfully to {database} for user {user_name}")
    return my_conn


if __name__ == "__main__":
    try:
        test_connection = mysql_connect(
            host=d_config("MYSQL_HOST"),
            user_name=d_config("MYSQL_USER"),
            password=d_config("MYSQL_PASSWORD"),
            database="sandbox_onsite"
        )
    except Exception as err:
        logging.error(f"Connection to mysql failed with error {err}")



