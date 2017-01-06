import os
from datetime import datetime

from bs4 import BeautifulSoup
import pandas as pd
import urllib2

from fin_data.util.file import latest_filename


SITE = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def store_snapshot(base_dir):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(SITE, headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, 'html5lib')

    table = soup.find('table', {'class': 'wikitable sortable'})
    sectors = []
    subsectors = []
    tickers = []
    for row in table.findAll('tr'):
        col = row.findAll('td')
        if len(col) > 0:
            sector = str(col[3].string.strip()).lower().replace(' ', '_')
            subsector = str(col[4].string.strip()).lower().replace(' ', '_')
            ticker = str(col[0].string.strip())

            sectors.append(sector)
            subsectors.append(subsector)
            tickers.append(ticker)
    sp500 = pd.DataFrame({'ticker': tickers, 'sector': sectors, 'subsector': subsectors})

    snapshot_file = datetime.today().strftime('%Y%m%d')
    out_file = os.path.join(base_dir, '{}.csv'.format(snapshot_file))

    sp500.to_csv(out_file, index=False)


def load_latest(base_dir):
    return pd.read_csv(latest_filename('{}/*.csv'.format(base_dir)))

