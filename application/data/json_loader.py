"""Module importing json files to dataframes"""

from pandas import read_json, to_datetime

URL = "https://www.svt.se/special/articledata/3362/owid_vax.json"


def get_start_date(dataframe):
    for index, row in dataframe.iterrows():
        if row["Last_Update"] != row["date0str"]:
            print(row["date0str"])
            return to_datetime(row["date0str"], format='%Y-%m-%d')


def subtract(a, b):
    return a - b


def load_json():
    """Load json and rename columns to fit other datatable"""
    data = read_json(URL)
    data_tidy = data.rename(columns={'eng': 'Country_Region', 'datestr': 'Last_Update'}, inplace=False)
    data_tidy["n_full"] = data_tidy["n_full"].fillna(0).astype(int)
    data_tidy["n_single"] = data_tidy.apply(lambda row : subtract(row['n_total'], row['n_full']), axis=1)
    return data_tidy


def filter_data(dataframe, filter_type, filter_key):
    try:
        return dataframe.loc[dataframe[filter_type] == filter_key]
    except AttributeError:
        return print("Invalid datafile")


if __name__ == "__main__":
    df = load_json()
    df = filter_data(df, "Country_Region", "United Arab Emirates")

    print(get_start_date(df))
    print(df)
    # for index, row in df.iterrows():

        # print(row["Country_Region"], row["Last_Update"], row["n_total"], row["n_full"], row["n_single"])


# date0str = dagen då data började komma in
# n_total = antal vaccinerade
# n_full = antal med 2 doser?
# days_ix = dagar från idag
