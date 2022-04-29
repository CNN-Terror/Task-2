from PIL import Image, ImageDraw
from svgpathtools import svg2paths
import numpy as np
from PIL import Image


# Input:
#  - original_image: PIL.image
def __CropImageUpperAndLowerMargins(original_image):
  colors_rgb = sorted(list(dict.fromkeys(original_image.getcolors())), key=lambda x: x[1])
  _, page_color = colors_rgb[-1]

  pixels = np.array(original_image)

  row_index_start = 0
  only_page_color = all(pixel == page_color for pixel in pixels[row_index_start])
  while only_page_color and row_index_start < original_image.height - 1:
    row_index_start += 1
    only_page_color = all(pixel == page_color for pixel in pixels[row_index_start])

  row_index_end = original_image.height - 1
  only_page_color = all(pixel == page_color for pixel in pixels[row_index_end])
  while only_page_color and row_index_end > 0:
    row_index_end -= 1
    only_page_color = all(pixel == page_color for pixel in pixels[row_index_end])

  pixels = pixels[row_index_start:row_index_end + 1]
  return Image.fromarray(pixels)


# Input:
#  - original_image: PIL.image
def __CropImageMargins(original_image):
  altered_image = __CropImageUpperAndLowerMargins(original_image)
  rotated_altered_pixels =  np.rot90(np.array(altered_image))
  rotated_final_image = \
    __CropImageUpperAndLowerMargins(Image.fromarray(rotated_altered_pixels))
  return Image.fromarray(np.rot90(np.array(rotated_final_image), k=3))


# Crops an image from original_image using the given mask.
# The result is a PIL.Image.
# Input:
#  - original_image: PIL.Image
#  - mask_path: 
# Output:
#  - image: PIL.Image
# https://stackoverflow.com/questions/22588074/polygon-crop-clip-using-python-pil
def CropImage(original_image, mask_path):
  # Extract list of points
  mask_points = [(line.start.real, line.start.imag) for line in mask_path]
  mask = Image.new("L", original_image.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.polygon(mask_points, fill=255, outline=None)

  # Use the page color to fill in empty space
  colors_rgb = sorted(list(dict.fromkeys(original_image.getcolors())), key=lambda x: x[1])
  _, page_color_rgb = colors_rgb[-1]
  page_color = page_color_rgb[0]
  background_image = Image.new("L", original_image.size, page_color)

  result = Image.composite(original_image, background_image, mask)

  # Crop margins 
  # https://www.geeksforgeeks.org/python-pil-image-crop-method/
  x = [x for (x, _) in mask_points]
  y = [y for (_, y) in mask_points]
  result = result.crop((min(x), min(y), max(x), max(y)))

  return __CropImageMargins(result)


# Extracts all the word images from the given PIL.Image.
# Returns a list of PIL.Image objects.
def CropAllWordImages(full_page_image, mask_filepath):
  mask, _ = svg2paths(mask_filepath)

  word_images = []
  for mask_path in mask:
    word_images.append(CropImage(full_page_image, mask_path))
  return word_images
