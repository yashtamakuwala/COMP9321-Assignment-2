from alchemy import Engine
import pandas as pd

class RatingRanker:
    def __init__(self, limit=-1, ascending=False):
        self.limit = limit
        self.ascending = ascending

    def rank(self):
        df = RatingRanker.load_df()

        # group by lga & rename mean price
        df = df.groupby('lga').mean().reset_index()
        df = df.rename({'rating': 'mean_rating'}, axis=1)

        # sort & limit
        df = df.sort_values('mean_rating', ascending=self.ascending)
        if self.limit >= 0:
            df = df[:self.limit]

        # format
        df['mean_rating'] = df['mean_rating'].apply(lambda x: round(x, 2))

        return df.to_dict(orient='records')

    def load_df():
        # Load dataframe
        df = pd.read_sql_table('properties', con=Engine)

        # Get needed columns only
        columns = ['lga', 'rating']
        df = df[columns]

        return df
