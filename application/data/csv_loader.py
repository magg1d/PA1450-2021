"""Module loading CSV dataframes"""
from pandas import DataFrame, read_csv, unique
import os

DATADIR = "application/data_files/"
URL_PATH = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" # + yyyy-mm-dd.csv


def load_csv(filename, src):
    """Loads CSV file to Dataframe"""
    if src =="url":
        filename = URL_PATH + filename
    elif src == "local":
        filename = DATADIR + filename
    else:
        return -1
    dataframe = DataFrame()
    try:
        dataframe = read_csv(filename)
    except FileNotFoundError:
        return "File not found. Please try again."
    return dataframe
https://www.svt.se/special/articledata/3362/fohm_tabeller.json