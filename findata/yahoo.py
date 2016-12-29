
import pandas as pd
import re
import StringIO
import urllib2


class Yahoo(object):

    # Taken from http://www.jarloo.com/yahoo_finance/
    yahoo_query_params = {
        'dividend_yield': 'y',
        'dividend_per_share': 'd',
        'earnings_per_share': 'e',
        'est_eps_yr': 'e7',
        'est_eps_next_yr': 'e8',
        'ex_dividend_date': 'q',
        'market_cap': 'j1',
        'price_earnings_ratio': 'r',
        'short_ratio': 's7'
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
            df = pd.read_csv(StringIO.StringIO(raw_dat), header=None)
            dfs.append(df)
        ret = pd.concat(dfs)
        return ret

    def query(self, symbols):
        ret = self._fetch_fields(symbols, ''.join(Yahoo.yahoo_query_params.values()))
        ret.columns = Yahoo.yahoo_query_params.keys()
        for col in ['ex_dividend_date']:
            ret[col] = pd.to_datetime(ret[col])
        ret['market_cap'] = [self._convert_market_cap(mc) for mc in ret.market_cap]
        ret['Symbol'] = symbols
        return ret



