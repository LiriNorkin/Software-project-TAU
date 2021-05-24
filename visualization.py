"""
This module is used to visualize the result clusters of both algorithms.
It saves the results in a PFD file named clusters.pdf, that includes the
clustering visualization of both algorithms and the descriptive information requested
"""
import pandas as pd
import matplotlib.pyplot as plt

def readCluster(f, obs, couples):
    """
    :param f: The file object containing the clusters of both algorithms
    :param obs: The original observations
    :param couples: The set of couples of observations in the same cluster currently counted
    in both the algorithm and the original data
    :return: The coordinates of the points in this cluster, and the number of common couples in this
    cluster in the algorithm and the original data
    """
    commonCouples = 0
    ser = pd.Series(f.readline().split(','))
    ser[len(ser) - 1] = int(ser[len(ser) - 1])
    for j in range(len(ser)):
        for t in range(j + 1, len(ser)):
            if (int(ser[j]), int(ser[t])) in couples:
                commonCouples += 1
            else:
                couples.add((int(ser[j]), int(ser[t])))
    points = obs.take(ser, axis=0)
    return points, commonCouples

def visualizeClusters(obs, n, d, K, centers):
    """
    :param obs: The original observations
    :param n: The number of observations
    :param d: The dimension of each observation
    :param K: The number of clusters in the generated data
    :param centers: The original cluster of each observation in the generated data
    This function creates the clustering visualization of both algorithms and the descriptive information
    requested, and saves the results in clusters.pdf
    """
    f = open("clusters.txt", "r")
    k = int(f.readline())
    couplesBefore = set()
    clusters_list = [[] for i in range(K)]
    for i in range(n):
        clusters_list[centers[i]].append(i)
    for i in range(K):
        for j in range(len(clusters_list[i])):
            for t in range(j+1, len(clusters_list[i])):
                couplesBefore.add((clusters_list[i][j], clusters_list[i][t]))
    if d == 3:
        fig = plt.figure()
    for j in range(1, 3):
        if d == 2:
            ax = plt.subplot(2, 2, j)
        if d == 3:
            ax = fig.add_subplot(2, 2, j, projection='3d')
        if j == 1:
            ax.set_title('Normalized Spectral Clustering', fontsize=11)
            couples = couplesBefore.copy()
        else:
            ax.set_title('K-means', fontsize=11)
            couples = couplesBefore
        commonCouples = 0
        for i in range(k):
            points, newCouples = readCluster(f, obs, couples)
            commonCouples += newCouples
            if d == 2:
                ax.scatter(points[:, 0], points[:, 1])
            if d == 3:
                ax.scatter3D(points[:, 0], points[:, 1], points[:, 2])
        if j == 1:
            jacSpec = commonCouples/len(couples)

        else:
            jacKmeans = commonCouples/len(couples)
    f.close()

    plt.figtext(0.5, 0.35, "Data was generated from the values:", ha="center", fontsize=12)
    plt.figtext(0.5, 0.29, "n = {0} , k = {1}".format(n, K), ha="center", fontsize=12)
    plt.figtext(0.5, 0.23, "The k that was used for both algorithms was {0}".format(k), ha="center", fontsize=12)
    plt.figtext(0.5, 0.17, "The Jaccard measure for Spectral Clustering: {0}".format(jacSpec), ha="center", fontsize=12)
    plt.figtext(0.5, 0.11, "The Jaccard measure for K-means: {0}".format(jacKmeans), ha="center", fontsize=12)
    plt.rcParams['pdf.fonttype'] = 42
    plt.savefig("clusters.pdf")
