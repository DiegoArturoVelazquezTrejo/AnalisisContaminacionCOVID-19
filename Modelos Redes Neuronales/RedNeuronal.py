import numpy as np
import nnfs

from nnfs.datasets import spiral_data

from matplotlib import pyplot as plt

nnfs.init()

np.random.seed(0)

# Clase layer de una red neuronal
class Layer_Dense:

    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    # Método para calcular la salida de la capa
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases


class Activation_ReLU:

    def forward(self, inputs):
        self.output = np.maximum(0, inputs)


class Activation_Softmax:

    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probabilities

def create_data(points, classes):
    X = np.zeros((points*classes,2))
    Y = np.zeros(points*classes, dtype='uint8')
    for class_number in range(classes):
        ix = range(points*class_number, points*(class_number+1))
        r = np.linspace(0.0, 1, points)
        t = np.linspace(class_number*4, (class_number+1)*4, points) + np.random.randn(points)*0.2
        X[ix] = np.c_[r*np.sin(t*2.5), r*np.cos(t*2.5)]
        Y[ix] = class_number
    return X, Y






X, y = spiral_data(samples=100, classes=3)

layer1 = Layer_Dense(2, 3)
layer2 = Layer_Dense(3, 3)

activation1 = Activation_ReLU()
activation2 = Activation_Softmax()

layer1.forward(X)
activation1.forward(layer1.output)
layer2.forward(activation1.output)
activation2.forward(layer2.output)

print(activation2.output)
'''
x, y = create_data(100, 3)

plt.scatter(x[:, 0], x[:, 1])

plt.show()

plt.scatter(x[:,0], x[:,1], c=y, cmap="brg")

plt.show()
X = [[1, 2, 3, 2.5],
     [2, 5, -1, 2],
     [-1.5, 2.7, 3.3, -0.8]]

print(x, y)
'''
