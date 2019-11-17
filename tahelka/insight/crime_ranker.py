from alchemy import Engine
import pandas as pd
import os

class CrimeRanker:
    def __init__(self, limit=-1, ascending=True):
        self.limit = limit
        self.ascending = ascending

    def rank(self):
        # Load dataframe
        df = CrimeRanker.load_df()

        # Filter to get only available LGAs
        available_lgas = CrimeRanker.get_available_lgas()
        df = df[df['lga'].isin(available_lgas)]

        # Get mean of monthly crime count
        month_columns = df.columns[1:]
        df['mean_crime_count'] = df[month_columns].mean(axis='columns')

        # Drop month columns
        df = df.drop(month_columns, axis=1)

        # Group by LGA
        df = df.groupby(['lga']).sum().reset_index()

        # sort & limit
        df = df.sort_values('mean_crime_count', ascending=self.ascending)
        if self.limit >= 0:
            df = df[:self.limit]

        # format
        df['mean_price'] = df['mean_crime_count'].apply(lambda x: round(x, 2))
        df['mean_price'] = '$' + df['mean_crime_count'].astype('str')


        return df.to_dict(orient='records')

    def load_df():
        root = os.path.abspath(os.curdir)
        path_of_data = os.path.join(root, 'data/crime_clean.csv')
        df = pd.read_csv(path_of_data)
        return df.rename({'LGA': 'lga'}, axis=1)

    def get_available_lgas():
        # Get all LGAs in listings
        df = pd.read_sql_table('properties', con=Engine)
        return df['lga'].unique()
