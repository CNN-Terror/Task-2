import os
from feature_extraction import ExtractFeatures, Feature

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
def GetTrainAndTestSignatureFeatures(train_paths, train_users, test_paths, test_users):
    train_features = []
    test_features = []

    for i in range(len(train_paths)):
        file_to_array_features = fromFileToArray(train_paths[i])
        features = ExtractFeatures(file_to_array_features)
        train_features.append((train_users[i], features))

    for i in range(len(test_paths)):
        file_to_array_features = fromFileToArray(test_paths[i])
        features = ExtractFeatures(file_to_array_features)
        test_features.append((test_users[i], features))
    
    return train_features, test_features
    
    

def GetProcessedInputData():
    gt = ExtractGtAsList()
    
    train_signature_numbers, train_signature_paths = \
        ExtractSignaturePaths(os.path.join('SignatureVerification', 'enrollment'))
    test_signature_numbers, test_signature_paths = \
        ExtractSignaturePaths(os.path.join('SignatureVerification', 'verification'))

    train_signatures, test_signatures = \
        GetTrainAndTestSignatureFeatures(train_signature_paths, train_signature_numbers, test_signature_paths, test_signature_numbers)
  
    return gt, train_signatures, test_signatures


