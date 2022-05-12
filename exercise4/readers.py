import os
from feature_extraction import ExtractFeatures
from feature_normalization import NormalizeFeatures
from feature import Feature


# Extracts gt.
# Output:
#  - gt: list of (signature_id, signature_type [g or f])
def ExtractGtAsList():
  gt = []
  gt_path = os.path.join('SignatureVerification', 'gt.txt')
  with open(gt_path) as gt_file:
    for line in gt_file.readlines():
      signature_id, signature_type = line.strip().split(sep=" ")
      gt.append((signature_id, signature_type))

  return gt

#  - list of size n containing user numbers
#  - list of size n containing paths to original txt signatures
def ExtractSignaturePaths(file_path):
  signature_numbers = []
  signature_paths = []

  for file in os.listdir(file_path):
    if file.endswith(".txt"):
        signature_numbers.append(file[0:4] + file[-6:-4])
        signature_paths.append(os.path.join(file_path, file))
  return signature_numbers, signature_paths

#To get a 2d array of Feature from each signature file
def fromFileToArray(fileName):
    array = []
    file = open(fileName, "r")
    for line in file.readlines():
        subArray = line.split(' ')
        subArrayInt = list(map(float, subArray))
        # * stand for argument unpacking
        array.append(Feature(*subArrayInt))
    file.close()
    return array

#To get a list of user and its 2d array signature features
# Input:
# - normalization_method: NormalizationMethod
def GetTrainAndTestSignatureFeatures(train_paths, train_users, test_paths, test_users, normalization_method):
    ordered_train_features = []
    ordered_test_features = []
    number_of_train_features_per_id = {}
    number_of_test_features_per_id = {}

    for i in range(len(train_paths)):
        file_to_array_features = fromFileToArray(train_paths[i])
        features = ExtractFeatures(file_to_array_features)
        ordered_train_features.append(features)
        number_of_train_features_per_id[train_users[i]] = len(features)

    for i in range(len(test_paths)):
        file_to_array_features = fromFileToArray(test_paths[i])
        features = ExtractFeatures(file_to_array_features)
        ordered_test_features.append(features)
        number_of_test_features_per_id[test_users[i]] = len(features)
    
    # Normlaize data
    ordered_train_features =\
         [feature for feature_list in ordered_train_features for feature in feature_list]
    ordered_test_features =\
         [feature for feature_list in ordered_test_features for feature in feature_list]
    normalized_ordered_train_features = \
        NormalizeFeatures(ordered_train_features, normalization_method)
    normalized_ordered_test_features = \
        NormalizeFeatures(ordered_test_features, normalization_method)

    # Build output 
    train_features = []
    lower_index = 0
    upper_index = 0
    for i in range(len(train_paths)):
        lower_index = upper_index
        upper_index = upper_index + number_of_train_features_per_id[train_users[i]]
        train_features.append((train_users[i], normalized_ordered_train_features[lower_index:upper_index]))

    test_features = []
    lower_index = 0
    upper_index = 0
    for i in range(len(test_paths)):
        lower_index = upper_index
        upper_index = upper_index + number_of_test_features_per_id[test_users[i]]
        test_features.append((test_users[i], normalized_ordered_test_features[lower_index:upper_index]))

    return train_features, test_features
    

# Input:
# - normalization_method: NormalizationMethod
def GetProcessedInputData(normalization_method, is_test_mode):
    gt = ExtractGtAsList()
    
    train_signature_numbers, train_signature_paths = \
        ExtractSignaturePaths(os.path.join('SignatureVerification', 'enrollment'))
    test_signature_numbers, test_signature_paths = \
        ExtractSignaturePaths(os.path.join('SignatureVerification', 'verification'))
    
    if is_test_mode is True:
        train_signature_numbers = [train_signature_numbers[0]]
        train_signature_paths = [train_signature_paths[0]]
        test_signature_numbers = [test_signature_numbers[0]]
        test_signature_paths = [test_signature_paths[0]]

    train_signatures, test_signatures = \
        GetTrainAndTestSignatureFeatures(train_signature_paths, 
                                         train_signature_numbers, 
                                         test_signature_paths, 
                                         test_signature_numbers, 
                                         normalization_method)
  
    return gt, train_signatures, test_signatures


