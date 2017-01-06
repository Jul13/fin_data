import glob
import os
from datetime import datetime

import pandas as pd
from pandas import HDFStore

from fin_data.util.file import latest_filename


class WikiStore(object):
    """
    WikiStore is a HDFStore storage for a Quandl WIKI dataset.

    The Quandl WIKI dataset can be retrieved from: https://www.quandl.com/data/WIKI-Wiki-EOD-Stock-Prices.
    """
    def __init__(self, base_dir, date_index=True):
        self.base_dir = base_dir
        assert os.path.exists(self.base_dir)
        self.date_index = date_index
        self._init()

    def keys(self):
        return self.tickers

    def __getitem__(self, item):
        df = self.store[item]
        if self.date_index:
            df.set_index('date', inplace=True)
        return df


    @staticmethod
    def store_snapshot(base_dir, snapshot_file):
        w_df = pd.read_csv(snapshot_file, parse_dates=[1])
        w_df.columns = [c.replace('-', '_') for c in w_df.columns]
        w_df.set_index('ticker', inplace=True)
        w_df.sort_index(inplace=True)

        snapshot_file = datetime.today().strftime('%Y%m%d')

        with HDFStore(os.path.join(base_dir, '{}.h5'.format(snapshot_file)), 'w',
                      complevel=6, complib='blosc') as store:
            tickers = set(w_df.index)
            for ticker in tickers:
                df = w_df.loc[ticker, :]
                df.reset_index(inplace=True)
                df = df.drop('ticker', 1)

                store[ticker] = df

    def _init(self):
        self.store = HDFStore(latest_filename('{}/*.h5'.format(self.base_dir)))
        self.tickers = [t[1:] for t in self.store.keys()]

    def close(self):
        self.store.close()
