"""Module importing json files to dataframes"""

from pandas import read_json

URL = "https://www.svt.se/special/articledata/3362/owid_vax.json"


def load_json():
    """Load json and rename columns to fit other datatable"""
    data = read_json(URL)
    data_tidy = data.rename(columns={'eng': 'Country_Region', 'datestr': 'Last_Update'}, inplace=False)
    data_tidy["n_full"] = data_tidy["n_full"].fillna(0).astype(int)
    return data_tidy


def filter_data(dataframe, filter_type, filter_key):
    try:
        return dataframe.loc[dataframe[filter_type] == filter_key]
    except AttributeError:
        return print("Invalid datafile")


if __name__ == "__main__":
    df = load_json()
    df = filter_data(df, "Country_Region", "Albania")
    for index, row in df.iterrows():
        print(row["Country_Region"], row["Last_Update"], row["n_total"], row["n_full"])


# date0str = dagen då data började komma in
# n_total = antal vaccinerade
# n_full = antal med 2 doser?
# days_ix = dagar från idag
