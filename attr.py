from environment import *
import numpy as np
class Dict(dict):
    def __init__(self):
        super().__init__()

    def __setitem__(self, key, value):
        if key not in self:
            value2 = possible_actions(key)
            super().__setitem__(key, value2)
        super().__setitem__(key, value)

    def __getitem__(self, key):

        if key not in self:

            value = possible_actions(key)

            super().__setitem__(key, value)

        return super().__getitem__(key)



def chance_action(action):
    cards = []
    indexs = np.random.randint(0, len(action[1]), size=(action[0],))
    for i in indexs:
        cards.append(action[1][i])
    return cards

class Player:
    def __init__(self, id):
        self.id = id

        pass

class Buffer:
    def __init__(self, size):
        self.size = size
        self.cur_size = 0
        self.buffer = []

    def push(self, x):
        if self.cur_size < self.size:
            self.buffer.append(x)
            self.cur_size += 1
        else:
            k = np.random.randint(0, self.cur_size - 1, size = (1,))
            if k < self.size:
                self.buffer[k] = x

    def sample(self,k):
        sample = np.random.choice(self.buffer, size=k, replace=False)
        data = []
        value = []
        s = 0
        for i in sample:
            data.append(i[0])
            value.append(i[1]* i[2])
            s += i[1]
        return data, value, s