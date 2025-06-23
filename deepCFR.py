from pokerbot3.environment.python_dependencies.environment import *
from networks import *
import numpy as np
from tqdm import tqdm

def traverse(history, i, curr_player, t, val_mem, pol_mem, val1_net, val2_net, pol_net):
    #print(history)
    if is_terminal(history):
        return utility(history, i)
    if curr_player != 'c':
        infoset = normalize_infoset(get_infoset(history, curr_player))
    else:
        infoset = get_infoset(history, curr_player)
    if curr_player == i:
        regret = []
        cum_regret = 0
        for j in range(6):
            new_action = process_action(j, history, i)
            new_history = history + new_action
            r = traverse(new_history, i, get_next_turn(new_history), t, val_mem, pol_mem, val1_net, val2_net, pol_net)
            cum_regret += val1_net.regret_matching(infoset)[j] * r
            regret.append(r)
        val_mem.push((infoset, t, np.array(regret) - np.full(len(regret), cum_regret)))
        return cum_regret
    else:
        if curr_player == 'c':
            a = chance_action(possible_actions(history, curr_player))
            new_history = history + (('c',  a, None),)
            next_player = get_next_turn(new_history)
            return traverse(new_history, i, next_player, t, val_mem, pol_mem, val1_net, val2_net, pol_net)
        else:
            p = val2_net.regret_matching(infoset)
            na = np.random.choice(len(p), p = p)
            next_action = process_action(na, history, curr_player)
            next_history = history + next_action
            pol_mem.push((infoset, t, p))
            return traverse(next_history, i, get_next_turn(next_history), t, val_mem, pol_mem, val1_net, val2_net, pol_net)





if __name__ == '__main__':
    T = 10
    players = [1, 2]
    K = 20
    value_networks = {1: ValueNetwork(15, 6, 8), 2: ValueNetwork(15, 6, 8)}
    pol_networks = PolicyNetwork(15, 6, 8)
    value_memories = {1: Buffer(200000), 2: Buffer(200000)}
    strategy_memory = Buffer(200000)
    print(pol_networks.output_layer_weights)
    print(pol_networks.hidden_layer_weights)
    print("\n\n")
    for t in tqdm(range(1, T)):
        history = initialize_tree(25)
        for i in players:
            for k in tqdm(range(1, K)):
                p = get_next_turn(history)
                traverse(history, i, p, t, value_memories[i], strategy_memory, value_networks[i], value_networks[3-i], pol_networks)
            value_networks[i] = ValueNetwork(15, 6, 8)
            value_networks[i].train(50, value_memories[i], 200)
        pol_networks.train(50, strategy_memory, 200)
    print(pol_networks.output_layer_weights)
    print("hidden layer")
    print(pol_networks.hidden_layer_weights)

