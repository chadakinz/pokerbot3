import numpy as np
import phevaluator
from eval7 import equity, cards, handrange
from attr import *


### History data type ({'c': [cards]}, {1: {'R': amount}}, {2: {'C': amount}}}
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suits = ['s', 'd', 'c', 'h']
deck = []
for rank in ranks:
    for suit in suits:
        deck.append(rank + suit)
def initialize_tree(bb_max_range, ):
    starting_stacks = np.random.randint(3, bb_max_range, size = (2,))
    cards = chance_action((4,deck))
    return ((1, starting_stacks[0], None), (2, starting_stacks[1], None) , ('c', cards[0:2], 1), ('c', cards[2:], 2),
            (2, "R", 1), (1, "C", 1), (1, "R", 1))



def get_next_turn(history):
    n = len(history)

    if n == 7: return 2

    elif n > 7:
        count = 0
        for item in reversed(history):
            if item[0] == 'c':
                break
            if item[1] == "R" or item[1] == "C":
                count += 1

        if history[-1][1] == "C":
            if count > 1:
                return 'c'
            else:
                if history[-1][0] == 1: return 2
                else: return 1
        elif history[-1][1] == "A" or history[-2][1] == "A" or history[-3][1] == "A":
            return 'c'
        elif  history[-1][1] == "R":
            if history[-1][0] == 1: return 2
            else: return 1

        elif history[-1][0] == "c":
            return 1


        else: return -1


def is_terminal(history):
    if history[-1][1] == "F":
        return True

    if get_betting_round(history) != 3:
        return False

    for item in history:
        if item[1] == "A":
            return True

    check = False
    for item in reversed(history):
        if item[0] == 'c':
            return False
        if item[1] == "C" and not check:
            check = True
        elif check and (item[1] == "R" or item[1] == "C"):
            return True
    return False

#TODO NEEDS to be tested
def utility(history, i):
    if i == 1:
        opp = 2
        chips = history[0][1]
        opp_chips = history[1][1]
    else:
        opp = 1
        chips = history[1][1]
        opp_chips = history[0][1]
    chips_staked = chips - get_chips(history, i)

    opp_chips_staked = opp_chips - get_chips(history, opp)

    if history[-1][1] == 'F' and history[-1][0] == i:
        return -chips_staked
    elif history[-1][1] == 'F' and history[-1][0] != i:
        return opp_chips_staked

    round_winner = hand_winner(get_hand(history, i), get_hand(history, opp))
    if round_winner == 1:
        return opp_chips_staked
    elif round_winner == -1:
        return -chips_staked
    else:
        return 0

def hand_winner(curr_hand, opp_hand):
    """Curr hand and opp hand in form [As, Aj, 8h, 7h, 5h], [Ks, Kj, 8h, 7h, 5h]"""
    curr_score = evaluate(curr_hand)
    opp_score = evaluate(opp_hand)

    if curr_score > opp_score:
        return -1
    elif curr_score < opp_score:
        return 1
    else:
        return 0

def evaluate(cards):
    return phevaluator.evaluate_cards(cards[0], cards[1], cards[2], cards[3], cards[4], cards[5], cards[6])

def possible_actions(history, i):
    if i == 'c':
        count = 0
        cards = []
        for item in history:
            if item[0] == 'c':
                count += 1
                cards += item[1]

        if count == 0: return (2, deck)
        elif count == 1: return (2, remove_cards(deck, cards))
        elif count == 2: return (3, remove_cards(deck, cards))
        elif count == 3: return (1, remove_cards(deck, cards))
        elif count == 4: return (1, remove_cards(deck, cards))

    else:
        ### 0 - Fold, 1 - Call/Check, 2 - .25 * Pot, 3 - .5 * Pot, 4 - 1 * pot, 5 - all in
        return {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}


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

    if curr_player == 'c':
        return history

    infoset = [0] * 15

    # Chip stacks
    p1_chips, p2_chips = history[0][1], history[1][1]
    infoset[0] = p1_chips if curr_player == 1 else p2_chips
    infoset[1] = p2_chips if curr_player == 1 else p1_chips
    if curr_player == 1:
        cards = history[2][1]
    else:
        cards = history[3][1]
    raise_count = 0
    # Track board and current street
    board = []
    potsize = 0
    count = 0
    for j in range(4, len(history)):
        if history[j][0] == 'c':
            infoset[2 + 3 * count] = get_equity(cards + board)
            infoset[2 + 3 * count + 1] = raise_count
            infoset[2 + 3 * count + 2] = potsize
            raise_count = 0
            potsize = 0
            board += history[j][1]
            count += 1

        if history[j][1]  == "R":
            raise_count += 1
            potsize += history[j][2]
        elif history[j][1] == "C":
            potsize += history[j][2]

    infoset[2 + 3 * count] = get_equity(cards + board)
    infoset[2 + 3 * count + 1] = raise_count
    infoset[2 + 3 * count + 2] = potsize
    infoset[-1] = count
    return infoset



def remove_cards(deck, cards):
    return [x for x in deck if x not in cards]



