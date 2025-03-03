import numpy as np

class Kmeans:
    def __init__(self):
        self.centroids=None
        self.assigned_indexes=None

    def initialize_centroid(self,X,k):
        n_samples = X.shape[0]
        centroids = np.zeros((k, X.shape[1]))
        centroids[0] = X[np.random.randint(n_samples)]
        for i in range(1, k):
            dist = np.min(np.linalg.norm(X[:, np.newaxis] - centroids[:i], axis=2), axis=1)
            prob = dist / np.sum(dist)
            centroids[i] = X[np.random.choice(n_samples, p=prob)]
        return centroids
    
    def assign_centroid(self, X, centroids):
        dists = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        return np.argmin(dists, axis=1)

    def compute_new_centroids(self,X,assigned_centroids,k):
        centroids = np.array([X[assigned_centroids == i].mean(axis=0) for i in range(k)])
        return centroids

    def fit_kmeans(self,X,k,max_iters=15):
        initial_centroids=self.initialize_centroid(X,k)
        centroids=initial_centroids
        for i in range (max_iters):
            #print(i+1)
            assigned_centroids=self.assign_centroid(X,centroids)
            new_centroids=self.compute_new_centroids(X,assigned_centroids,k)
            if np.all(centroids==new_centroids):
                break
            centroids=new_centroids
        self.centroids=centroids
        self.assigned_centroids=assigned_centroids
        return

