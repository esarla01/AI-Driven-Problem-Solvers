import numpy as np
import pandas as pd
import scipy
# from tensorflow import keras
# import tensorflow as tf
#from sklearn.model_selection import train_test_split
import collections
import pathlib
# import tensorflow
# import tensorflow as tf

# from tensorflow.keras import layers
# from tensorflow.keras import losses
# from tensorflow.keras import utils


class ann: 
    labels = []
    features = []

trainingSet = []

# Prepare Data

# Extract the data from the file 
cols = ['Sepal length', 'Sepal width', 'Petal length', 'Petal width', 'Flower Type']
data_set = pd.read_csv('irisData.txt', names=cols)
data_set.head()

# Find the feature and labels in the data set
data = data_set.values
features = data[:,4]
labels = data[:,0:3]

# update labels with integer for the names
for x in range(len(features) - 1):

    if features[x] == 'Iris-setosa':
        features[x] = 1

    elif features[x] == 'Iris-versicolor':
        features[x] = 2
        
    else: 
        features[x] = 2



# Activation Functions -----------------------

# Define the sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Define the derivative of the sigmoid function
def sigmoid_prime(self, x):
    return sigmoid(x) * (1 - sigmoid(x))



    # Training Function -------------------------
    
# Define the training function
def train(X, y, n_hidden_units=10, n_epochs=100000, learning_rate=0.1):
  # Initialize the weights randomly
  W1 = np.random.rand(X.shape[1], n_hidden_units)
  W2 = np.random.rand(n_hidden_units, n_hidden_units)
  W3 = np.random.rand(n_hidden_units, len(label_map))

  # Train the network for n_epochs
  for epoch in range(n_epochs):
    # Forward pass
    L1 = sigmoid(np.dot(X, W1)) # training data random weightlerle carpiliyo
    L2 = sigmoid(np.dot(L1, W2))  # ikinci layera pass edildi sonra .dot = vector operasyonu yapiyor
    L3 = sigmoid(np.dot(L2, W3))
# Layer
    # Compute the error
    error = y - L3

    # Backward pass
    delta_W3 = error * sigmoid_prime(L3)
    delta_W2 = np.dot(L2.T, delta_W3) * sigmoid_prime(L2)
    delta_W1 = np.dot(L1.T, delta_W2) * sigmoid_prime(L1)

    # Update the weights
    W3 += learning_rate * np.dot(L2.T, delta_W3)
    W2 += learning_rate * np.dot(L1.T, delta_W2)
    W1 += learning_rate * np.dot(X.T, delta_W1)

  return W1, W2, W3

# Define the main function
def main():
  # Train the ANN
  W1, W2, W3 = train(X, y)

  # Test the MLP on a few examples
  for i in range(10):
    x = X[i]
    L1 = sigmoid(np.dot(x, W1))
    L2 = sigmoid(np.dot(L1, W2))
    L3 = L3 = sigmoid(np.dot(L2, W3))
    print(np.argmax(L3, axis=1))









    print(features)
    print(labels)


#

# Convert the labels to numeric values
y = np.array([label_map[label] for label in y])

# Define the sigmoid function
def sigmoid(x):
  return 1 / (1 + np.exp(-x))

# Define the derivative of the sigmoid function
def sigmoid_prime(x):
  return sigmoid(x) * (1 - sigmoid(x))

# Define the training function
def train(X, y, n_hidden_units=10, n_epochs=100000, learning_rate=0.1):
  # Initialize the weights randomly
  W1 = np.random.rand(X.shape[1], n_hidden_units)
  W2 = np.random.rand(n_hidden_units, n_hidden_units)
  W3 = np.random.rand(n_hidden_units, len(label_map))

  # Train the network for n_epochs
  for epoch in range(n_epochs):
    # Forward pass
    L1 = sigmoid(np.dot(X, W1)) # training data random weightlerle carpiliyo
    L2 = sigmoid(np.dot(L1, W2))  # ikinci layera pass edildi sonra .dot = vector operasyonu yapiyor
    L3 = sigmoid(np.dot(L2, W3))
# Layer
    # Compute the error
    error = y - L3

    # Backward pass
    delta_W3 = error * sigmoid_prime(L3)
    delta_W2 = np.dot(L2.T, delta_W3) * sigmoid_prime(L2)
    delta_W1 = np.dot(L1.T, delta_W2) * sigmoid_prime(L1)

    # Update the weights
    W3 += learning_rate * np.dot(L2.T, delta_W3)
    W2 += learning_rate * np.dot(L1.T, delta_W2)
    W1 += learning_rate * np.dot(X.T, delta_W1)

  return W1, W2, W3

# Define the main function
def main():
  # Train the ANN
  W1, W2, W3 = train(X, y)

  # Test the MLP on a few examples
  for i in range(10):
    x = X[i]
    L1 = sigmoid(np.dot(x, W1))
    L2 = sigmoid(np.dot(L1, W2))
    L3 = L3 = sigmoid(np.dot(L2, W3))
    print(np.argmax(L3, axis=1))

# Prompt the user for input features and classify the input
while True:
  sepal_length = input('Enter sepal length (in cm): ')
  sepal_width = input('Enter sepal width (in cm): ')
  petal_length = input('Enter petal length (in cm): ')
  petal_width = input('Enter petal width (in cm): ')
  L1 = sigmoid(np.dot([[sepal_length, sepal_width, petal_length, petal_width]], W1))




  