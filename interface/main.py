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
            [2.85944479e+03, 2.88250354e+03, 2.85944479e+03, 2.85944479e+03, 2.91743109e+03, -1.43754632e+04],
            [2.19703627e+00, 2.19166414e-01, -1.13110597e+00, -8.84883679e-01, 1.76594207e+00, 6.54268279e-01],
            [-4.63767178e+00, -4.38986616e+00, -3.92708192e+00, 6.14105823e+00, 8.36730715e-01, 8.13140233e+00],
            [1.89750078e+00, -5.30805206e-01, -1.35909198e+00, 5.27803582e-01, 1.45984800e+00, 6.42727600e-01],
            [2.52603763e+00, -7.02117343e-01, -3.73004869e+00, 2.47653862e+00, 3.07381880e+00, -9.11230496e-02],
            [5.03581775e+00, -2.90086365e+00, -8.07405723e+00, 4.65745957e+00, 5.26143925e+00, -1.87044335e+00],
            [9.52190151e+01, 9.34902906e+00, -1.51464271e+02, 9.37004974e+01, 9.53673400e+01, -1.38967858e+02],
            [9.88158048e-01, 5.02276625e-01, 1.12795361e+00, -2.06926904e+00, 9.36748829e-01, 9.55692867e-01],
            [9.93682701e+01, 1.05139386e+01, -1.58992982e+02, 9.70562952e+01, 1.00231564e+02, -1.45705405e+02]
        ])


        hidden_weights = np.array([
            [-1.74540707e+00, -1.10209590e+01, -8.17182620e-01, -4.69130336e-01, -1.51655753e+00, -9.46337909e+01,
             -1.07537217e+00, -1.25661568e+02],
            [-1.25652077e+01, -5.62306862e+01, -4.86460190e+00, -5.38149941e+00, -9.24362895e+00, -2.00413876e+03,
             -8.55544995e+00, -2.63787514e+03],
            [-3.41770012e+01, -1.54491977e+02, -1.39751556e+01, -1.43940589e+01, -2.81240832e+01, -2.29031564e+03,
             -2.27721550e+01, -3.01416653e+03],
            [-1.17667014e+00, -4.99935135e+00, 3.64999163e-01, 1.56339426e-01, -4.44932266e-01, -4.51730836e+01,
             -1.24617879e-01, -5.88606501e+01],
            [-4.40866416e+00, -2.21011059e+01, -1.34404558e+00, -1.70400570e+00, -3.02837693e+00, -1.90858692e+02,
             -2.60407707e+00, -2.51416514e+02],
            [-9.65503720e+00, -4.38008411e+01, -3.44557346e+00, -3.87705125e+00, -7.49406462e+00, -3.81704163e+02,
             -6.16648168e+00, -5.02561275e+02],
            [-1.80865386e+00, -7.55263715e+00, -3.42553273e-01, -3.84217193e-01, -1.00282121e+00, -3.58019315e+01,
             -7.25583484e-01, -4.67541283e+01],
            [8.11129770e-01, 6.78733889e-01, 6.88279897e-01, 4.51686542e-01, 8.71310997e-01, 3.74876627e-01,
             4.87290132e-01, 2.36357768e-01],
            [1.58190892e-01, 3.23585155e-01, 5.19018043e-01, 1.84276509e-01, 7.21311983e-01, 2.36685949e-01,
             8.04104142e-02, 2.23714241e-01],
            [5.55670958e-01, -7.30345644e+00, 8.08502896e-01, 1.86909880e-01, 5.58116261e-01, -2.00875021e+01,
             9.28914424e-01, -2.62457492e+01],
            [1.14130893e-02, -2.13836855e+01, 1.16301712e-01, 7.08664247e-01, 4.24931991e-01, -2.86089162e+02,
             5.85112966e-01, -3.76401268e+02],
            [4.76572751e-01, -4.33127434e+01, 7.71752755e-01, 1.24923019e-01, 3.65891072e-01, -2.86203866e+03,
             8.44567761e-01, -3.76710326e+03],
            [6.90163973e-01, 2.61731350e-01, 4.87527951e-01, 8.68633054e-01, 8.67110808e-01, 9.55334702e-01,
             9.17634013e-01, 5.19642755e-01],
            [9.99582192e-01, 5.95079916e-01, 5.33292050e-01, 7.85251448e-01, 8.03827815e-01, 8.92097486e-01,
             1.10305208e-01, 5.21801941e-01],
            [5.10001406e-01, 8.83804368e-01, 7.11484438e-01, 8.11810059e-01, 9.52298784e-01, 5.50277801e-01,
             8.20095457e-01, 1.52262177e-01],
            [-1.67162159e+00, -2.17196964e+01, -2.39640961e-01, -3.26139758e-01, -1.17778912e+00, -1.90277853e+02,
             -1.11719476e+00, -2.50998129e+02]
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
        self.draw_button(str(bot_chips), 10, SCREEN_HEIGHT - 600)

    def draw_potsize(self):
        player_chips = get_potsize(self.history)
        self.draw_button(str(player_chips), SCREEN_WIDTH - 600, SCREEN_HEIGHT - 305)

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