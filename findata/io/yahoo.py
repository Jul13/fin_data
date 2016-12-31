import urllib
from datetime import date
import pandas as pd
import urllib2

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class Yahoo(object):

    # Taken from http://www.jarloo.com/yahoo_finance/
    yahoo_query_params = {
        'ticker': 's',
        'average_daily_volume': 'a2',
        'dividend_yield': 'y',
        'dividend_per_share': 'd',
        'earnings_per_share': 'e',
        'est_eps_yr': 'e7',
        'est_eps_next_yr': 'e8',
        'ex_dividend_date': 'q',
        'market_cap': 'j1',
        'price_earnings_ratio': 'r',
        'short_ratio': 's7',
        'volume': 'v',
        '52w_low': 'j',
        '52w_high': 'k'
    }

    def __init__(self, chunk_size=500):
        self.chunk_size = chunk_size
        self.market_cap_pattern = '(\d+[\.]\d+)([MB])'

    def _convert_market_cap(self, str_value):
        if type(str_value) != str:
            return -1.
        last_char = str_value[-1]
        if last_char in ['B', 'M']:
            base = float(str_value[:-1])
            multiplier = 10.**9 if last_char == 'B' else 10.**6
            return base * multiplier
        return float(str_value)

    def _fetch_fields(self, symbols, fields):
        def chunker(symbols):
            i = 0
            while i < len(symbols):
                count_chunk = min(self.chunk_size, len(symbols) - i)
                yield symbols[i:(i + count_chunk)]
                i += count_chunk
        dfs = []
        for chunk in chunker(symbols):
            request = 'http://download.finance.yahoo.com/d/quotes.csv?s={}&f={}'.format(','.join(chunk), fields)
            raw_dat = urllib2.urlopen(request).read()
            df = pd.read_csv(StringIO(raw_dat), header=None)
            dfs.append(df)
        ret = pd.concat(dfs)
        return ret

    def batch_snapshot(self, tickers):
        """
        Retrieves financial information for a batch of stock symbols.

        Args:
            tickers (list<str>): list of stock symbols
        Returns:
            pandas.Dataframe: dataframe with one row per symbol.
        """
        ret = self._fetch_fields(tickers, ''.join(Yahoo.yahoo_query_params.values()))
        ret.columns = Yahoo.yahoo_query_params.keys()
        for col in ['ex_dividend_date']:
            ret[col] = pd.to_datetime(ret[col])
        ret['market_cap'] = [self._convert_market_cap(mc) for mc in ret.market_cap]
        return ret

    def _history_call(self, ticker, from_date, to_date, params):
        base_url = 'http://ichart.finance.yahoo.com/table.csv'
        params.update({'s': ticker,
                  'a': from_date.day,
                  'b': from_date.month,
                  'c': from_date.year,
                  'd': to_date.day,
                  'e': to_date.month,
                  'f': to_date.year
                  })
        url = '{}?{}'.format(base_url, urllib.urlencode(params))
        raw_dat = urllib2.urlopen(url).read()
        df = pd.read_csv(StringIO(raw_dat), parse_dates=[0])
        return df


    def historic_ohlc(self, ticker, from_date=date(2010, 1, 1), to_date=date.today()):
        """
        Extracts an OHLC dataframe for the given ticker.

        Args:
            ticker (str): stock symbol
            from_date (date): start date
            to_date (date): end date
        """
        return self._history_call(ticker, from_date, to_date, {'g': 'd'})

    def historic_dividends(self, ticker, from_date=date(2010, 1, 1), to_date=date.today()):
        """
        Extracts the dividend payout history for an individual stock.

        Args:
            ticker (str): stock symbol
            from_date (date): start date
            to_date (date): end date
        Returns:
            pandas.DataFrame: dataframe with dates and dividends.
        """
        return self._history_call(ticker, from_date, to_date, {'g': 'v'})





