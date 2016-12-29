import unittest

from findata.yahoo import Yahoo


class TestWikiData(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testFetch(self):
        yahoo = Yahoo()

        df = yahoo.query(['F', 'AAPL'])
        symbols = df.ticker.tolist()
        self.assertTrue('F' in symbols)
        self.assertTrue('AAPL' in symbols)
        self.assertTrue('52w_high' in df.columns)
