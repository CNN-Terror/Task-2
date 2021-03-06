import numpy as np
from feature import Feature


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
    delta_t = initial_features_for_current_time.t - initial_features_for_previous_time.t
    vx = delta_x / delta_t
    vy = delta_y / delta_t

  return np.array([initial_features_for_current_time.x, 
                   initial_features_for_current_time.y, 
                   initial_features_for_current_time.pressure,
                   vx, 
                   vy],
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