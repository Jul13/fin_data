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
    w_store.close()
