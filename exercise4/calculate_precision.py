import numpy
import sklearn.metrics
from distance_normalization import normalizeDistances

def calculate_scores(y_true, y_pred):
    r = numpy.flip(sklearn.metrics.confusion_matrix(y_true, y_pred))
    #print(r)

    precision = sklearn.metrics.precision_score(y_true=y_true, y_pred=y_pred, pos_label="g")
    #print(precision)

    recall = sklearn.metrics.recall_score(y_true=y_true, y_pred=y_pred, pos_label="g")
    #print(recall)

    return [r, precision, recall]

def calculate_results(distances, train_signatures, gt_list, threshold = 0.25):
    normalized_distances = normalizeDistances(distances)
    normalized_distances_dict = normalized_distance_dict(normalized_distances, threshold)
    signature_results = merge_genuine_signature_results(normalized_distances_dict, train_signatures)
    y_pred = get_predictions(signature_results)
    scores = calculate_scores(list(gt_list.values()),list(y_pred.values()))

    return scores + [y_pred]


def get_predictions(signature_results):
    # we have 5 distances, majority_vote=3 (believe what most people believe. (Please, never ever do so in real life).
    majority_vote = 3
    y_pred = {}

    for i in signature_results:
        y_pred[i] = "g" if signature_results[i] < majority_vote else "f"
    return y_pred


def merge_genuine_signature_results(new_dict, train_signatures):
    merged_results_dict = {}
    for i in range(len(train_signatures)):
        if (i % 5 == 0):
            first_and_second_genuine_writers_results = mergeDictionary(new_dict[train_signatures[i][0]], new_dict[train_signatures[i + 1][0]])
            third_and_fourth_genuine_writers_results = mergeDictionary(new_dict[train_signatures[i + 2][0]], new_dict[train_signatures[i + 3][0]])
            merged_results = mergeDictionary(third_and_fourth_genuine_writers_results, mergeDictionary(new_dict[train_signatures[i + 4][0]], first_and_second_genuine_writers_results))
            merged_results_dict.update(merged_results)
            i = i + 4
    return merged_results_dict


def normalized_distance_dict(normalized_distances, threshold):
    new_dict = {}
    for k in normalized_distances:
        new_dict[k] = {}
        for key, value in normalized_distances[k].items():
            # Hardcoded value, what to consider as margin, how exactly to choose this value?
            if value < threshold:
                new_dict[k][key] = 0
            else:
                new_dict[k][key] = 1
    return new_dict

def mergeDictionary(dict_1, dict_2):
   dict_3 = {**dict_1, **dict_2}
   for key, value in dict_3.items():
       if key in dict_1 and key in dict_2:
               dict_3[key] = value + dict_1[key]
   return dict_3