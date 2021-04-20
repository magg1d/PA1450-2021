"""Module loading CSV dataframes"""
from pandas import DataFrame, read_csv
import os

DATADIR = "application/data_files/"


def load_csv(filename):
    """Loads CSV file to Dataframe"""
    print(os.path.abspath("test"))
    filename = DATADIR + filename
    dataframe = DataFrame()
    try:
        dataframe = read_csv(filename)
    except FileNotFoundError:
        return "File not found. Please try again."
    return dataframe
