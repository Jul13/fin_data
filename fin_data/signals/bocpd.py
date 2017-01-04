import numpy as np
from scipy import stats


class BayesianPdf(object):
    """
    Abstract interface which captures new evidence in a Bayesian framework, updating parameters of the underlying pdf.
    """
    def pdf(self, x):
        raise NotImplementedError
    def update_statistics(self, data):
        raise NotImplementedError


class Student(BayesianPdf):
    """
    Posterior distribution of a set of Gaussian variables.
    """
    def __init__(self, alpha, beta, tau, mu):
        self.alpha0 = self.alpha = np.array([alpha])
        self.beta0 = self.beta = np.array([beta])
        self.tau0 = self.tau = np.array([tau])
        self.mu0 = self.mu = np.array([mu])

    def pdf(self, data):
        """
        Returns the likelihoold of the data given the current estimation of the hyperparameters.

        Args:
            data (float): input positions to evaluate.

        Returns:
            numpy.array: likelihood for each of the underlying states of the hyperparameters.
        """
        return stats.t.pdf(x=data,
                           df=2*self.alpha,
                           loc=self.mu,
                           scale=np.sqrt(self.beta * (self.tau + 1) / (self.alpha * self.tau)))

    def update_statistics(self, data):
        """
        update_statistics applies posterior update rules at:
        http://www.stat.columbia.edu/~cook/movabletype/mlm/CONJINTRnew%2BTEX.pdf

        Beware! Method with side-effects, it updates the underlying hyperparameters.
        """
        muT0 = np.concatenate((self.mu0, (self.tau * self.mu + data) / (self.tau + 1)))
        tauT0 = np.concatenate((self.tau0, self.tau + 1.))
        alphaT0 = np.concatenate((self.alpha0, self.alpha + 0.5))
        betaT0 = np.concatenate((
            self.beta0,
            self.beta + (self.tau * (data - self.mu)**2) / (2. * (self.tau + 1.))))

        self.mu = muT0
        self.tau = tauT0
        self.alpha = alphaT0
        self.beta = betaT0


def runlength_max(runlengths):
    """
    Takes an array of runlengths (as returned by bayesian_online_changepoint_detection and returns maxima per time.

    Args:
        runlengths (np.array): 2D array of runlengths probabilities
    Returns:
        argmax (np.array): values with maxima for the runlength sequence.
    """
    n = runlengths.shape[1]
    ret = np.zeros(n + 1)
    for t in xrange(runlengths.shape[1]):
        ret[t] = runlengths[:, t].argmax()
    return ret


def bayesian_online_changepoint_detection(vals, dist, lambda_hazard):
    """
    Implements bayesian changepoint detection according to the algorithm in [1].

    References:
        1. R. Adams, D. MacKay, "Bayesian Online Changepoint Detection", https://arxiv.org/abs/0710.3742

    Args:
        vals (np.array): array of input values
        dist (ExponentialDistribution): instance of ExponentialDistribution class.
        lambda_hazard (float): Hazard constant.
    Returns:
        run_lengths (np.array): 2-d distribution of run-lengths (run-length, time)
    """
    run_lengths = np.zeros((len(vals) + 1, len(vals) + 1))
    run_lengths[0, 0] = 1.

    for t, v in enumerate(vals):
        # 3. Evaluate predictive probability.
        predictive_p = dist.pdf(v)

        hazard = 1. / lambda_hazard * np.ones((1 + t,))

        # 4. Calculate growth probabilities.
        run_lengths[1:(t + 2), t + 1] = run_lengths[:(t + 1), t] * predictive_p * (1. - hazard)

        # 5. Calculate changepoint probabilities.
        run_lengths[0, t + 1] = np.sum(run_lengths[:(t + 1), t] * predictive_p * hazard)

        # 6. Calculate evidence.
        evidence = np.sum(run_lengths[:, t + 1])

        # 7. Determine run-length distribution.
        run_lengths[:, t + 1] = run_lengths[:, t + 1] / evidence

        # 8. Update statistics
        dist.update_statistics(v)

    return run_lengths

