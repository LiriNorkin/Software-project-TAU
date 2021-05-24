import argparse
import random
import generateData
import ourAlgorithems
import kmeans_pp
import visualization


if __name__ == '__main__':
    """
    This Python file is used to run the entire project
    """
    max_capacity_n_2 = 200
    max_capacity_K_2 = 20
    max_capacity_n_3 = 200
    max_capacity_K_3 = 20
    max_iter = 300
    parser = argparse.ArgumentParser()
    parser.add_argument("k", type=int, help="number of clusters")
    parser.add_argument("n", type=int, help="number of observations")
    parser.add_argument("rand", type=str, help="Random value")
    args = parser.parse_args()
    rand = True if (args.rand == "True") else False

   # d = random.randint(2,3)
    #
    d=3

    if not rand:
        K = args.k
        n = args.n
        if ((K >= n) or (K <= 0) or (n <= 0)):
            print("invalid inputs")
            exit(0)
    else:
        if d == 2:
            n = random.randrange(max_capacity_n_2//2, max_capacity_n_2)
            K = random.randrange(max_capacity_K_2//2, max_capacity_K_2)
        else:
            n = random.randrange(max_capacity_n_3 // 2, max_capacity_n_3)
            K = random.randrange(max_capacity_K_3 // 2, max_capacity_K_3)
    obs, centers = generateData.generate_points(n, d, K)
    k = ourAlgorithems.NormalizedSpectralClustering(obs, n, rand, K)
    kmeans_pp.kmeansInit(obs, n, k, d, 300)
    visualization.visualizeClusters(obs, n, d, K, centers)














