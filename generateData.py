"""
This module is used to generate data points according to the user's request and save a data file
"""
from sklearn.datasets import make_blobs
import numpy as np

def generate_points(n, d, K):
    """
    :param n: number of data points
    :param d: number of dimentions
    :param K: numbers of centers
    :return: list of data points
    this function generates the data points at random according to the paramaters
    and creates a data file with the observations
    """
    obs, centers = make_blobs(n_samples=n, centers=K, n_features=d)
    obs = obs.astype(np.float32)
    f = open("data.txt", "w")
    for i in range(len(obs)):
        line = ""
        for j in range(d):
            line += str(obs[i][j])
            line += ","
        line += str(centers[i])
        line += '\n'
        f.write(line)
    f.close()
    return obs, centers