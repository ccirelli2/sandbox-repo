"""
Example ETL
"""
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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
from src.connections import mysql_connect
from src import utilities as m_utils
from src.utilities import my_timeit
from src.queries import query_wine
from src import visualizations as my_viz
from src import transformations as my_trans
from src import models as m_models


# Package Settings
pd.set_option('display.max_columns', None)
logging.basicConfig(level=logging.INFO)
warnings.filterwarnings('ignore')

# Instantiate Connection to Database
my_conn = mysql_connect(
            host=d_config("MYSQL_HOST"),
            user_name=d_config("MYSQL_USER"),
            password=d_config("MYSQL_PASSWORD"),
            database="sandbox_onsite"
        )


########################################################################################################################
# Query Data
########################################################################################################################
db_tables = pd.read_sql(sql="SHOW TABLES;", con=my_conn)
df_wine = pd.read_sql(sql="SELECT * FROM wine_raw;", con=my_conn)


########################################################################################################################
# Exploratory Data Analysis
########################################################################################################################
"""
# Visualize Dataset
'Looks like all are of dtype float'
print(df_wine.head())

# Inspect Column Names
'''['alcohol', 'malic_acid', 'ash', 'alcalinity_of_ash', 'magnesium', 'total_phenols', 'flavanoids',
'nonflavanoid_phenols', 'proanthocyanins', 'color_intensity', 'hue', 'od280/od315_of_diluted_wines',
'proline', 'target']
'''
print(df_wine.columns.tolist())

# Dataset Dimensions
'Dataset Dimensions => (180, 14)'
print(f"Dataset Dimensions => {df_wine.shape}")

# Dataset Null Values
'1 row for all columns has null values'
nan_cnt_by_col = df_wine.isna().sum()
print(f"Nan Count By Column => {nan_cnt_by_col}")

# Data Types
'''
All columns are of type float64
'''
data_types = df_wine.dtypes
print(data_types)

# Get Target Values
'Unique target values => [0.0, 1.0, 2.0, nan].  Take note of the nan value'
target_unique = df_wine.target.unique().tolist()
print(f"Unique target values => {target_unique}")

# Let's Look At Distribution of columns
my_viz.plot_distribution(
    data_frame=df_wine,
    column_name=df_wine.columns.tolist(),
    save_fig=True,
    directory=DIR_RESULTS)

# Heat Map
my_viz.correlation_matrix(df_wine, save_fig=True, directory=DIR_RESULTS)
"""

########################################################################################################################
# Data Transformations
########################################################################################################################

# Get Rid of Nan Values
data_frame = my_trans.remove_nan_rows(data_frame=df_wine)

# Change Target Value to Int
data_frame["target"] = list(map(lambda x: int(x), data_frame.target.values))

########################################################################################################################
# Train Model
########################################################################################################################

# Fit Single Model

accuracy = m_models.single_fit_decision_tree(
    data_frame=data_frame,
    pplot_tree=True,
    pplot_confusion_matrix=True,
    max_depth=4)


# Get Optimal Tree Dept# h
df_accuracy = m_models.optimize_max_trees(data_frame, max_depth=12, result_to_file=True, directory=DIR_RESULTS)




