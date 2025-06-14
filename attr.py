
import numpy as np
import random

def normalize_infoset(infoset):
    max_values = np.array([15, 15, 1, 25, 50, 1, 25, 50, 1, 25, 50, 1, 25, 50, 4])
    return infoset/max_values
def chance_action(action):
    return random.sample(action[1], action[0])

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
        #print(f"buffer = {self.buffer}")
        #print(len(self.buffer))
        sample = random.sample(self.buffer, min(len(self.buffer), k))
        data = []
        value = []
        s = 0

        for i in sample:
            data.append(i[0])
            value.append(i[1]* i[2])
            s += i[1]

        return data, value, s

    def sample_batch(self, start, end):
        sample = self.buffer[start:end]
        data = []
        value = []
        s = 0

        for i in sample:
            data.append(i[0])
            value.append(i[1] * i[2])
            s += i[1]

        return data, value, s

    def shuffle(self):
        np.random.shuffle(self.buffer)

    def __len__(self):
        return len(self.buffer)