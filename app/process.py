import numpy as np
from app.K_Means_Clustering import Kmeans
import cv2

def resize(image):
    original_shape=image.shape
    new_shape=np.array(original_shape[:2])
    factor=np.min(400/new_shape)
    new_shape=(new_shape*factor).astype(int)
    resized_image = cv2.resize(image, (new_shape[1], new_shape[0]), interpolation=cv2.INTER_AREA)
    new_shape=resized_image.shape
    pixel_values=resized_image.reshape((-1,3))
    return pixel_values,original_shape,new_shape
    
def reconstruct_img(centroids,idx,oshape,nshape):
    reconstructed_image=np.round(centroids[idx]).astype(np.uint8)
    reconstructed_image=reconstructed_image.reshape(nshape)
    reconstructed_image = cv2.resize(reconstructed_image,(oshape[1],oshape[0]), interpolation=cv2.INTER_AREA)
    return reconstructed_image

def process_image(image,k,max_iters):
    vals,oshape,nshape=resize(image)
    clusterer=Kmeans()
    clusterer.fit_kmeans(vals,k,max_iters)
    centroids,idx=clusterer.centroids,clusterer.assigned_centroids
    new_img=reconstruct_img(centroids,idx,oshape,nshape)
    return new_img