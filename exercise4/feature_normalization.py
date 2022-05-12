from enum import Enum
from sklearn.preprocessing import minmax_scale
from feature_extraction import Feature


class NormalizationMethod(Enum):
  NONE = 0
  MIN_MAX = 1


# Input:
# - features: list of Feature objects
# - method: NormalizationMethod
# https://www.codecademy.com/article/normalization
def NormalizeFeatures(initial_features, method):
  if method is NormalizationMethod.MIN_MAX:
    return __ApplyMinMaxNormalization(initial_features)
  return initial_features


def __ApplyMinMaxNormalization(initial_features):
  features_as_nparray = [[feature.t,
                          feature.x,
                          feature.y,
                          feature.pressure,
                          feature.penup,
                          feature.azimuth,
                          feature.inclination] for feature in initial_features]
  normalized_features_as_nparray = \
    minmax_scale(features_as_nparray[:], feature_range=(0,1))
  normalized_features = [Feature(normalized_feature[0],
                                 normalized_feature[1],
                                 normalized_feature[2],
                                 normalized_feature[3],
                                 normalized_feature[4],
                                 normalized_feature[5],
                                 normalized_feature[6]) for normalized_feature in normalized_features_as_nparray]
  return normalized_features
  

if __name__ == "__main__":
  features = [
    Feature(0.0000, 15.8200, 16.0100, 334.000000, 1.000000, 299.000000, 63.000000),
    Feature(0.0100, 16.2300, 16.3000, 417.000000, 0.000000, 303.000000, 62.000000),
    Feature(0.0010, 15.5300, 16.2000, 416.000000, 0.500000, 301.000000, 62.500000),
  ]
  print(features[0].x)
  normalized_features = NormalizeFeatures(features, NormalizationMethod.MIN_MAX)
  print(normalized_features[0].x)