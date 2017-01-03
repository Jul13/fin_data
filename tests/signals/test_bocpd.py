import numpy as np
from scipy import stats

from fin_data.signals.bocpd import Student, runlength_max
from fin_data.signals.bocpd import bayesian_online_changepoint_detection


def test_bocpd():
    np.random.seed(234)
    a = stats.norm().rvs(size=200)
    b = stats.norm().rvs(size=200) * 5. + 10.
    data = np.concatenate((a, b))
    print data.shape

    student = Student(20, .1, 1, 0)
    runlengths = bayesian_online_changepoint_detection(data, student, 250.)
    assert runlengths[200, 200] > .9
    assert runlengths[:10, 205].max() > .8
