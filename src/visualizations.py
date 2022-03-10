"""
Visualization Functions
"""
import os
import sys
import pandas as pd
import numpy as np
from sklearn import tree
from decouple import config as d_config
import logging
import warnings
import matplotlib.pyplot as plt
import seaborn as sns

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


# Functions
def plot_distribution(data_frame: pd.DataFrame, column_name: [str, list], save_fig: bool = False, directory: str = None):
    """
    Generic function to plot histogram of a numeric field.
    Args:
        directory:
        save_fig:
        data_frame:
        column_name:
    """
    if isinstance(column_name, str):
        sns.histplot(data_frame.loc[:, column_name].values)
        plt.title(f"Histogram Plot of {column_name}")
        if save_fig:
            filename = f"wine_hist_{column_name}.png"
            plt.savefig(os.path.join(directory, filename))
            logging.info(f"{filename} written to {DIR_RESULTS}")
        plt.show()
        plt.close()

    if isinstance(column_name, list):
        for col in column_name:
            sns.histplot(data_frame.loc[:, col].values)
            plt.title(f"Histogram Plot of {col}")
            if save_fig:
                filename = f"wine_hist_{col}.png"
                plt.savefig(os.path.join(directory, filename))
                logging.info(f"{filename} written to {DIR_RESULTS}")
            plt.show()
            plt.close()


def correlation_matrix(data_frame: pd.DataFrame, save_fig: bool = False, directory: str = None) -> None:
    """

    Args:
        directory:
        save_fig:
        data_frame:
    """
    # Get Correlation Matrix
    corr = data_frame.corr()
    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})

    if save_fig:
        filename = "wine-correlation-matrix.png"
        plt.savefig(os.path.join(directory, filename))
        logging.info(f"{filename} saved to {directory}")

    plt.title("Wine Dataset - Correlation Matrix")
    plt.tight_layout()
    plt.show()

