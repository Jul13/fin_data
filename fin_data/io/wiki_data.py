import glob
import os
from datetime import datetime

import pandas as pd


class WikiData(object):
    """Interface to the Quandl wikidata available at: https://www.quandl.com/data/WIKI-Wiki-EOD-Stock-Prices"""

    def __init__(self, base_dir):
        self.base_dir = base_dir

    def store_snapshot(self, snapshot_file):
        """
        Stores a snapshot downloaded as CSV file.

        Args:
            snapshot_file (str): path to snapshot file
        """
        df = pd.read_csv(snapshot_file, parse_dates=[1])

        snapshot_file = datetime.today().strftime('%Y%m%d')
        df.to_hdf(os.path.join(self.base_dir, '{}.hdf.zip'.format(snapshot_file)), 'wiki',
                  complib='zlib', complevel=6)

    def load(self):
        """
        Loads the latest available snapshot.

        Returns:
            Dataframe: loaded dataframe.
        """
        wiki_files = glob.glob('{}/*.hdf.zip'.format(self.base_dir))
        assert len(wiki_files) > 0
        last_file = sorted(wiki_files, reverse=True)[0]
        return pd.read_hdf(os.path.join(self.base_dir, last_file))

    @staticmethod
    def pivot_dimension(dat):
        """
        Pivots the data along the 'adj_close' dimension.

        Args:
             dat (DataFrame): loaded wiki data.

        Returns:
            DataFrame: pivoted dataframe.
        """
        return dat.pivot(columns='ticker', values='adj_close')
