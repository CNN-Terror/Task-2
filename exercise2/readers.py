import csv
from image import Image
from PIL import Image
import numpy as np
import os
import exercise2_config as config


# Reads a list of Images from the given csv file.
def ReadFromCsvFile(filename):
  images = []
  with open(filename, 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    for row in csv_reader:
      image = Image()
      image.label = int(row[0])
      image.pixels = [int(pixel) for pixel in row[1:]]
      images.append(image)
  return images

def ReadImages(dir, label):
  images = []
  print(dir)
  for filename in os.listdir(dir) :
    image_path = os.path.join(dir, filename)
    image = Image.open(image_path)
    image_as_array = np.array(image.getdata())
    images.append(image_as_array)
  images = np.insert(images, 0, label, axis=1) 
  return images

# Reads an Image from the given png file.
def ReadFromPngFiles():
  for label in range(10):
    dirTrain = os.path.join(config.TRAIN_PERMUTATED_DATA_FILE, f'{label}')
    dirTest = os.path.join(config.TEST_PERMUTATED_DATA_FILE, f'{label}')
    imagesTrain = ReadImages(dirTrain, label)
    imagesTest = ReadImages(dirTest, label)
    #Delete the output.csv file after each run, because it appends the result at the end of it each time
    with open("../mnist/trainOutput.csv", "a") as f1:
      writer = csv.writer(f1)
      writer.writerows(imagesTrain)
    with open("../mnist/testOutput.csv", "a") as f2:
      writer = csv.writer(f2)
      writer.writerows(imagesTest)
    #input() 
  f1.close()
  f2.close()
