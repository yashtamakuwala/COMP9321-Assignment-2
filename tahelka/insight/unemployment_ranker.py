from alchemy import Engine
import pandas as pd
import os

class UnemploymentRanker:
    def __init__(self, limit=-1, ascending=True):
        self.limit = limit
        self.ascending = ascending

    def rank(self):
        # Load dataframe
        df = UnemploymentRanker.load_df()

        # Filter to get only available LGAs
        available_lgas = UnemploymentRanker.get_available_lgas()
        df = df[df['lga'].isin(available_lgas)]

        # Get mean of monthly crime count
        month_columns = df.columns[1:]
        df['mean_unemp_rate'] = df[month_columns].mean(axis='columns')

        # Drop month columns
        df = df.drop(month_columns, axis=1)

        # sort & limit
        df = df.sort_values('mean_unemp_rate', ascending=self.ascending)
        if self.limit >= 0:
            df = df[:self.limit]

        # format
        df['mean_unemp_rate'] = df['mean_unemp_rate'].apply(lambda x: round(x, 2))
        df['mean_unemp_rate'] = df['mean_unemp_rate'].astype(str) + '%'


        return df.to_dict(orient='records')

    def load_df():
        root = os.path.abspath(os.curdir)
        path_of_data = os.path.join(root, 'data/unemployment_clean.csv')
        df = pd.read_csv(path_of_data)
        return df.rename({'LGA': 'lga'}, axis=1)

    def get_available_lgas():
        # Get all LGAs in listings
        df = pd.read_sql_table('properties', con=Engine)
        return df['lga'].unique()
