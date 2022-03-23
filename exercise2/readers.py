import csv
from image import Image


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


# Reads an Image from the given png file.
def ReadFromPngFile(filename):
  pass