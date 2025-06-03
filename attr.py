from environment import *
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
