"""
This module is used to create The Weighted Adjacency Matrix,
The Diagonal Degree Matrix **-0.5
and The Normalized Graph Laplacian Matrix
"""
import numpy as np

def createW(obs, n):
    """
    :param obs: data points
    :param n: number of data points
    :return: The Weighted Adjacency Matrix
    """
    W = np.ndarray(shape=(n,n), dtype = np.float32)
    for i in range(n):
        for j in range(i,n):
            if i != j:
                W[i, j] = np.exp(-0.5*np.linalg.norm(obs[i]-obs[j]))
                W[j,i] = W[i,j]
            else:
                W[i,i] = 0
    return W

def createDH(W, n):
    """
    :param W: The Weighted Adjacency Matrix
    :param n: number of data points
    :return: The Diagonal Degree Matrix **-0.5
    """
    DH = np.zeros((n,n), dtype = np.float32)
    for i in range(n):
        optional = np.sqrt(np.sum(W[i]))
        DH[i, i] = 0 if np.absolute(optional) < 0.0001 else 1/optional
    return DH

def createNL(DH, W, n):
    """
    :param DH: The Diagonal Degree Matrix **-0.5
    :param W: The Weighted Adjacency Matrix
    :param n: number of data points
    :return: The Normalized Graph Laplacian Matrix
    """
    return (np.eye(n, dtype = np.float32) - np.matmul(np.matmul(DH,W), DH))




