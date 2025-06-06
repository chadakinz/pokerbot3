import numpy as np
import phevaluator
from eval7 import equity, cards, handrange

#ZACHAREY IS A LOOSER

### History data type ({'c': [cards]}, {1: {'R': amount}}, {2: {'C': amount}}}
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suits = ['s', 'd', 'c', 'h']
deck = []
for rank in ranks:
    for suit in suits:
        deck.append(rank + suit)
def initialize_tree(bb_max_range, ):
    return np.random.randint(0, bb_max_range, size = (2,))

#TODO Logic needs fixed
def get_next_turn(history):
    n = len(history)
    #Preflop and cards need to be dealt
    if n < 5: return 'c'
    #Small blind ante
    if n == 5: return 2
    #Big blind ante
    elif n == 6: return 1
    #First action call or raise defers to opp
    elif n == 7: return 1

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


#TODO ZACHY
def get_infoset(history, curr_player):
    """

    :param history: Example of tuple:
    (Player1_Chips, Player2_Chips, {'c': [As, Ks]}, {'c': [Jc, Kc]}, {2: {'R': (Small blind) :: Int}},
    {1: {'C': (Small blind) :: Int}}, {1: {'R': (Small blind) :: Int}}, {2: {'C': (Small blind) :: Int}}, {'c': [2h, 3h, 6c]})
    :param curr_player: goign to be 1, 2 or 'c', if c just return history.
    :return: return a vector (represented as a list)
    [Current player chips, Opposing player chips, prelop equity, preflop raise count, preflop potsize, flop equity, flop raise count, flop potsize,
    turn equity, turn raise count, turn potsize, river equity, river raise count, river potsize]
    Using the example aboce, the infoset vector for player 1 would be:
    [Player1_Chips, Player2_Chips, .7, 4, 2, .7, 0, 0, 0 ,0 ,0 ,0 ,0 ,0]
    Use get_equity to get the equity it is implemented for you already
    """
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


#TODO ZACHY
def get_betting_round(history):
    """
    Take the history and return the betting round. 0 for preflop, 1 for flop, 2 for turn and 3 for river.
    :param history: tuple of actions:
    Example of tuple:
    (Player1_Chips, Player2_Chips, {'c': [As, Ks]}, {'c': [Jc, Kc]}, {2: {'R': (Small blind) :: Int}},
    {1: {'C': (Small blind) :: Int}}, {1: {'R': (Small blind) :: Int}}, {2: {'C': (Small blind) :: Int}}, {'c': [2h, 3h, 6c]})
    :return:
    """

    count = 0
    for action in history[4:]:
        if action.key() == 'c':
            count += 1

    return count

#TODO ZACHY
def get_hand(history, i):
    """
    :param history: tuple of actions:
    Example of tuple:
    (Player1_Chips, Player2_Chips, {'c': [As, Ks]}, {'c': [Jc, Kc]}, {2: {'R': (Small blind) :: Int}},
    {1: {'C': (Small blind) :: Int}}, {1: {'R': (Small blind) :: Int}}, {2: {'C': (Small blind) :: Int}}, {'c': [2h, 3h, 6c]})
    :param i: Which player, either 1 or 2. if 1 get hand returns [As, Ks, 2h, 3h, 6c], else [Jc, Kc, 2h, 3h, 6c]
    :return:
    """
    pass
#TODO ZACHY
def get_potsize(history):
    """
    :param history: tuple of actions:
    Example of tuple:
    (Player1_Chips, Player2_Chips, {'c': [As, Ks]}, {'c': [Jc, Kc]}, {2: {'R': (Small blind) :: Int}},
    {1: {'C': (Small blind) :: Int}}, {1: {'R': (Small blind) :: Int}}, {2: {'C': (Small blind) :: Int}}, {'c': [2h, 3h, 6c]})
    :return: Potsize from actions 'C' and 'R'. THe raise is added on top of the call. So, the potsize is 4x small blind in this current hand
    """

    return 3
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

#Todo Process action integer 0 - 5 to fold - allin. Make sure edge cases are taken into consideration
def process_action(num, history, i):
    call_amount = get_call_amount(history)
    match num:
        case 0: return 'F'
        case 1:

            if is_all_in(call_amount, i):
                return all_in_action(history, call_amount)
            return {'C': call_amount}
        case 2:
            potsize = get_potsize(history)
            raise_amount = round(.25 * potsize)


            return {'R': raise_amount}

            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass


def get_call_amount(history):
    pass

def is_all_in(call_amonunt):
    return False

def all_in_action(history):
    pass