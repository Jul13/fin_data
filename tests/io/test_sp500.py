import tempfile

from fin_data.io import sp500


def test_sp500():
    test_dir = tempfile.mkdtemp()

    sp500.store_snapshot(test_dir)
    df = sp500.load_latest(test_dir)

    out_cols = sorted(df.columns.tolist())
    assert out_cols == ['sector', 'subsector', 'ticker'], out_cols
