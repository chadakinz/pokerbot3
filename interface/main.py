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
            [-0.08208868, 0.06813695, 0.04767652, -0.37261689, 0.70670259, 0.06206976],
            [-0.12161612, -0.32516425, -0.1300983, -0.50873458, 0.27908614, 0.09882234],
            [-0.0291064, 0.21051911, -0.50979158, 0.47097816, 0.08033155, 0.32998639],
            [0.15960616, 0.13907959, 0.07617853, 0.80895414, 0.13810942, 0.00645817],
            [0.47632718, -0.21318209, 0.52019657, -0.49217116, -0.36816874, 0.24469713],
            [0.00848592, -0.14624898, -0.12119177, -0.14649245, -0.29674514, 0.1576072],
            [0.0326592, -0.24183516, -0.4057944, 0.26711294, -0.04332596, -0.19993077],
            [-0.12645823, -0.30625524, -0.37531507, 0.15945651, -0.08340334, 0.44236958],
            [-0.40501301, -0.02574194, -0.05735686, 0.08611161, 0.05055559, 0.28011262]
        ])

        hidden_weights = np.array([
            [0.00164637, 0.20340699, 0.18197939, 0.08375441, 0.44619923, -0.12971397, -0.51962741, -0.25287258],
            [-0.01825157, 0.293148, 0.0644315, -0.06598593, 0.21418683, -0.35426061, -0.15821124, 0.54518082],
            [-0.38538362, -0.73308468, 0.66389235, -0.24206958, -0.49627515, -0.28840634, -0.31177302, 0.23311731],
            [0.02985965, 0.04020033, -0.35871702, -0.33785985, -0.24440258, -0.02926719, -0.54993502, 0.24034922],
            [0.10032093, -0.18345163, 0.28951232, -0.31417345, -0.00347867, 0.4789508, -0.41916799, -0.13935396],
            [0.255503, -0.02547083, 0.12113712, -0.01347123, -0.48023848, 0.20573427, -0.11890865, -0.40684663],
            [0.15931177, -0.14637024, -0.16235369, 0.14173948, -0.23430806, -0.59510108, -0.76449733, -0.09068397],
            [0.06942843, -0.00885283, -0.39762087, -0.13086693, 0.36188981, 0.21292697, -0.12970714, -0.1262954],
            [0.28057309, 0.07845018, 0.03601126, 0.03567202, 0.14722916, -0.14892861, 0.10782846, -0.03871063],
            [-0.16844055, 0.30862366, 0.15566245, 0.60834527, 0.31533137, 0.12149128, 0.5326147, -0.2941847],
            [0.17270114, 0.18062142, 0.09874918, -0.09794471, -0.3811765, 0.28128187, 0.08994309, 0.04694051],
            [0.20469147, 0.50478434, 0.45616463, 0.0211471, -0.52027603, -0.32724942, -0.28096992, 0.07240342],
            [-0.11030879, 0.13666842, 0.16836813, 0.37848346, -0.01043308, -0.27442164, 0.19199378, -0.15463022],
            [-0.04318477, -0.06120864, 0.44507297, 0.14433551, 0.22240269, 0.67133079, 0.23382934, 0.34896184],
            [-0.08573935, 0.16852717, 0.00920919, -0.55304169, 0.4769186, -0.0422858, 0.73441572, 0.36701235],
            [-0.29831029, -0.03153446, 0.15187958, -0.05316631, 0.03099371, 0.20333034, -0.07543239, -0.41960606]
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