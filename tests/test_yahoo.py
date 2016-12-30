import unittest

from findata.yahoo import Yahoo


class TestWikiData(unittest.TestCase):

    def setUp(self):
        self.yahoo = Yahoo()

    def tearDown(self):
        pass

    def test_batch_snapshot(self):
        df = self.yahoo.batch_snapshot(['F', 'AAPL'])
        symbols = df.ticker.tolist()
        self.assertTrue('F' in symbols)
        self.assertTrue('AAPL' in symbols)
        self.assertTrue('52w_high' in df.columns)

    def test_historic_dividends(self):
        dividends = self.yahoo.historic_dividends('F')
        self.assertTrue({'Date', 'Dividends'}.issubset(dividends.columns))

    def test_historic_ohlc(self):
        ohlc = self.yahoo.historic_ohlc('F')
        self.assertTrue({'Date', 'Open', 'High', 'Low', 'Close', 'Volume'}.issubset(ohlc.columns))
