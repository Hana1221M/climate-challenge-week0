import pandas as pd
import numpy as np

COUNTRIES = ['Ethiopia', 'Kenya', 'Sudan', 'Tanzania', 'Nigeria']

def load_data(data_path):
    dfs = []
    for country in COUNTRIES:
        try:
            df = pd.read_csv(f"{data_path}/{country.lower()}.csv")
            df['Country'] = country
            df.replace(-999, np.nan, inplace=True)
            df['Date'] = pd.to_datetime(df['YEAR'] * 1000 + df['DOY'], format='%Y%j')
            df['Month'] = df['Date'].dt.month
            df.ffill(inplace=True)
            dfs.append(df)
        except FileNotFoundError:
            continue
    return pd.concat(dfs, ignore_index=True)

def filter_data(df, countries, year_range):
    return df[
        (df['Country'].isin(countries)) &
        (df['YEAR'] >= year_range[0]) &
        (df['YEAR'] <= year_range[1])
    ]