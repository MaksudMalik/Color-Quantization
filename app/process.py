import numpy as np
from K_Means_Clustering import Kmeans
import cv2

def get_pixel_vals(image):
    original_shape=image.shape
    pixel_values=image.reshape((-1,3))
    return pixel_values,original_shape
    
def reconstruct_img(centroids,idx,shape):
    reconstructed_image=np.round(centroids[idx]).astype(np.uint8)
    reconstructed_image=reconstructed_image.reshape(shape)
    return reconstructed_image

def process_image(image,k,max_iters):
    vals,shape=get_pixel_vals(image)
    clusterer=Kmeans()
    clusterer.fit_kmeans(vals,k,max_iters)
    centroids,idx=clusterer.centroids,clusterer.assigned_centroids
    new_img=reconstruct_img(centroids,idx,shape)
    return new_img