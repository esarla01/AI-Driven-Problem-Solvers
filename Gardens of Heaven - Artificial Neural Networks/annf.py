import numpy as np
import pandas as pd

# Load data
import scipy
# from tensorflow import keras
import tensorflow as tf
import collections
import pathlib

# Import necessary modules
import numpy as np
import pandas as pd
import random

import matplotlib.pyplot as plt

#Importing data
Titles = ['Sepal length', 'Sepal width', 'Petal length', 'Petal width', 'Flower Type']
data_set = pd.read_csv('irisData.txt', names=Titles)
data_set.head()
data = data_set.values
#Shuffling the dataset in first axis (rows) before splitting

shuffledList = random.sample(list(data), len(data))
ShuffledData = np.array(shuffledList)

#Assing data to features and labels arrays
features = np.array(ShuffledData[:,:4])
labels = np.array(ShuffledData[:,4])

#Changing data type inside the array so that sigmoid function can work
features = features.astype('float64')

#Hot encoding the labels
HotEncodedLabels = np.ones((len(labels),3))
NumberOfRows = len(labels)
for rowNumber in range(NumberOfRows):

    if labels[rowNumber] == 'Iris-setosa':
        HotEncodedLabels[rowNumber,:] = np.array([1,0,0])

    elif labels[rowNumber] == 'Iris-versicolor':
        HotEncodedLabels[rowNumber, :] = np.array([0,1,0])

    else:
        HotEncodedLabels[rowNumber, :] = np.array([0,0,1])
Classes = ['Iris-setosa','Iris-versicolor', 'Iris-virginica']
SplitRatioTrain = 0.80
SplitRatioTest = 0.10
SplitRatioTestValidate = 0.10

EndIndexTrain = round(NumberOfRows*SplitRatioTrain)
EndIndexTest = EndIndexTrain + round(NumberOfRows*SplitRatioTest)

trainFeatures = features[0:EndIndexTrain,:]
testFeatures = features[EndIndexTrain:EndIndexTest,:]

trainLabels = HotEncodedLabels[0:EndIndexTrain,:]
testLabels = HotEncodedLabels[EndIndexTrain:EndIndexTest,:]

print(np.shape(trainFeatures))
print(np.shape(testFeatures))

print(np.shape(trainLabels))
print(np.shape(testLabels))

#Hyperparameters
trainingSetSize = np.shape(trainLabels)[0]
learning_rate = 0.15
Epoch = 4000

#Network architecture
NumberOfInputs = 4
HiddenSize = 2
NumberOfCategories = 3

ResultsTable = pd.DataFrame(columns=["MSE", "Accuracy"])

# Initial Weights:
np.random.seed(8)
W1 = np.random.normal(scale=0.5, size=(NumberOfInputs, HiddenSize))
W2 = np.random.normal(scale=0.5, size=(HiddenSize , NumberOfCategories))


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def MSE(Prediction, TrueVal):
    return ((Prediction - TrueVal)**2).sum() / (2*len(Prediction))

def Accuracy(Prediction, TrueVal):
    Accuracy = Prediction.argmax(axis=1) == TrueVal.argmax(axis=1)
    return Accuracy.mean()


for TrainCycle in range(Epoch):

    #FF
    Layer1 = sigmoid(np.dot(trainFeatures, W1))

    Layer2 = sigmoid(np.dot(Layer1, W2))

    #MSE Error
    mse = MSE(Layer2, trainLabels)
    acc = Accuracy(Layer2, trainLabels)
    ResultsTable=ResultsTable.append({"MSE":mse, "Accuracy":acc},ignore_index=True )

    print("MSE:",mse)
    print("Accuracy:",acc)

    #Backpropagation
    dW1 = (Layer2 - trainLabels) * Layer2 * (1 - Layer2)
    dW2 = (np.dot(dW1, W2.T)) * Layer1 * (1 - Layer1)

    UpdateW2 = np.dot(Layer1.T, dW1) / trainingSetSize
    UpdateW1 = np.dot(trainFeatures.T, dW2) / trainingSetSize

    W2 = W2 - learning_rate * UpdateW2
    W1 = W1 - learning_rate * UpdateW1

ResultsTable.MSE.plot(title="Mean Squared Error")
plt.show()
ResultsTable.Accuracy.plot(title="Accuracy")
plt.show()


#Testing training data with the model (W1, W2)

#Feedforward calculation

TestLayer1 = sigmoid(np.dot(testFeatures, W1))
TestOutputLayer = sigmoid(np.dot(TestLayer1, W2))

TestAcc = Accuracy(TestOutputLayer, testLabels)
print('Accuracy on the test data is', TestAcc)


SepalLength = input ("Please enter a sepal length: ")
SepalWidth = input ("Please enter a sepal width: ")
PetalLength = input ("Please enter a petal length: ")
PetalWidth = input ("Please enter a petal width: ")


ManualEntryFeatures = testFeatures[0]
ManualEntryFeatures[0] = SepalLength
ManualEntryFeatures[1] = SepalWidth
ManualEntryFeatures[2] = PetalLength
ManualEntryFeatures[3] = PetalWidth

ManualEntryLayer1 = sigmoid(np.dot(ManualEntryFeatures, W1))
TestOutputLayer = sigmoid(np.dot(ManualEntryLayer1, W2))

FlowerType = TestOutputLayer
print('Probability for each category based on your entries is', FlowerType)
print('The model predicts that the type of Iris plant is', Classes[np.argmax(FlowerType)])