from networks import *
class PolicyNetworkTest(PolicyNetwork):
    def __init__(self, data_size, classification_size, hidden_layer_size, hidden_layer, output_layer):
        super().__init__(data_size, classification_size, hidden_layer_size)
        self.hidden_layer = hidden_layer
        self.output_layer = output_layer