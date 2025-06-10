from environment import *
from attr import *
import pygame
from model import *
import numpy as np


pygame.init()
deck = []
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suits = ['s', 'd', 'c', 'h']
for rank in ranks:
    for suit in suits:
        deck.append(rank + suit)
# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
CARD_WIDTH = 71
CARD_HEIGHT = 96

# Colors
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)



class PokerGame:
    def __init__(self, starting_stacks, player_id):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Poker vs AI")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.player_id = player_id
        # Game state
        self.community_cards = []
        self.pot = 0
        self.game_phase = "pre_flop"  # pre_flop, flop, turn, river, showdown
        cards = chance_action((4,deck))
        self.history = ((1, starting_stacks, None), (2, starting_stacks, None) , ('c', cards[0:2], 1), ('c', cards[2:], 2),
            (2, "R", 1), (1, "C", 1), (1, "R", 1))
        self.current_act = get_next_turn(self.history)
        output_weights = np.array([
            [2.40307101e+01, 2.44384705e+01, 1.21996107e+01, 2.40422860e+01, -1.04619177e+02, 2.30535626e+01],
            [1.97885798e+00, 9.92556413e-01, -6.78441070e-01, -3.82371384e-01, 1.57204748e+00, -1.12055720e+00],
            [1.63235723e+00, 8.72507355e-01, -2.17615982e-01, -7.85643590e-01, 2.08547793e+00, -9.59205605e-01],
            [3.16012491e-02, 7.55918948e-01, 5.98498961e-01, 9.92608662e-01, 5.94183396e-01, -1.49803544e-02],
            [1.19874484e+00, 1.19643261e+00, -4.59870645e-01, 1.83099970e-01, 1.03631111e+00, -7.63215525e-01],
            [7.78967131e-01, 9.76761814e-01, 5.62918862e-01, 5.99859085e-01, 7.51410832e-01, 3.05230698e-01],
            [1.37763150e+00, 8.93491987e-01, 3.50423896e-01, 1.00058673e-01, 1.22699616e+00, 1.41758504e-01],
            [1.82911749e+00, 1.59720828e+00, 1.20007655e+00, -4.32994224e+00, 8.61634630e-01, 2.54590639e+00],
            [1.94887594e+00, 1.47070594e+00, -1.17887922e+00, -6.90538790e-01, 1.88684764e+00, -1.58264571e+00],
        ])

        hidden_weights = np.array([
            [6.79735114e-01, 9.68931016e-02, -1.72214697e-01, 4.43218304e-01, 5.79790138e-01, 2.08871497e-01,
             2.75144059e-01, 4.55097382e-01],
            [-4.24906280e+00, -4.30458172e+00, -2.31867390e+00, -3.28158141e+00, -3.93919867e+00, -4.46578307e+00,
             -4.33126156e+00, -5.84774120e+00],
            [-3.77149348e+00, -4.37283828e+00, -2.47653830e+00, -3.11655963e+00, -4.61346581e+00, -3.82074861e+00,
             -4.46501543e+00, -5.77609618e+00],
            [8.86712898e-02, 7.54092427e-01, 7.82079263e-01, 7.19643534e-01, 6.60197682e-01, 1.30591828e-01,
             2.21394834e-02, 9.22202373e-02],
            [-1.16245809e+00, -4.44356236e-01, -6.14785651e-01, -7.98614038e-01, -3.68579906e-01, -6.30503705e-01,
             6.86808283e-01, -1.29018582e+00],
            [-3.62586256e+00, -4.01256284e+00, -2.25742363e+00, -2.71723242e+00, -4.28024106e+00, -3.74933837e+00,
             -5.16879371e-01, -5.27468562e+00],
            [4.64054655e-01, 3.40424512e-01, 1.38877976e-01, 4.47444452e-01, 7.53088064e-01, 1.19648357e-01,
             3.17545944e-01, 1.84734165e-01],
            [8.97866097e-02, 1.44693561e-01, 8.24291920e-01, 6.65899447e-01, 5.34857620e-01, 7.72861983e-01,
             -3.34758178e-01, 3.67237850e-01],
            [5.93613122e-01, 4.10477751e-01, 5.57871376e-01, -2.37419024e-02, 6.21412976e-01, 5.34919925e-01,
             -8.08512874e+00, 2.69391078e-01],
            [2.99174649e-01, 3.48869591e-02, 6.93661495e-01, 4.00470672e-01, 9.09524838e-01, 7.36401174e-01,
             1.13379172e-01, 3.20011729e-01],
            [3.40260965e-01, 2.11903731e-01, 1.65056267e-01, -1.35989167e-03, 2.03091205e-01, 8.55403173e-01,
             8.75647675e-01, 6.46204020e-01],
            [7.48447126e-01, 3.06225861e-01, 5.23127433e-01, 4.81360644e-01, 4.97675059e-01, 2.00735493e-01,
             3.30474346e-01, 7.78842176e-01],
            [7.66642190e-01, 8.52599268e-01, 8.10624191e-02, 3.73303792e-01, 2.01661401e-01, 9.46789813e-03,
             4.23186533e-01, 4.76204341e-01],
            [6.69571228e-01, 2.09238283e-01, 1.09029617e-01, 4.27487700e-01, 1.02800667e-01, 7.09840764e-01,
             6.63512227e-01, 5.64493288e-02],
            [6.99887099e-01, 7.12466819e-02, 1.21942022e-01, 5.79687223e-01, 1.77131951e-01, 3.97499421e-02,
             9.39688779e-01, 5.63948907e-01],
            [-2.68125893e-01, -3.72378702e-01, 7.09190779e-01, 1.40525475e-01, -2.77047738e-01, -1.88485673e-01,
             2.84042293e-01, 1.99338208e-01],
        ])


        self.model = PolicyNetworkTest(15, 6, 8, hidden_weights, output_weights)
    def draw_cards(self):
        cards = get_hand(self.history, self.player_id)
        i = 0
        for card in cards[:2]:
            i += 1
            imgCard = f'/Users/chadgothelf/pokah/pokerbot3/interface/playing_cards/{card}.png'
            card = pygame.image.load(imgCard)
            card = pygame.transform.scale(card, (100, 150))
            pygame.Surface.blit(self.screen, card, (50 + i * 80, SCREEN_HEIGHT - 150))


    def draw_chip_amount(self):
        player_chips = get_chips(self.history, self.player_id)
        bot_chips = get_chips(self.history, 3 - self.player_id)
        self.draw_button(str(player_chips), 10, SCREEN_HEIGHT - 200)
        self.draw_button(str(bot_chips), 10, SCREEN_HEIGHT - 50)

    def draw_potsize(self):
        player_chips = get_potsize(self.history)
        self.draw_button(str(player_chips), SCREEN_WIDTH - 100, SCREEN_HEIGHT - 75)

    def draw_game(self):
        self.screen.fill(GREEN)
        self.draw_cards()
        self.draw_chip_amount()
        self.draw_potsize()
        self.draw_button("CALL", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100)
        self.draw_button("RAISE", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150)
        self.draw_button("FOLD", SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)

    def draw_button(self, text, x, y):
        button_rect = pygame.Rect(x, y, 120, 40)
        pygame.draw.rect(self.screen, WHITE, button_rect)
        pygame.draw.rect(self.screen, BLACK, button_rect, 2)
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        return button_rect


    def run(self):
        running = True
        while running:
            if is_terminal(self.history):
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Handle button clicks here
                    print(f"Clicked at: {mouse_pos}")
                if self.current_act == self.player_id:
                    self.draw_game()
                    pass
                else:
                    infoset = np.array(get_infoset(self.history, 3 - self.player_id))
                    action, _ = self.model.sample_action(infoset)
                    print(infoset, action, _, self.history)
                    self.history += process_action(action, self.history, self.current_act)
                    self.current_act = get_next_turn(self.history)


            self.draw_game()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()



# Run the game
if __name__ == "__main__":
    starting_stacks = int(input("Please enter starting stacks in BB: "))
    player_id = int(input("Type 1 for player 1 or 2 for player 2: "))
    game = PokerGame(starting_stacks, player_id)
    game.run()