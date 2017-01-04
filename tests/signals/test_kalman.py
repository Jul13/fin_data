import unittest

from fin_data.signals.kalman import moving_average


class TestKalman(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testKalman(self):
        x = range(100)
        m, c = moving_average(x, transition_covariance=1.)
        assert  (m[-1] - c[-1])[0] <= x[-1] <= (m[-1] + c[-1])[0]
