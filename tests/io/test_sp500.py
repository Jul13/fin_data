import tempfile
from datetime import datetime

from fin_data.io import sp500


def test_sp500():
    test_dir = tempfile.mkdtemp()

    sp500.store_snapshot(test_dir)
    df = sp500.load_latest(test_dir)

    out_cols = sorted(df.columns.tolist())
    assert out_cols == ['date_first_added', 'sector', 'subindustry', 'ticker'], out_cols
    mmm = df[df.ticker == 'MMM']
    assert mmm.date_first_added.tolist()[0] == datetime(1970, 1, 1), mmm.date_first_added.tolist()[0]
    akam = df[df.ticker == 'AKAM']
    assert akam.date_first_added.tolist()[0] == datetime(2007, 7, 12), type(akam.date_first_added.tolist()[0])
