import pandas as pd


def create_dataframe(weather_list):
    """
    Convert weather data list into a Pandas DataFrame.
    """

    if not weather_list:
        return pd.DataFrame()

    return pd.DataFrame(weather_list)


def clean_data(df):
    """
    Clean and preprocess weather data.
    """

    if df.empty:
        return df

    df = df.dropna().copy()

    return df