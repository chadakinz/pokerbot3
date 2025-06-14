import unittest
from environment import *
from histories import *

class EnvironmentTest(unittest.TestCase):
    def test_get_next_turn(self):
        for history, label in get_next_turn_histories:
            self.assertEqual(get_next_turn(history), label, f"History: {history}, "
                                                            f"Received: {get_next_turn(history)}, Expected: {label}")

    def test_is_terminal(self):
        for history, label in is_terminal_histories:
            self.assertEqual(is_terminal(history), label, f"History: {history}, "
                                                          f"Received: {is_terminal(history)}, Expected: {label}")

    def test_utility(self):
        for history, i, label in utility_histories:
            self.assertEqual(utility(history, i), label, f"History: {history}, Player: {i}, Received: "
                                                         f"{utility(history, i)}, Expected: {label}")
    def test_hand_winner(self):
        pass
    def test_get_potsize(self):
        for history, label in get_potsize_histories:
            self.assertEqual(get_potsize(history), label, f"History: {history}, Received: {get_potsize(history)}, "
                                                          f"Expected: {label}")
    def test_get_infoset(self):
        pass
    def test_process_action(self):
        pass

if __name__ == '__main__':
    unittest.main()