def get_betting_round(history):
    """
    Return the betting round from the history.
    0 = preflop, 1 = flop, 2 = turn, 3 = river
    """
    round_num = 0
    for item in history[4:]:
        if item[0] == 'c':
            round_num += 1
    return round_num


def get_hand(history, i):
    """
    :param history: tuple representing game history
    :param i: player index (1 or 2)
    :return: list of cards (hole cards + board cards)
    """

    # Get player hole cards
    if i == 1:
        hole_cards = history[2][1]
    elif i == 2:
        hole_cards = history[3][1]
    else:
        raise ValueError("Player index must be 1 or 2")

    # Collect board cards from all dicts with key 'c' after player cards
    board_cards = []
    for item in history[4:]:
        if item[0] == 'c':
            board_cards += item[1]  # always take latest board snapshot

    # Combine hole cards and board cards
    full_hand = hole_cards + board_cards

    return full_hand


def get_potsize(history):

    potsize = 0
    for item in history:
        if item[1] == "C" or item[1] == "R":
            potsize += item[2]
    return potsize

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

    try:
        return equity.py_all_hands_vs_range(hero_dist, villain_dist, new_board, num_iter)[(cards.Card(hero_cards[0]), cards.Card(hero_cards[1]))]
    except:
        return equity.py_all_hands_vs_range(hero_dist, villain_dist, new_board, num_iter)[(cards.Card(hero_cards[1]), cards.Card(hero_cards[0]))]


def process_action(num, history, i):
    call_amount = get_call_amount(history)
    potsize = get_potsize(history)
    match num:
        case 0: return ((i, 'F', None),)
        case 1:
            if get_chips(history + ((i, 'C', call_amount),), 1) <= 0 or get_chips(history + ((i, 'C', call_amount),), 2) <= 0:
                return ((i, 'A', call_amount),)
            else: return ((i, 'C', call_amount),)
        case 2:
            raise_amount = round(.25 * potsize)
            if call_amount >= get_chips(history, i):
                return ((i, 'A', call_amount),)
            elif raise_amount < call_amount:
                return (i, "C", call_amount) , (i, 'R',  min(call_amount, get_chips(history, 1), get_chips(history,2)))
            else:
                return (i, "C", call_amount), (i, 'R',  min(raise_amount, get_chips(history, 1), get_chips(history,2)))

        case 3:
            raise_amount = round(.5 * potsize)
            if call_amount >= get_chips(history, i):
                return ((i, 'A', call_amount),)
            if raise_amount < call_amount:
                return (i, "C", call_amount), (i, 'R',  min(call_amount, get_chips(history, 1), get_chips(history, 2)))
            else:

                return (i, "C", call_amount), (i, 'R', min(raise_amount, get_chips(history, 1), get_chips(history, 2)))


        case 4:
            raise_amount = potsize
            if call_amount >= get_chips(history, i):
                return ((i, 'A', call_amount),)
            if raise_amount < call_amount:
                return (i, "C", call_amount), (i, 'R',  min(call_amount, get_chips(history, 1), get_chips(history, 2)))
            else:

                return (i, "C", call_amount), (i, 'R',  min(raise_amount, get_chips(history, 1), get_chips(history, 2)))

        case 5:
            raise_amount = get_chips(history, i)
            if call_amount >= get_chips(history, i):
                return ((i, 'A', call_amount),)
            if raise_amount < call_amount:
                return (i, "C", call_amount), (i, 'R', min(call_amount, get_chips(history, 1), get_chips(history, 2)))
            else:

                return (i, "C", call_amount) , (i, 'R',  min(raise_amount, get_chips(history, 1), get_chips(history, 2)))


def get_call_amount(history):
    """
    Returns the most recent raise amount from the action history,
    which represents the amount to call. Returns 0 if there was no raise.

    Assumes history is a tuple of actions, where each action is a dict like:
    {player_id: {'R': amount}} or {player_id: {'C': amount}}, etc.
    """
    for item in reversed(history):
        if item[0] == 'c': return 0
        elif item[1] == "C": return 0
        elif item[1] == "F": return 0
        elif item[1] == "R": return item[2]
    return 0


def get_chips(history, i):
    """
    Returns the remaining chips for player i after all call and raise actions.
    :param history: tuple of game state
    :param i: player index (1 or 2)
    :return: int - chips remaining
    """
    chips = history[0][1] if i == 1 else history[1][1]
    for item in history[4:]:
        if (item[1] == "C" or item[1] == "R" or item[1] == "A") and item[0] == i: chips -= item[2]
    return chips




if __name__ == '__main__':
    history = (
        (1, 80, None), (2, 80, None),
        ('c', ['Jh', 'Jc'], None),
        ('c', ['Qs', 'Qc'], None),
        (2, 'R',  1),
        (1, 'C', 1),
        (1, 'R', 1),
        (2, 'C', 1),
        ('c', ['Ad', 'Kh', 'Ks'], None),
        (2, 'R', 4),
        (1, 'C', 4), ('c', ['As'], None),
            (1, 'R', 6),
            (2, 'C', 6),
            ('c', ['Qh'], None), (1, 'C', 0), (2, 'C', 0))

    print(get_infoset(history, 1))
    print(is_terminal(history))