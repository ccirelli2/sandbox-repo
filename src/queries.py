"""
Scratchpad
"""
import os
import sys
import pandas as pd
from sklearn import tree
from decouple import config as d_config

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


