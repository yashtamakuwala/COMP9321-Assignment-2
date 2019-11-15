from alchemy import Engine
import pandas as pd

class PriceRanker:
    def __init__(self, limit=-1, ascending=True):
        self.limit = limit
        self.ascending = ascending

    def rank(self):
        df = PriceRanker.load_df()

        # group by lga & rename mean price
        df = df.groupby('lga').mean().reset_index()
        df = df.rename({'price': 'mean_price'}, axis=1)

        # sort & limit
        df = df.sort_values('mean_price', ascending=self.ascending)
        if self.limit >= 0:
            df = df[:self.limit]

        return df.to_dict(orient='records')

    def load_df():
        # Load dataframe
        df = pd.read_sql_table('properties', con=Engine)

        # Get needed columns only
        columns = ['lga', 'price']
        df = df[columns]

        return df
