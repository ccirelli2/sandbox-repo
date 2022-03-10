"""
Scratchpad
"""
import os
import sys
import pandas as pd
from sklearn import tree
from decouple import config as d_config
import mysql.connector
from uuid import uuid4
import logging
logging.basicConfig(level=logging.INFO)


# Declare Directories
DIR_ROOT = d_config("DIR_ROOT")
DIR_DATA = d_config("DIR_DATA")
DIR_SRC = d_config("DIR_SRC")
sys.path.append(DIR_ROOT)
sys.path.append(DIR_SRC)

# Queries
def query_wine():
    """
    Generic query to get all data from wine table
    Returns:
    string of query
    """
    query = """
    SELECT *
    FROM wind_raw;
    """
    return query

def insert_dt_opt_depth(data_frame: pd.DataFrame, conn: mysql.connector, max_depth_col_name: str,
                        accuracy_col_name: str) -> None:
    """

    Args:
        accuracy_col_name:
        max_depth_col_name:
        conn:
        data_frame:
    """
    count = 0
    for row in data_frame.iterrows():
        series = row[1]
        max_depth = series[max_depth_col_name]
        accuracy = series[accuracy_col_name]

        # Create Cursor
        my_cursor = conn.cursor()

        # Create Event ID
        event_id = str(uuid4())[:4]

        # Insertion
        sql = "INSERT INTO sandbox_onsite.decision_tree_accuracy_max_depth (event_id, max_depth, accuracy) VALUES (%s, %s, %s)"
        val = (event_id, int(max_depth), float(accuracy))
        my_cursor.execute(sql, val)
        conn.commit()

        # Increase Count
        count += 1
        logging.info(f"Row {count} inserted")

    logging.info("Results insertion finished.")
