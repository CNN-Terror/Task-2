from PIL import Image, ImageDraw
from svgpathtools import svg2paths


# Crops an image from original_image using the given mask.
# The result is a PIL.Image.
# - original_image: PIL.Image
# - mask_path: 
# https://stackoverflow.com/questions/22588074/polygon-crop-clip-using-python-pil
def CropImage(original_image, mask_path):
  # Extract list of points
  mask_points = [(line.start.real, line.start.imag) for line in mask_path]
  mask = Image.new("L", original_image.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.polygon(mask_points, fill=255, outline=None)

  all_white_image = Image.new("L", original_image.size, 255)

  result = Image.composite(original_image, all_white_image, mask)

  # Crop margins 
  # https://www.geeksforgeeks.org/python-pil-image-crop-method/
  x = [x for (x, _) in mask_points]
  y = [y for (_, y) in mask_points]
  result = result.crop((min(x), min(y), max(x), max(y)))

  return result


# Extracts all the word images from the given PIL.Image.
# Returns a list of PIL.Image objects.
def CropAllWordImages(full_page_image, mask_filepath):
  mask, _ = svg2paths(mask_filepath)

  word_images = []
  for mask_path in mask:
    word_images.append(CropImage(full_page_image, mask_path))
  return word_images
