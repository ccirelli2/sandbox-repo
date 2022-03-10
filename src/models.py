"""
Visualization Functions
"""
import os
import sys
import pandas as pd
from pandas import DataFrame
from sklearn import tree
from decouple import config as d_config
import logging
import warnings
import matplotlib.pyplot as plt
import graphviz

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import accuracy_score

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

# Models
def single_fit_decision_tree(data_frame: pd.DataFrame, pplot_tree: bool = False, pplot_confusion_matrix: bool = False,
                             max_depth: int = 4):
    """

    Args:
        data_frame (object):
        pplot_tree:
        pplot_confusion_matrix:
        max_depth:

    Returns:

    """
    # Split X & Y Variables
    Y = data_frame.target
    X_columns = data_frame.columns.tolist()
    X_columns.remove("target")
    X = data_frame[X_columns]

    # Split Dataset
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=1234)

    # Fit Model
    clf = tree.DecisionTreeClassifier(max_depth=4)
    clf.fit(X_train, y_train)

    # Visualize Tree
    if pplot_tree:
        tree.plot_tree(clf)
        plt.show()
        #plt.savefig(os.path.join(DIR_RESULTS, "tree-plot.png"))

    # Predict
    y_pred = clf.predict(X_test)
    y_test = y_test.tolist()

    # Visualize Confusion Matrix
    if pplot_confusion_matrix:
        cf_matrix = confusion_matrix(y_test, y_pred)
        print(cf_matrix)

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


def optimize_max_trees(data_frame: pd.DataFrame, max_depth: int = 10, pplot: bool = False) -> DataFrame:
    """

    Args:
        data_frame:
    """
    accuracy_results = {}

    for i in range(1, max_depth):
        accuracy = single_fit_decision_tree(data_frame, max_depth=i)
        accuracy_results[i] = accuracy

    # Create DataFrame
    df_results = pd.DataFrame({})
    df_results["Max_Depth"] = [x for x in range(1, max_depth)]
    df_results["Test_Accuracy"] = [accuracy_results[x] for x in list(accuracy_results)]

    if pplot:
        plt.plot(df_results["Max_Depth"], df_results["Test_Accuracy"])
        plt.grid(b=True)
        plt.title("Decision Tree - Best Depth")
        plt.tight_layout()
        plt.show()

    return df_results




