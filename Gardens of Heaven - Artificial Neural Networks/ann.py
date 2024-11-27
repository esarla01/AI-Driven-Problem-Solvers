# # Import necessary libraries
# import numpy as np

# # Load the Iris data set from the file
# data = np.loadtxt('irisData.txt')

# # Shuffle the data
# np.random.shuffle(data)

# # Separate the features from the labels
# X = data[:, :4]
# y = data[:, 4]

# Map the class labels to numeric values
label_map = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
label_map_inv = {v: k for k, v in label_map.items()}


print(len(label_map))
# # Convert the labels to numeric values
# y = np.array([label_map[label] for label in y])

# # Define the sigmoid function
# def sigmoid(x):
#   return 1 / (1 + np.exp(-x))

# # Define the derivative of the sigmoid function
# def sigmoid_prime(x):
#   return sigmoid(x) * (1 - sigmoid(x))

# # Define the training function
# def train(X, y, n_hidden_units=10, n_epochs=100000, learning_rate=0.1):
#   # Initialize the weights randomly
#   W1 = np.random.rand(X.shape[1], n_hidden_units)
#   W2 = np.random.rand(n_hidden_units, n_hidden_units)
#   W3 = np.random.rand(n_hidden_units, len(label_map))

#   # Train the network for n_epochs
#   for epoch in range(n_epochs):
#     # Forward pass
#     L1 = sigmoid(np.dot(X, W1))
#     L2 = sigmoid(np.dot(L1, W2))
#     L3 = sigmoid(np.dot(L2, W3))

#     # Compute the error
#     error = y - L3

#     # Backward pass
#     delta_W3 = error * sigmoid_prime(L3)
#     delta_W2 = np.dot(L2.T, delta_W3) * sigmoid_prime(L2)
#     delta_W1 = np.dot(L1.T, delta_W2) * sigmoid_prime(L1)

#     # Update the weights
#     W3 += learning_rate * np.dot(L2.T, delta_W3)
#     W2 += learning_rate * np.dot(L1.T, delta_W2)
#     W1 += learning_rate * np.dot(X.T, delta_W1)

#   return W1, W2, W3

# # Define the main function
# def main():
#   # Train the ANN
#   W1, W2, W3 = train(X, y)

#   # Test the MLP on a few examples
#   for i in range(10):
#     x = X[i]
#     L1 = sigmoid(np.dot(x, W1))
#     L2 = sigmoid(np.dot(L1, W2))
#     L3 = L3 = sigmoid(np.dot(L2, W3))
#     print(np.argmax(L3, axis=1))

# # Prompt the user for input features and classify the input
# while True:
#   sepal_length = input('Enter sepal length (in cm): ')
#   sepal_width = input('Enter sepal width (in cm): ')
#   petal_length = input('Enter petal length (in cm): ')
#   petal_width = input('Enter petal width (in cm): ')
#   L1 = sigmoid(np.dot([[sepal_length, sepal_width, petal_length, petal_width]], W1))




  