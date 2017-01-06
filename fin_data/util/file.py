import glob

def latest_filename(pattern):
    files = glob.glob(pattern)
    assert len(files) > 0
    last = sorted(files, reverse=True)[0]
    return last
