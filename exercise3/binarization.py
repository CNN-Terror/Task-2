# pip3 install opencv-python numpy matplotlib
import cv2
import matplotlib.pyplot as plt 
import numpy as np
from PIL import Image


# TODO: write a method for binarization, not necessary Otsu

# NOT WORKING
def ApplyOtsu(jpg_image_filename):
  original_image = cv2.imread(jpg_image_filename)
  # _, final_image_pixels = cv2.threshold(original_image, 127, 255, cv2.THRESH_BINARY)

  image_after_blur = cv2.medianBlur(original_image, 5)
  _, final_image_pixels = cv2.adaptiveThreshold(image_after_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

  return Image.fromarray(final_image_pixels)


# Applies KMeans clustering with the given k on the image at the given path 
# and returns the output as a a PIL.Image.
def ApplyKMeansClusteringToImageFile(jpg_image_filename, k=2):
  original_image = cv2.imread(jpg_image_filename)
  pixels = original_image.reshape((-1,3))
  pixels = np.float32(pixels)

  # Define criteria, number of clusters and apply KMeans.
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
  _, label, center = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

  # Convert back into uint8.
  center = np.uint8(center)
  final_image_pixels = center[label.flatten()]
  final_image_pixels = final_image_pixels.reshape((original_image.shape))

  return Image.fromarray(final_image_pixels)


# IN PROGRESS, NOT WORKING/FINISHED. Probably not worth finishing anyway.
# - original_image: PIL.Image
# https://www.thepythoncode.com/article/kmeans-for-image-segmentation-opencv-python
# https://medium.com/towardssingularity/k-means-clustering-for-image-segmentation-using-opencv-in-python-17178ce3d6f3
def ApplyKMeansClusteringToImagePixels(original_image, k=2):
  pixels = []
  for row in range(original_image.height):
    pixel_row = []
    for column in range(original_image.width):
      pixel_row.append(original_image.getpixel((column, row)))
    pixels.append(pixel_row)
  pixels = np.float32(pixels)
  pixel_vals = pixels.reshape((-1,3)) 

  x_size, y_size = original_image.size
  shape = (x_size, y_size, 1)

  # processed_image = Image.new('L', original_image.size, 0)
  # return processed_image

  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85) #criteria
  _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS) 

  centers = np.uint8(centers) # convert data into 8-bit values 
  segmented_data = centers[labels.flatten()] # Mapping labels to center points( RGB Value)
  segmented_image = segmented_data
  # segmented_image = segmented_data.reshape((shape)) # reshape data into the original image dimensions
  plt.imshow(segmented_image)
  plt.show()
  input()
