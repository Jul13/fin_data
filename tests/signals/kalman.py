import unittest

from findata.signals.kalman import moving_average


class TestKalman(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testKalman(self):
        m, c = moving_average(range(10))
