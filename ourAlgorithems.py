"""
This module is used to preform the algorithems of Gram-Shmidt,
QR Iteration, The Eigengap Heuristic, and Normalized Spectral Clustering
"""

import numpy as np
import matrixCreator
import kmeans_pp

e = 0.0001

def gramShmidt(A, n):
    """
    :param A: the initial matrix of size n*n
    :param n: the dimention of the matrix
    :return: matrixes Q and R, such that A = QR,
    Q is orthogonal and R is upper triangular matrix
    """
    U = A.copy()
    R = np.zeros(shape=(n, n), dtype=np.float32)
    Q = np.zeros(shape=(n, n), dtype=np.float32)
    for i in range(n):
        R[i,i] = np.linalg.norm(U[:,i])
        if np.absolute(R[i, i]) < e:
            Q[:, i] = 0
        else:
            Q[:, i] = U[:, i] / R[i, i]
        R[i,i+1:] = Q[:,i] @  U[:,i+1:]
        U[:,i+1:] = U[:,i+1:] - (R[i,i+1:][np.newaxis,:]*Q[:,i][:,np.newaxis])
    return (Q, R)

def QRIteration(A, n):
    """
    :param A: the initial matix of size n*n
    :param n: the dimention of the matrix
    :return: Matrixes Atag, Qtag such that:
    Qtag is orthogonal matrix whose columnsapproach the eigenvectors of A,
    Atag is a diagonal matrix whose diagonal elements approach the eigenvalues of A.
    Each eigenvalue Atag(j,j) corresponds to an eigenvector Qtag(j)
    """
    Atag = A.copy()
    Qtag = np.eye(n, dtype=np.float32)
    for i in range(n):
        Q, R = gramShmidt(Atag, n)
        Atag = np.matmul(R, Q)
        helper = np.matmul(Qtag, Q)
        diff = np.absolute(Qtag) - np.absolute(helper)
        if (diff <= e).all() and (diff >= -e).all():
            return Atag, Qtag
        Qtag = helper
    return Atag, Qtag

def EigengapHeuristic(eigenVals, n):
    """
    :param eigenVals: The eigenvalues of the Normalized Graph Laplacian Matrix
    :param n: The number of eigenvalues
    :return: The k to use according to The Eigengap Heuristic
    """
    deltas = [abs(eigenVals[i] - eigenVals[i-1]) for i in range(1, (n//2)+1)]
    argmax = 0
    for i in range(1, len(deltas)):
        if deltas[i] > deltas[argmax]:
            argmax = i
    return (argmax+1)

def NormalizedSpectralClustering(obs, n, rand, k):
    """
    :param obs: The observation
    :param n: The number of observations
    :param rand: The value of Random
    :param k: The K that was choosen
    :return: The relevent k: K if Random is False, or the Eigengap Heuristic k if Random is True
    """
    #level 1
    W = matrixCreator.createW(obs, n)
    #level 2
    DH = matrixCreator.createDH(W, n)
    NL = matrixCreator.createNL(DH, W, n)
    #level 3
    Atag, Qtag = QRIteration(NL, n)
    diag = np.array([Atag[i, i] for i in range(n)])
    sortedDiag = np.sort(diag)
    if rand:
        k = EigengapHeuristic(sortedDiag, n)
    #level 4
    U = np.zeros(shape=(n, k), dtype=np.float32)
    for i in range(k):
        x = np.where(diag == sortedDiag[i])[0][0]
        U[:, i] = Qtag[:, x]
    #level 5
    T = np.zeros(shape=(n, k), dtype=np.float32)
    for i in range(n):
        norm = np.linalg.norm(U[i,:])
        if np.absolute(norm) < e:
            T[i,:] = 0
        else:
            for j in range(k):
                T[i, j] = U[i, j]/norm
    #level 6+7
    f = open("clusters.txt", "w")
    f.write(str(k))
    f.close()
    kmeans_pp.kmeansInit(T, n, k, k, 300)
    return k

