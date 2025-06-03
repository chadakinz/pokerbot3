from environment import *
from attr import *

def traverse(history, i, curr_player):
    if is_terminal(history): return utility(history, i)
    infoset = get_infoset(history, curr_player)
    if curr_player == i:
        pass
    else:
        if curr_player == 'c':
            a = chance_action(possible_actions(history, curr_player))
            new_history = history + ({'c': a})
            next_player = get_next_turn(new_history)
            return traverse(new_history, i, next_player)
        else:
            pass




if __name__ == '__main__':
    T = 1000
    players = [1, 2, 'c']
    K = 10
    for t in range(T):
        starting_stacks = initialize_tree(150)
        history = ({1:starting_stacks[0]}, {2:starting_stacks[1]},)
        for i in players:
            for k in range(1, K):
                p = get_next_turn(history)
                traverse(history, i, p)
            #Train player p's model based on samples received through K iterations