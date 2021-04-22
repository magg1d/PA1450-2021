"""This module reads all the data"""

from pandas import date_range, to_datetime, concat
from .csv_loader import load_csv
import datetime as dt


def date_to_filename(date):
    """Convert date object to formatted filename-string"""
    mm = date.strftime("%m")
    dd = date.strftime("%d")
    yyyy = date.strftime("%Y")
    return mm + "-" + dd + "-" + yyyy + ".csv"


def filter_data(dataframe, filter_type, filter_key):
    try:
        return dataframe.loc[dataframe[filter_type] == filter_key]
    except AttributeError:
        return print("Invalid datafile")


def compare_data(filter_type, filter_key, start_date, end_date, fetch_by, display):
    """Shows data over time"""
    data = []
    for curr_date in date_range(start_date, end_date):
        # Open each days dataframe
        filename = date_to_filename(curr_date)
        df = load_csv(filename, fetch_by)

        # Filter the dataframe by given params
        fd = filter_data(df, filter_type, filter_key)

        # Remove timestamps from date-column
        if display == "plot":
            fd["Last_Update"] = to_datetime(fd["Last_Update"], format='%Y-%m-%d')
        data.append(fd)

    # All configured data is summed into one dataframe
    total_data = concat(data)
    return total_data


def data_over_time(filter_type, filter_key, data_value, start_date, end_date, interval, fetch_by):
    """Shows how the data has changed over time"""
    data = []
    for curr_date in date_range(start_date, end_date, freq=str(interval)+'D'):
        # Open previous and today's datafile
        file1 = date_to_filename(curr_date - dt.timedelta(days=interval))
        file2 = date_to_filename(curr_date)
        df1 = load_csv(file1, fetch_by)
        df2 = load_csv(file2, fetch_by)

        # Filters the data of both dataframes
        fd1 = filter_data(df1, filter_type, filter_key)
        fd2 = filter_data(df2, filter_type, filter_key)

        # Extracting the values of the filtered data and places the delta into today's dataframe
        val1 = fd1.loc[fd1[filter_type] == filter_key, data_value].values[0]
        val2 = fd2.loc[fd2[filter_type] == filter_key, data_value].values[0]
        fd2.loc[fd2[filter_type] == filter_key, data_value] = val2 - val1

        # Remove timestamps from date-column
        fd2["Last_Update"] = to_datetime(fd2["Last_Update"], format='%Y-%m-%d')
        data.append(fd2)

    # All configured data is then summed into one dataframe
    total_data = concat(data)
    return total_data
