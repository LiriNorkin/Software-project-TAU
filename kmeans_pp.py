"""
This module is used to preform the Kmeans Plus Plus algorithm and saves the results to clusters.txt
while using the C extension - mykmeanssp
"""

import mykmeanssp as ckm
import numpy as np

def k_means_pp(obs, N, k, d):
    """
    :param obs: The observations
    :param N: The number of observations
    :param k: The number of clusters
    :param d: The dimension of the observations
    :return: The first k clusters according to the Kmeans Plus Plus algorithm
    """
    np.random.seed(0)
    rand = np.random.choice(N, 1)
    indexes = np.array([rand[0]])
    centroids = np.zeros(shape=(k,d))
    centroids[0] = obs[rand[0]]
    dists = np.array([np.sum((obs[i] - centroids[0])**2) for i in range(N)])
    for j in range(1,k):
        dists = np.array([min(dists[i], np.sum((obs[i] - centroids[j-1])**2)) for i in range(N)])
        sums = np.sum(dists)
        probs = np.array([dists[i]/sums for i in range(N)])
        rand = np.random.choice(N,1,p=probs)
        centroids[j] = obs[rand[0]]
        indexes = np.append(indexes, rand[0])
    return indexes

def kmeansInit(obs, N, k, d, MAX_ITER):
    """
    :param obs: The observations
    :param N: The number of observations
    :param k: The number of clusters
    :param d: The dimension of the observations
    :param MAX_ITER: The maximum number of iterations in the Kmeans algorithm
    This function calls the k_means_pp function in order to get the first k clusters,
    and calls the c extension mykmeanssp in order to preform the kmeans algorithm and
    save the results to clusters.txt
    """
    first = k_means_pp(obs, N, k, d)
    to_c_obs = obs.tolist()
    to_c_first = first.tolist()
    to_send = [k, N, d, MAX_ITER, to_c_first, to_c_obs]
    ckm.connect(to_send)

