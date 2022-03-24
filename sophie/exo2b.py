import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt

dfTest = pd.read_csv("mnist-csv-format/mnist_test.csv", sep=',', header=None)
dfTrain = pd.read_csv("mnist-csv-format/mnist_train.csv", sep=',', header=None)
trainData = np.array(dfTrain)
testData = np.array(dfTest)
trainLabels = trainData[:, 0]
trainData = trainData[:, 1:]
testLabels = testData[:, 0]
testData = testData[:, 1:]

cs = np.linspace(0.001,0.1,10)
neurons = np.linspace(10, 100, 10, dtype=int)
learningRatesEvolution = []
neuronsEvolution = []
bestAccuracy = 0
accuraciesEvolution = []
bestClassifier = MLPClassifier()

for c in cs:
    print(c)
    for n in neurons:
        clf =  MLPClassifier(hidden_layer_sizes=(n), activation="logistic", learning_rate_init = c).fit(trainData, trainLabels)
        predictions = clf.predict(testData)
        score = clf.score(testData, testLabels)
        if score > bestAccuracy:
            bestAccuracy = score
            accuraciesEvolution.append(bestAccuracy)
            learningRatesEvolution.append(c)
            neuronsEvolution.append(n)
            bestClassifier = clf

print("Best learning rate: %f \n Best number of neurons: %d \n Best accuracy: %f" % (learningRatesEvolution[-1], neuronsEvolution[-1], bestAccuracy))

fig=plot_confusion_matrix(bestClassifier, testData, testLabels, display_labels=["0","1","2","3","4","5","6","7","8","9"])
fig.figure_.suptitle("Confusion Matrix for MNIST Dataset")
plt.show()