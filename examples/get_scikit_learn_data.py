"""

"""
# Import Libraries
import os
import sys
from sklearn import datasets
import pandas as pd
from decouple import config as d_config

# Declare Directories
DIR_ROOT = d_config("DIR_ROOT")
DIR_SRC = d_config("DIR_SRC")
DIR_DATA = d_config("DIR_DATA")
DIR_RESULTS = d_config("DIR_RESULTS")
sys.path.append(DIR_ROOT)
sys.path.append(DIR_SRC)

# Import Project Modules
from src import utilities as m_utils

if __name__ == '__main__':
    # Get Data From Scikit
    data_bunch = datasets.load_wine(as_frame=True)
    data = data_bunch['data']
    target = data_bunch['target']
    frame = data_bunch['frame']
    target_names = data_bunch['target_names']
    description = data_bunch['DESCR']
    feature_names = data_bunch['feature_names']
    # Write Data to Data Folder
    m_utils.write_pandas_to_file(data_frame=frame, filename="wine-dataset-raw", directory=DIR_DATA)
    # Write Description to File
    with open(os.path.join(DIR_DATA, "wine-dataset-description.txt"), "w") as my_file:
        my_file.write(description)
        my_file.close()
