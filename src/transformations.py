"""
Visualization Functions
"""
import os
import sys
import pandas as pd
from sklearn import tree
from decouple import config as d_config
import logging
import warnings

# Declare Directories
DIR_ROOT = d_config("DIR_ROOT")
DIR_DATA = d_config("DIR_DATA")
DIR_SRC = d_config("DIR_SRC")
DIR_RESULTS = d_config("DIR_RESULTS")
sys.path.append(DIR_ROOT)
sys.path.append(DIR_SRC)

# Import Project Modules
from src import utilities as m_utils
from src.utilities import my_timeit

# Package Settings
pd.set_option('display.max_columns', None)
logging.basicConfig(level=logging.INFO)
warnings.filterwarnings('ignore')

# Transformations
@my_timeit
def remove_nan_rows(data_frame: pd.DataFrame) -> pd.DataFrame:
    """

    Args:
        data_frame:
    """
    logging.info(f"Dimensions prior to transformation => {data_frame.shape}")
    data_frame = data_frame.dropna()
    logging.info(f"Dimensions after to transformation => {data_frame.shape}")
    return data_frame


@my_timeit
def transform_column_datatypes(
        data_frame: pd.DataFrame,
        target_columns: list,
        target_datatype: str) -> pd.DataFrame:
    """
    Transform column data type
    :param target_datatype: Options ("str", "float", "int", "bool")
    :param data_frame:
    :param target_columns:
    """
    for column in target_columns:
        if target_datatype.upper() == "FLOAT":
            data_frame[column] = list(map(lambda x: float(x), data_frame.loc[:, column]))

        if target_datatype.upper() == "INT":
            data_frame[column] = list(map(lambda x: int(str(x).replace(',', '').replace('.', '')), data_frame.loc[:, column]))

        if target_datatype.upper() == "STR":
            data_frame[column] = list(map(lambda x: str(x), data_frame.loc[:, column]))

    return data_frame