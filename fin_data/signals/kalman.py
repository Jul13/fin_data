from pykalman import KalmanFilter


def moving_average(values, transition_covariance=.01):
    kf = KalmanFilter(transition_matrices = [1],
                      observation_matrices = [1],
                      initial_state_mean = 0,
                      initial_state_covariance = 1,
                      observation_covariance=1,
                      transition_covariance=transition_covariance)
    means, covs = kf.filter(values)
    return means, covs
