import csv
import time
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score


def csv_extract(file):
    count = 0
    csv_file = open(file)
    extracted = csv.reader(csv_file)

    extracted_class = []
    extracted_data = []
    for row in extracted:
        extracted_class.append(row[0])
        extracted_data.append(row[1:])
        count += 1
        if count > 5000:  # Number of elements we take (to test in a faster way the program)
            break
    csv_file.close()

    return extracted_class, extracted_data


def svm_classifier(data, classes, C_param, kernel_param):
    classifier = svm.SVC(kernel=kernel_param, C=C_param, decision_function_shape='ovo')
    # linear kernel (default would be rbf)
    # one vs one approach

    scores = cross_val_score(classifier, data, classes, cv=5)  # Cross validation of the train set
    print(f"Mean of cross-validation with C = {C_param} : {scores.mean()}")
    classifier.fit(data, classes)

    return classifier


start = time.time()

train_class, train_data = csv_extract('mnist_train.csv')
test_class, test_data = csv_extract('mnist_test.csv')

clf = svm_classifier(train_data, train_class, 10 ** -5, 'linear')  # Build classifier
predicted_class = clf.predict(test_data)  # Predict the class
print(f"Accuracy of our classifier : {accuracy_score(test_class, predicted_class)}")

#clf = svm_classifier(train_data, train_class, 10 ** -5, 'rbf')  # Build classifier
#predicted_class = clf.predict(test_data)  # Predict the class
#print(f"Accuracy of our classifier : {accuracy(test_class, predicted_class)}")


end = time.time()
print(format(end - start))  # Running time
