"""
Utility functions
"""
import copy
import logging
import os
import pickle
import sys
from datetime import datetime
from functools import wraps
import warnings

import pandas as pd
import yaml
from decouple import config as d_config
logging.basicConfig(level=logging.INFO)


# Functions
def my_timeit(n_funct):
    """
    My time it function
    """
    @wraps(n_funct)
    def wrapped(*args, **kwargs):
        logging.info(f"Starting function {n_funct.__name__}")
        start = datetime.now()
        response = n_funct(*args, **kwargs)
        duration_sec = (datetime.now() - start).total_seconds()
        duration_min = round(duration_sec / 60, 2)
        logging.info(
            f"{n_funct.__name__} finished.  Duration-sec: {duration_sec} | Duration-min: {duration_min}"
        )
        logging.info("\n")
        return response

    return wrapped


@my_timeit
def write_pandas_to_file(
        data_frame: pd.DataFrame,
        filename: str,
        directory: str
) -> None:
    """
    Generic function to write pandas dataframe to output directory.

    :param data_frame:
    :param filename:
    :param directory:
    """
    # Check if file extension is in the filename
    if ".csv" in filename or ".xls" in filename:
        warnings.warn(message="File name contains file extension")

    # Remove Extension
    filename = filename.replace(".csv", '').replace(".xlsx", '').replace(".xls", "")
    filename = filename + '.csv'
    data_frame.to_csv(os.path.join(directory, filename))
    logging.info(f'Writing {filename} to {directory}')


