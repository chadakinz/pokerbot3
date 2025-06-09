import numpy as np
from attr import *


class NeuralNetwork:
    """Neural Network with one hidden layer"""
    def __init__(self, data_size, classification_size, hidden_layer_size, dec_rate = 10):
        """
        Initialize the weights and hyperparameters of the neural network using arbitrary data size
        """
        self.hidden_layer_weights = np.random.uniform(0, 1, size=(data_size + 1, hidden_layer_size))
        self.output_layer_weights = np.random.uniform(0, 1, size=(hidden_layer_size + 1, classification_size))
        self.dec_rate = dec_rate

    def initialize_data(self, data, classification):
        """
        Gives the neural network the data to create the training and testing sets
        """

        self.x_train = data
        self.y_train = classification
        self.x_train = self.x_train.T
        self.y_train = self.y_train.T


    def train(self, r):
        #print(self.hidden_layer_weights)
        #print(self.output_layer_weights)
        #print(self.x_train.shape)
        #pr(self.y_train.shape)

        for j in range(r):
            for i in range(self.x_train.shape[1]):
                X = self.x_train[:, i]
                Y = self.y_train[:, i]
                Z, A = self.input_to_hidden(X)
                T = self.hidden_to_output(Z)
                g = self.softmax(T)

                dg_dT = np.diag(g/T) - np.outer(g, g/T)
                drel_dA = np.array([1 if x > 0 else 0 for x in A])
                dR_dg = -2 * (Y - g)
                S = dg_dT @ dR_dg
                L = np.matmul(self.output_layer_weights[1:], S) * drel_dA
                """  
                print(F"dRel_da: {drel_dA}")
                print()
                print(F"T: {T}")
                print()
                print(f"dg_dT: {dg_dT}")
                print()
                print(f"dR_dg: {dR_dg}")
                print()
                print(f"L: {L}")
                print()
                print(f"S: {S}")
                print()
                print(f"dec rate: {self.dec_rate}")
                """
                self.output_layer_weights[1:] -=  (self.dec_rate * 10) * np.matmul(Z[:, np.newaxis], (S[:, np.newaxis].T))
                self.output_layer_weights[0] -= (self.dec_rate * 10) * S

                self.hidden_layer_weights[0] -= (self.dec_rate * 10) * L
                self.hidden_layer_weights[1:] -= (self.dec_rate * 10) * np.matmul(X[:, np.newaxis], L[:, np.newaxis].T)


    def input_to_hidden(self, X):
        """
        Applies weights and biases to the input vector X and returns vector Z = vector reLU(A)
        Returns both Z and A for partial derivative calculations in gradient descent.
        :param X:
        :return: Z, A
        """
        biases = self.hidden_layer_weights[0]
        weights = self.hidden_layer_weights[1:]

        #print(weights.T)
        A = biases + (weights.T @ X)
        reLU = np.vectorize(lambda x: np.maximum(0, x))
        Z = reLU(A)
        return Z, A

    def hidden_to_output(self, Z):
        """
        Takes vector Z output from the hidden layer, and outputs vector T.
        """
        biases = self.output_layer_weights[0]
        weights = self.output_layer_weights[1:]
        T = biases + (weights.T @ Z)
        normalize = np.vectorize(lambda x: np.maximum(1, x))
        return normalize(T)
    def softmax(self, T):
        """
        Apply softmax activation to our output vector T and get the distribution of our classification predictions
        as probabilities from [0, 1]. Apply the log function to vector T in order to prevent divergence and
        return vector g.
        """
        exp_T = np.exp(np.log(T))
        return exp_T / np.sum(exp_T)


class ValueNetwork(NeuralNetwork):
    def __init__(self, data_size, classification_size, hidden_layer_size, dec_rate = 10):
        super().__init__(data_size, classification_size, hidden_layer_size, dec_rate)

    def train(self, r):
        for j in range(r):
            for i in range(self.x_train.shape[1]):
                X = self.x_train[:, i]  # Input vector (features)
                Y = self.y_train[:, i]  # Target value(s)

                # Forward pass
                Z, A = self.input_to_hidden(X)  # Hidden layer output (Z), pre-activation (A)
                T = self.hidden_to_output(Z)  # Output layer (regression output)

                # Compute gradient of MSE loss w.r.t. output T
                dR_dT = 2 * (T - Y)  # Assuming Y and T are both vectors

                # Backpropagate to hidden layer
                dT_dZ = self.output_layer_weights[1:]  # Shape: [hidden_size, output_size]
                dR_dZ = dT_dZ @ dR_dT  # shape: [hidden_size]
                dZ_dA = np.array([1 if a > 0 else 0 for a in A])  # ReLU derivative
                dR_dA = dR_dZ * dZ_dA  # Element-wise multiply

                # Update output layer weights
                self.output_layer_weights[1:] -= self.dec_rate * np.outer(Z, dR_dT)
                self.output_layer_weights[0] -= self.dec_rate * dR_dT

                # Update hidden layer weights
                self.hidden_layer_weights[1:] -= self.dec_rate * np.outer(X, dR_dA)
                self.hidden_layer_weights[0] -= self.dec_rate * dR_dA
    def regret_matching(self, I):
        Z, A = self.input_to_hidden(I)
        T = self.hidden_to_output(Z)
        if np.all(T <= 0):
            return np.ones_like(T) / len(T)

        positive_regrets = np.maximum(T, 0)
        total = positive_regrets.sum()

        if total == 0:
            return np.ones_like(T) / len(T)

        return positive_regrets / total

class PolicyNetwork(NeuralNetwork):
    def __init__(self, data_size, classification_size, hidden_layer_size, dec_rate = 10):
        super().__init__(data_size, classification_size, hidden_layer_size, dec_rate)

    def sample_action(self, I):
        Z, A = self.input_to_hidden(I)
        T = self.hidden_to_output(Z)
        g = self.softmax(T)
        return np.random.choice(len(g), p = g), g
