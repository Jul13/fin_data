#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_findata
----------------------------------

Tests for `findata` module.
"""
import os
import shutil
import sys
import tempfile
import unittest

from findata import findata
from findata import wiki_data


class TestWikiData(unittest.TestCase):

    def setUp(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        self.input_csv = os.path.join(dir, 'resources/WIKI_test.csv')
        self.test_dir = tempfile.mkdtemp()
        self.wiki_data = wiki_data.WikiData(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_snapshot(self):
        self.wiki_data.store_snapshot(self.input_csv)
        df = self.wiki_data.load()
        self.assertEqual(len(df), 9)
        self.assertEqual(len(df.columns), 14)


if __name__ == '__main__':
    unittest.main()
