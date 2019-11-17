import pandas as pd

class CrimeDataframePreparer:
    CRIME_BUCKETS = [-1, 250, 500, 1000, 1500, 100_000]
    def prepare():
        # Load DFC
        path_of_data = open('data/crime_clean.csv')
        dfc = pd.read_csv(path_of_data)

        # Get monthly mean of crime count
        month_columns = dfc.columns[1:]
        dfc['mean_crime_count'] = dfc[month_columns].mean(axis='columns')

        # Drop month columns
        dfc = dfc.drop(month_columns, axis=1)

        # Group by LGA
        dfc = dfc.groupby(['LGA']).sum().reset_index()

        # Mean crime count to crime levels
        dfc['crime_level'] = pd.cut(dfc['mean_crime_count'], bins= CrimeDataframePreparer.CRIME_BUCKETS,
                                    labels=range(1, len(CrimeDataframePreparer.CRIME_BUCKETS)))
        dfc = dfc.drop(['mean_crime_count'], axis=1)

        return dfc