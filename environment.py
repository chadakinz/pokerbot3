import numpy as np
import phevaluator
from eval7 import equity, cards, handrange



### History data type ({'c': [cards]}, {1: {'R': amount}}, {2: {'C': amount}}}
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suits = ['s', 'd', 'c', 'h']
deck = []
for rank in ranks:
    for suit in suits:
        deck.append(rank + suit)
def initialize_tree(bb_max_range, ):
    return np.random.randint(0, bb_max_range, size = (2,))

def get_next_turn(history):
    n = len(history)
    #Preflop and cards need to be dealt
    if n < 4: return 'c'
    #Small blind ante
    if n == 4: return 2
    #Big blind ante
    elif n == 5: return 1
    #First action call or raise defers to opp
    elif n == 6: return 1

    elif n > 6:
        if history[-1].value() == 'C': return 'c'
        elif history[-1].value() == 'R':
            if history[-1].key() == 1:
                return 2
            else:
                return 1

        else: raise Exception("get next turn missing case")

def is_terminal(history):
    if history[-1].value() == 'F': return True
    count = 0
    for action in history:
        if action.key() == 'c': count += 1

    if count == 5 and history[-1].value() == 'C': return True
    else: return False

def utility(history, i):
    if i == 1:
        cards = history[2]
        opp_cards = history[3]
    else:
        cards = history[3]
        opp_cards = history[2]
    chips_staked = 0
    opp_chips_staked = 0

    community_cards = []
    for action in history:
        #TODO bugged with checking
        if action.value().key() == 'C' and action.key() == i:
            chips_staked += action.value().value()
        elif action.value().key() == 'C' and action.key() != i:
            opp_chips_staked += action.value().value()
        elif action.value().key() == 'R' and action.key() == i:
            chips_staked += action.value().value()
        elif action.value().key() == 'R' and action.key() != i:
            opp_chips_staked += action.value().value()

        if action.key() == 'c':
            community_cards += action.value()


    if history[-1].value() == 'F' and history[-1].key() == i:
        return -chips_staked
    elif history[-1].value() == 'F' and history[-1].key() != i:
        return opp_chips_staked

    round_winner = hand_winner(cards + community_cards, opp_cards + community_cards)
    if round_winner == 1:
        return opp_chips_staked
    elif round_winner == -1:
        return -chips_staked
    else:
        return 0


def hand_winner(curr_hand, opp_hand):
    #TODO, NEED TO PROCESS CARDS IN o s and DD format for it to work in evaluate function
    if evaluate(curr_hand) < evaluate(opp_hand):
        return 1
    elif evaluate(curr_hand) > evaluate(opp_hand):
        return -1
    else: return 0

def evaluate(cards):
    return phevaluator.evaluate_cards(cards[0], cards[1], cards[2], cards[3], cards[4], cards[5], cards[6])

def possible_actions(history, I):
    p1_chips = history[3]
    p2_chips = history[4]

    for action in history:
        if action.value() == 'C' or action.value() == 'R':
            if action.key() == 1:
                p1_chips -= action.value().value()
            else:
                p2_chips -= action.value().value()

    if I == history:
        count = 0
        cards = []
        for action in I:
            if action.key() == 'c':
                count += 1
                cards.append(action.value())

        if count == 0: return (2, deck)
        elif count == 1: return (2, remove_cards(deck, cards))
        elif count == 2: return (3, remove_cards(deck, cards))
        elif count == 3: return (1, remove_cards(deck, cards))
        elif count == 4: return (1, remove_cards(deck, cards))

    else:
        ### 0 - Fold, 1 - Call/Check, 2 - .25 * Pot, 3 - .5 * Pot, 4 - 1 * pot, 5 - all in
        return {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}



def get_infoset(history, curr_player):
    ### (stack size, opp stack size, equity, pot size, raise count, check raise?, betting round)
    betting_round = get_betting_round(history)
    pot_size = get_potsize(history)
    raise_count = 0
    for i in range(len(history) - 1, 0, -1):
        if history[i].value() == 'R':
            raise_count += 1
        if history[i].key() == 'c':
            break
    if curr_player == 'c':
        return history
    else:

        hand = get_hand(history, curr_player)
        equity = get_equity(hand)
        if curr_player == 1:
            return (history[0].value(), history[1].value(), equity, pot_size, raise_count, betting_round)
        else:
            return (history[1].value(), history[0].value(), equity, pot_size, raise_count, betting_round)






def remove_cards(deck, cards):
    return [x for x in deck if x not in cards]


def get_betting_round(history):
    #TODO Fix function
    count = 0
    for action in history[4:]:
        if action.key() == 'c':
            count += 1

    return count
#TODO
def get_hand(history, i):
    pass
#TODO
def get_potsize(history):
    pass
def get_equity(cards):
    return _equity(cards[:2], cards[2:], 10000)

def _equity(hero_cards, board, num_iter):

    hero_dist = handrange.HandRange(f"{hero_cards[0]}{hero_cards[1]}")

    villain_dist = handrange.HandRange("AA, KK, QQ, AKs, JJ, AQs, KQs, AJs, KJs, TT, AKo, ATs, QJs, KTs, QTs, JTs, 99, AQo, A9s, KQo, 88, K9s, T9s, A8s, Q9s, J9s, AJo, A5s, 77, A7s, KJo, A4s, A3s, A6s, QJo, 66, K8s, T8s, A2s, 98s, J8s, ATo, Q8s, "
                                       "K7s, KTo, 55, JTo, 87s, QTo, 44, 33, 22, K6s, 97s, K5s, 76s, T7s, K4s, K3s, K2s, Q7s, 86s, 65s, J7s, 54s, Q6s, 75s, 96s, Q5s, 64s, Q4s, Q3s, T9o, T6s, Q2s, A9o, 53s, 85s, J6s, J9o, K9o, J5s, Q9o, 43s, 74s, J4s, "
                                       "J3s, 95s, J2s, 63s, A8o, 52s, T5s, 84s, T4s, T3s, 42s, T2s, 98o, T8o, A5o, A7o, 73s, A4o, 32s, 94s, 93s, J8o, A3o, 62s, 92s, K8o, A6o, 87o, Q8o, 83s, A2o, 82s, 97o, 72s, 76o, K7o, 65o, T7o, K6o, 86o, 54o, K5o, J7o, "
                                       "75o, Q7o, K4o, K3o, 96o, K2o, 64o, Q6o, 53o, 85o, T6o, Q5o, 43o, Q4o, Q3o, 74o, Q2o, J6o, 63o")
    new_board = []
    for i in board:
        new_board.append(cards.Card(i))

    #print(f"Equity.py: {equity.py_all_hands_vs_range(hero_dist, villain_dist, board, num_iter)}")
    try:
        return equity.py_all_hands_vs_range(hero_dist, villain_dist, new_board, num_iter)[(hero_cards[0], hero_cards[1])]
    except:
        return equity.py_all_hands_vs_range(hero_dist, villain_dist, new_board, num_iter)[(hero_cards[1], hero_cards[0])]