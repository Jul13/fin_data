#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_findata
----------------------------------

Tests for `findata` module.
"""
import os
import shutil
import tempfile
import unittest

from fin_data.io import wiki_data


class TestWikiData(unittest.TestCase):

    def setUp(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        self.input_csv = os.path.join(dir, '../resources/WIKI_test.csv')
        self.test_dir = tempfile.mkdtemp()
        self.wiki_data = wiki_data.WikiData(self.test_dir)
        self.wiki_data.store_snapshot(self.input_csv)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_snapshot(self):
        df = self.wiki_data.load()
        self.assertEqual(len(df), 9)
        self.assertEqual(len(df.columns), 14)

    def test_pivot(self):
        df = self.wiki_data.load()
        pivot_dat = wiki_data.WikiData.pivot_dimension(df)
        self.assertListEqual(sorted(pivot_dat.columns.tolist()),
                             list(set((df.ticker.tolist()))))


if __name__ == '__main__':
    unittest.main()
