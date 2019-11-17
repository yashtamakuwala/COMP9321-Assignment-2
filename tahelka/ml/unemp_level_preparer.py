import pandas as pd

class UnempDataframePreparer:
    UNEMP_BUCKETS = [-1, 2, 4, 6, 8, 100_000]
    def prepare():
        # Load DFU
        path_of_data = open('data/unemployment_clean.csv')
        dfu = pd.read_csv(path_of_data)

        # Get monthly mean of unemp count
        month_columns = dfu.columns[1:]
        dfu['mean_unemp_count'] = dfu[month_columns].mean(axis='columns')

        # Drop month columns
        dfu = dfu.drop(month_columns, axis=1)

        # Mean crime count to crime levels
        dfu['unemp_level'] = pd.cut(dfu['mean_unemp_count'], bins= UnempDataframePreparer.UNEMP_BUCKETS,
                            labels=range(1, len(UnempDataframePreparer.UNEMP_BUCKETS)))
        dfu = dfu.drop(['mean_unemp_count'], axis=1)
        return dfu
