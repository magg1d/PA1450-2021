"""Module loading CSV dataframes"""
from pandas import DataFrame, read_csv

URL_PATH = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/" # + yyyy-mm-dd.csv


def load_csv(filename):
    """Loads CSV file to Dataframe"""
    filename = URL_PATH + filename
    dataframe = DataFrame()
    try:
        dataframe = read_csv(filename)
    except FileNotFoundError:
        return "File not found. Please try again."
    return dataframe
