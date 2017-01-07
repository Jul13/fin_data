import os
import tempfile

import datetime

from fin_data.io.wiki_store import WikiStore


def test_wiki_store():
    dir = os.path.dirname(os.path.abspath(__file__))
    input_csv = os.path.join(dir, '../resources/WIKI_test.csv')
    test_dir = tempfile.mkdtemp()

    WikiStore.store_snapshot(test_dir, input_csv)

    w_store = WikiStore(test_dir)

    assert len(w_store.keys()) == 2
    df = w_store['A']
    assert df.index.min() == datetime.datetime(1999, 11, 18)

    ac = w_store.tickers_column(w_store.keys())
    assert ac.columns.tolist() == ['A', 'ZUMZ']

    ac_filter = w_store.tickers_column(w_store.keys(), fun_filter=lambda df: df[df.index.year == 2000])
    assert ac_filter.columns.tolist() == ['A', 'ZUMZ']
    assert ac_filter.index.year.max() == 2000
    assert ac_filter.index.year.min() == 2000
    w_store.close()
