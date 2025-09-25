import numpy as np


class NeuralNetwork:
    """Neural Network with one hidden layer"""
    def __init__(self, data_size, classification_size, hidden_layer_size, dec_rate = 10):
        """
        Initialize the weights and hyperparameters of the neural network using arbitrary data size
        """
        self.hidden_layer_weights = np.random.normal(
            0, np.sqrt(1 / ( (data_size))),
            size=(data_size + 1, hidden_layer_size)
        )

        self.output_layer_weights = np.random.normal(
            0, np.sqrt(1 / ( (hidden_layer_size))),
            size=(hidden_layer_size + 1, classification_size)
        )

        self.dec_rate = dec_rate
        self.batch_size = 1
        self.alpha = .01

    def initialize_data(self, data, classification):
        """
        Gives the neural network the data to create the training and testing sets
        """
        self.x_train = data
        self.y_train = classification



    def train(self, r, memory, batch_size):

        for j in range(r):
            memory.shuffle()
            for i in range(0, len(memory), batch_size):
                data, train, dec_rate = memory.sample_batch(i, min(len(memory), i + batch_size))
                self.batch_size =   min(batch_size, len(memory) - i)

                self.initialize_data(np.array(data), np.array(train))

                self.dec_rate = 1/dec_rate


                X = self.x_train
                Y = self.y_train
                Z, A = self.input_to_hidden(X)
                T = self.hidden_to_output(Z)
                g = self.softmax(T)

                dR_dg = g - Y
                sum_term = np.sum(dR_dg * g, axis=1, keepdims=True)

                dZ_dA =  np.where(A > 0, 1.0, self.alpha)

                dR_dT = g * (dR_dg - sum_term)
                dR_dZ = dR_dT @ self.output_layer_weights[1:].T
                dR_dA = dR_dZ * dZ_dA
                dR_dHW = X[:, :, None] * dR_dA[:, None, :]


                dR_dOW =  Z[:, :, None] * dR_dT[:, None, :]


                self.output_layer_weights[1:] -=  (1/6) * (self.dec_rate ) * np.mean(dR_dOW, axis=0)
                self.output_layer_weights[0] -= (1/6) * (self.dec_rate ) * np.mean(dR_dT, axis=0)

                self.hidden_layer_weights[0] -= (1/6) * (self.dec_rate ) * np.mean(dR_dA, axis=0)
                self.hidden_layer_weights[1:] -= (1/6) * (self.dec_rate ) * np.mean(dR_dHW, axis=0)


    def input_to_hidden(self, X):
        """
        Applies weights and biases to the input vector X and returns vector Z = vector reLU(A)
        Returns both Z and A for partial derivative calculations in gradient descent.
        :param X:
        :return: Z, A
        """

        biases = np.tile(self.hidden_layer_weights[0], (self.batch_size, 1))
        weights = self.hidden_layer_weights[1:]


        A = biases + (X @ weights)

        Z = np.where(A > 0, A, self.alpha * A)

        return Z, A

    def hidden_to_output(self, Z):
        """
        Takes vector Z output from the hidden layer, and outputs vector T.
        """
        biases = np.tile(self.output_layer_weights[0], (self.batch_size, 1))
        weights = self.output_layer_weights[1:]
        T = biases + (Z @ weights)
        return T
    def softmax(self, T):
        """
        Apply softmax activation to our output vector T and get the distribution of our classification predictions
        as probabilities from [0, 1]. Apply the log function to vector T in order to prevent divergence and
        return vector g.
        """

        max_vals = np.max(T, axis=1, keepdims=True)

        T_stable = T - max_vals


        exp_T = np.exp(T_stable)

        sum_exp = np.sum(exp_T, axis=1, keepdims=True)

        return exp_T / sum_exp

    def single_input_to_hidden(self, X):
        """
        Applies weights and biases to the input vector X and returns vector Z = vector reLU(A)
        Returns both Z and A for partial derivative calculations in gradient descent.
        :param X:
        :return: Z, A
        """
        biases = self.hidden_layer_weights[0]
        weights = self.hidden_layer_weights[1:]

        # print(weights.T)
        A = biases + (weights.T @ X)
        Z = np.where(A > 0, A, self.alpha * A)
        return Z, A

    def single_hidden_to_output(self, Z):
        """
        Takes vector Z output from the hidden layer, and outputs vector T.
        """
        biases = self.output_layer_weights[0]
        weights = self.output_layer_weights[1:]
        T = biases + (weights.T @ Z)
        return T

    def single_softmax(self, T):
        """
        Apply softmax activation to our output vector T and get the distribution of our classification predictions
        as probabilities from [0, 1]. Apply the log function to vector T in order to prevent divergence and
        return vector g.
        """
        exp_T = np.exp(T - np.max(T))
        return exp_T / np.sum(exp_T)


class ValueNetwork(NeuralNetwork):
    def __init__(self, data_size, classification_size, hidden_layer_size, dec_rate = 10):
        super().__init__(data_size, classification_size, hidden_layer_size, dec_rate)

    def train(self, r, memory, batch_size):
        for j in range(r):
            memory.shuffle()
            for i in range(0, len(memory), batch_size):

                self.batch_size =  min(batch_size, len(memory) - i)

                data, train, dec_rate = memory.sample_batch(i, min(len(memory), batch_size + i))
                self.initialize_data(np.array(data), np.array(train))
                self.dec_rate = 1 / dec_rate

                X = self.x_train
                Y = self.y_train
                Z, A = self.input_to_hidden(X)
                T = self.hidden_to_output(Z)


                dR_dT = T - Y

                dZ_dA = np.where(A > 0, 1.0, self.alpha)

                dR_dZ = dR_dT @ self.output_layer_weights[1:].T

                dR_dA = dR_dZ * dZ_dA
                dR_dHW = X[:, :, None] * dR_dA[:, None, :]

                dR_dOW = Z[:, :, None] * dR_dT[:, None, :]

                self.output_layer_weights[1:] -= (1/6) * (self.dec_rate) * np.mean(dR_dOW, axis=0)
                self.output_layer_weights[0] -= (1/6) *(self.dec_rate) * np.mean(dR_dT, axis=0)

                self.hidden_layer_weights[0] -= (1/6)* (self.dec_rate) * np.mean(dR_dA, axis=0)
                self.hidden_layer_weights[1:] -= (1/6)* (self.dec_rate) * np.mean(dR_dHW, axis=0)
    def regret_matching(self, I):
        Z, A = self.single_input_to_hidden(I)
        T = self.single_hidden_to_output(Z)
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
        Z, A = self.single_input_to_hidden(I)

        T = self.single_hidden_to_output(Z)

        g = self.single_softmax(T)
        return np.random.choice(len(g), p = g), g
