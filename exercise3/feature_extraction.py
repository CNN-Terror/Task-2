from enum import Enum 


class Method(Enum):
  PIXEL_RATIO = 1


# TODO: write better method/methods to extract features
# Input:
#  - image: PIL.Image
def ExtractFeatures(image, method=Method.PIXEL_RATIO):
  if method == Method.PIXEL_RATIO:
    return __ExtractPixelRatio(image)
  pass


# Counts number of dark pixels/number of light pixels.
# Input:
#  - image: PIL.Image 
# Output:
#  - list of siez image.widht representing the number black pixels/number of white pixels
# for a given column
def __ExtractPixelRatio(image):
  text_color_rgb = sorted(list(dict.fromkeys(image.getcolors())), key=lambda x: x[1])
  _, text_color = text_color_rgb[-1]
  
  # pixels = list(image.getdata())
  features = []
  for column in range(image.width):
    number_of_pixels_for_text = 0
    for row in range(image.height):
      number_of_pixels_for_text = number_of_pixels_for_text + (image.getpixel((column, row)) == text_color)
    features.append(number_of_pixels_for_text/image.height)

  return features
