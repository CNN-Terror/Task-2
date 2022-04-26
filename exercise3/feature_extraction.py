from enum import Enum


class Method(Enum):
  BLACK_PIXEL_RATIO = 1
  UPPER_CONTOUR = 2
  LOWER_CONTOUR = 3
  PIXEL_TRANSITIONS = 4
  BLACK_PIXEL_RATIO_LC_UP = 5


# Input:
#  - image: PIL.Image
#  - methods: list of methods (features we want to extract),
#         ex: methods = [Method.BLACK_PIXEL_RATIO, Method.LOWER_CONTOUR]
# Output:
#  - vector of normalized features (using min-max normalization)
def ExtractFeatures(image, methods):
  features_vector = []
  for method in methods:
    if method == Method.BLACK_PIXEL_RATIO:
      features_vector.append(__ExtractBlackPixelRatio(image))
    if method == Method.UPPER_CONTOUR:
      features_vector.append(__ExtractUpperContour(image)/image.height)
    if method == Method.LOWER_CONTOUR:
      features_vector.append((__ExtractLowerContour(image) + 1)/image.height)
    if method == Method.PIXEL_TRANSITIONS:
      features_vector.append(__ExtractPixelTransitions(image)/(image.height*image.width - 1))
    if method == Method.BLACK_PIXEL_RATIO_LC_UP:
      features_vector.append(__ExtractBlackPixelRatioLcUp(image))

  return features_vector
  pass

# Input:
#  - image: PIL.Image 
# Output:
#  - number of black pixels/total number of pixels
def __ExtractBlackPixelRatio(image):
  text_color_rgb = sorted(list(dict.fromkeys(image.getcolors())), key=lambda x: x[1])
  nb_of_black_pixels, _ = text_color_rgb[0]

  return nb_of_black_pixels/(image.height * image.width)

# Input:
#  - image: PIL.Image
# Output:
#  - row index of the highest black pixel
def __ExtractUpperContour(image):
  text_color_rgb = sorted(list(dict.fromkeys(image.getcolors())), key=lambda x: x[1])
  _, text_color = text_color_rgb[0]

  for row in range(image.height):
    for column in range(image.width):
      if image.getpixel((column, row)) == text_color:
        return row

  return image.height

# Input:
#  - image: PIL.Image
# Output:
#  - row index of the lowest black pixel
def __ExtractLowerContour(image):
  text_color_rgb = sorted(list(dict.fromkeys(image.getcolors())), key=lambda x: x[1])
  _, text_color = text_color_rgb[0]

  for row in range(image.height):
    for column in range(image.width):
      if image.getpixel((column, (image.height - 1) - row)) == text_color:
        return (image.height - 1) - row

  return -1

# Input:
#  - image: PIL.Image
# Output:
#  - number of transitions between black and white pixels
def __ExtractPixelTransitions(image):
  text_color_rgb = sorted(list(dict.fromkeys(image.getcolors())), key=lambda x: x[1])
  _, text_color = text_color_rgb[0]

  nb_transitions = 0
  current = image.getpixel((0, 0))

  for row in range(image.height):
    for column in range(image.width):
      if image.getpixel((column, row)) != current:
        current = image.getpixel((column, row))
        nb_transitions += 1
  return nb_transitions

# Input:
#  - image: PIL.Image
# Output:
#  - number of black pixels/number of pixels between the upper and the lower contour
def __ExtractBlackPixelRatioLcUp(image):
  text_color_rgb = sorted(list(dict.fromkeys(image.getcolors())), key=lambda x: x[1])
  nb_of_black_pixels, _ = text_color_rgb[0]
  lower_contour = __ExtractLowerContour(image)
  upper_contour = __ExtractUpperContour(image)
  nb_of_pixels_between = ((lower_contour - upper_contour + 1) * image.width)
  return nb_of_black_pixels/nb_of_pixels_between