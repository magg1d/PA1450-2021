"""This module reads all the data"""

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

DATADIR = "../csse_covid_19_daily_reports/"


def date_to_filename(date):
    mm = date.strftime("%m")
    dd = date.strftime("%d")
    yyyy = date.strftime("%Y")
    return mm + "-" + dd + "-" + yyyy + ".csv"


def load_csv(filename):
    """Loads CSV file to Dataframe"""
    filename = DATADIR + filename

    dataframe = pd.DataFrame()
    try:
        dataframe = pd.read_csv(filename)
    except FileNotFoundError:
        return "File not found. Please try again."
    return dataframe


def filter_data(dataframe, filter_type, filter_key):
    try:
        return dataframe.loc[dataframe[filter_type] == filter_key]
    except AttributeError:
        return print("Invalid datafile")


def compare_data(filter_type, filter_key, data_value, start_date, end_date):
    """Shows data over time"""
    data = []
    for curr_date in pd.date_range(start_date, end_date):
        filename = date_to_filename(curr_date)
        partial_data = load_csv(filename)
        filtered_data = filter_data(partial_data, filter_type, filter_key)
        data.append(filtered_data)

    total_data = pd.concat(data)
    total_data.plot(kind='line', x='Last_Update', y=data_value, marker='o', color='mediumvioletred')

    plt.show()


def data_over_time(filter_type, filter_key, data_value, start_date, end_date, interval):
    """Shows how the data has changed over time"""
    data = []
    for curr_date in pd.date_range(start_date, end_date, freq=str(interval)+'D'):
        file1 = date_to_filename(curr_date)
        file2 = date_to_filename(curr_date + dt.timedelta(days=interval))

        df1 = load_csv(file1)
        df2 = load_csv(file2)

        fd1 = filter_data(df1, filter_type, filter_key)
        fd2 = filter_data(df2, filter_type, filter_key)

        val1 = fd1.loc[fd1[filter_type] == filter_key, data_value].values[0]
        val2 = fd2.loc[fd2[filter_type] == filter_key, data_value].values[0]
        change = val2 - val1

        fd2.loc[fd2[filter_type] == filter_key, data_value] = change
        data.append(fd2)

    total_data = pd.concat(data)
    total_data.plot(kind='line', x='Last_Update', y=data_value, marker='o', color='mediumvioletred')
    plt.show()

# compare_data("Province_State", "Blekinge", "Confirmed",dt.datetime(2020, 3, 22), dt.datetime(2021, 4, 8))


data_over_time("Province_State", "Blekinge", "Confirmed", dt.datetime(2021, 1, 1), dt.datetime(2021, 2, 1), 7)

