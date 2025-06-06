from environment import *
from attr import *
from networks import *
import numpy as np
def traverse(history, i, curr_player, t, val_mem, pol_mem, val1_net, pol_net):
    if is_terminal(history): return utility(history, i)
    infoset = get_infoset(history, curr_player)
    if curr_player == i:
        regret = []
        weighted_value = []
        for j in range(6):
            new_action = process_action(j, history, i)
            new_history = history + ({curr_player: new_action},)
            r = traverse(new_history, i, get_next_turn(history), t, val_mem, pol_mem, val1_net, pol_net)
            p_r = val1_net.regret_matching(infoset)[j] * r
            regret.append(r - p_r)
            weighted_value.append(p_r)
        val_mem.push((infoset, t, np.array(regret)))
        return sum(weighted_value)
    else:
        if curr_player == 'c':
            a = chance_action(possible_actions(history, curr_player))
            new_history = history + ({'c': a})
            next_player = get_next_turn(new_history)
            return traverse(new_history, i, next_player, t, val_mem, pol_mem, val1_net, pol_net)
        else:
            na, p = pol_net.sample_action(infoset)
            next_action = process_action(na, history, curr_player)
            next_history = history + ({curr_player: next_action},)
            pol_mem.push((infoset, t, p))
            return traverse(next_history, i, get_next_turn(history), t, val_mem, pol_mem, val1_net, pol_net)





if __name__ == '__main__':
    T = 1000
    players = [1, 2]
    K = 100
    value_networks = {1: ValueNetwork(15, 6, 8), 2: ValueNetwork(15, 6, 8)}
    pol_networks = PolicyNetwork(15, 6, 8)
    value_memories = {1: Buffer(10000000000), 2: Buffer(10000000000)}
    strategy_memory = Buffer(10000000000)
    for t in range(T):
        history = initialize_tree(150)
        for i in players:
            for k in range(1, K):
                p = get_next_turn(history)
                traverse(history, i, p, t, value_memories[i], strategy_memory, value_networks[i], pol_networks)
            value_networks[i] = NeuralNetwork(15, 6, 8)
            data, train, dec_rate = value_memories[i].sample(1000)
            value_networks[i].initialize_data(data, train)
            value_networks[i].dec_rate = dec_rate
            value_networks[i].train(1)

        data, train, dec_rate = strategy_memory.sample(1000)
        pol_networks.initialize_data(data, train)
        pol_networks.dec_rate = dec_rate
        pol_networks.train(1)

