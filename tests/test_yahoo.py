import unittest

from findata.yahoo import Yahoo


class TestWikiData(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_batch_snapshot(self):
        yahoo = Yahoo()

        df = yahoo.batch_snapshot(['F', 'AAPL'])
        symbols = df.ticker.tolist()
        self.assertTrue('F' in symbols)
        self.assertTrue('AAPL' in symbols)
        self.assertTrue('52w_high' in df.columns)

    def test_history_dividends(self):
        yahoo = Yahoo()

        dividends = yahoo.history_dividends('F')
        self.assertTrue({'Date', 'Dividends'}.issubset(dividends.columns))
