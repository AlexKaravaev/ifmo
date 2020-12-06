# Import Python modules

import numpy as np
import matplotlib.pyplot as plt
import timeit
import matplotlib
import time
from multiprocessing import Pool


def euclidean(point_1, point_2):
    return np.sqrt(((point_1 - point_2)**2).sum())


class KMeans():
    
    def __init__(self, n_clusters):
        self.n_clusters = n_clusters
    
    def nearest_to_clusters(self, clusters, points):
        return np.argmin([euclidean(points,c) for c in clusters])
    
    def clusterize_points(self, points):

        self.labels_ = [self.nearest_to_clusters(self.clusters_centers, x) for x in X]
   
        indices=[]
        for j in range(self.n_clusters):
            cluster=[]
            for i, l in enumerate(self.labels_):
                if l==j: cluster.append(i)
            indices.append(cluster)
        X_by_cluster = [X[i] for i in indices]
        return X_by_cluster
        
    def compute(self, X):
        
        # Assign random centroids locations
        self.clusters_centers = np.random.permutation(X)[:self.n_clusters]
        
        # We'll make 500 iterations by default 
        for i in range(500):
            
            X_grouped = self.clusterize_points(X)
            new_centers=[c.sum(axis=0)/len(c) for c in X_grouped]
            new_centers = [arr.tolist() for arr in new_centers]
            old_centers=self.clusters_centers
            
    
            if np.all(new_centers == old_centers): 
                self.number_of_iter=i
                break;
            else: 

                self.clusters_centers = new_centers
        self.number_of_iter=i
        return self

    def predict(self, X):
        return self.labels_
    
    
class KMeans_parallel(KMeans):
    def __init__(self, n_clusters, num_cores):
        KMeans.__init__(self,n_clusters)
        self.num_cores = num_cores

    
    # Function that updates centroids and repeats 
    # assign_points_to_cluster until convergence or max_iter is reached
    def compute(self, X):
        
        self.clusters_centers = np.random.permutation(X)[:self.n_clusters]
        
        
        splitted_X=self.partition_data(X, self.num_cores)
        

        for i in range(200):
            # Partition data into chunks based on number of cores 
  
            # Parallel Process for assigning points to clusters 
            p = Pool(self.num_cores)
        
            result=p.map(self.clusterize_points, splitted_X )
            p.terminate()
            p.join()   

            
            X_by_cluster=[]
            for c in range(0,self.n_clusters):
                r=[]
                for p in range(0,self.num_cores):
                    tmp=result[p][c].tolist()
                    r=sum([r, tmp ], [])
                X_by_cluster.append(np.array(r))
            
            new_centers = [c.sum(axis=0)/len(c) for c in X_by_cluster]
            new_centers = [np.array(arr) for arr in new_centers]
            old_centers = self.clusters_centers
            old_centers = [np.array(arr) for arr in old_centers]
      
            if all([np.allclose(x, y) for x, y in zip(old_centers, new_centers)]) :
                self.number_of_iter=i
                break;
            else : 
               self.cluster_centers_ = new_centers
        p.close()
        self.labels_ = [self.nearest_to_clusters(self.clusters_centers, x) for x in X]
   
        self.number_of_iter=i
        return self
     
   
    def partition_data ( self,list_in, n):
        temp = np.random.permutation(list_in)
        result = [temp[i::n] for i in range(n)]
        return result
    
      
if __name__ == "__main__":

    X = np.genfromtxt(r's1.txt', delimiter='    ')

    
    kmeans = KMeans(n_clusters = 15)
    kmeans_p = KMeans_parallel(n_clusters=15, num_cores=12)
    st_time = time.time()
    kmeans.compute(X)
    print(f"Seq for took {time.time() - st_time} seconds")
    label = kmeans.predict(X)
    st_time = time.time()
    kmeans_p.compute(X)
    print(f"Parallel for took {time.time() - st_time} seconds")
    label_p = kmeans_p.predict(X)
 
    X = np.genfromtxt(r'big.txt', delimiter='    ')

    
    kmeans = KMeans(n_clusters = 15)
    kmeans_p = KMeans_parallel(n_clusters=15, num_cores=12)
    st_time = time.time()
    kmeans.compute(X)
    print(f"\nSeq for took {time.time() - st_time} seconds")
    label = kmeans.predict(X)
    st_time = time.time()
    kmeans_p.compute(X)
    print(f"Parallel for took {time.time() - st_time} seconds")
    label_p = kmeans_p.predict(X)