import numpy as np


class Feature:
  def __init__(self, t, x, y, pressure, penup, azimuth, inclination):
    self.t = t
    self.x = x
    self.y = y
    self.pressure = pressure
    self.penup = penup
    self.azimuth = azimuth
    self.inclination = inclination


  t = None
  x = None
  y = None
  pressure = None
  penup = None
  azimuth = None
  inclination = None


# Input:
# - initial_feature: Feature
# Output:
# - list of features
def ExtractFeaturesForPoint(initial_features_for_current_time, initial_features_for_previous_time):
  vx = 0
  vy = 0

  if initial_features_for_previous_time is not None:
    # TODO: check if this is correct, probably not
    delta_x = initial_features_for_current_time.x - initial_features_for_previous_time.x
    delta_y = initial_features_for_current_time.y - initial_features_for_previous_time.y
    vx = delta_x / initial_features_for_current_time.t
    vy = delta_y / initial_features_for_current_time.t

  return np.array([initial_features_for_current_time.x, 
                   initial_features_for_current_time.y, 
                   vx, 
                   vy, 
                   initial_features_for_current_time.pressure],
                   dtype=float)


# Input:
# - list of Feature objects
# Output:
# - list of lists
def ExtractFeatures(all_inital_features):
  final_features = [ExtractFeaturesForPoint(all_inital_features[0], None)]
  for index in range(1, len(all_inital_features)):
    new_features = ExtractFeaturesForPoint(all_inital_features[index], all_inital_features[index - 1])
    final_features.append(new_features)
  return np.array(final_features, dtype=float)


if __name__ == "__main__":
  initial_features = [
    Feature(0.0000, 15.8200, 16.0100, 334.000000, 1.000000, 299.000000, 63.000000),
    Feature(0.0100, 16.2300, 16.3000, 417.000000, 0.000000, 303.000000, 62.000000),
  ]
  features = ExtractFeatures(initial_features)
  print(features)