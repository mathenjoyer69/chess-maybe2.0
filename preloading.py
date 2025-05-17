import config
from buttons import *
from functions import draw_board

class PreScreen:
    def __init__(self):
        self.running = True
        self.autoplay = False
        self.bot_vs_bot = False
        self.analysis = False
        self.autoplay_online = False
        self.autoplay_button = Button(800, 0, 200, 50, 'auto play', self.autoplay, 'red', 'green', False, True)
        self.bot_vs_bot_button = Button(800, 50, 200, 50, 'bot vs bot', self.bot_vs_bot, 'red', 'green', False, True)
        self.analysis_button = Button(800, 100, 200, 50, 'analysis', self.analysis, 'red', 'green', False, True)
        self.autoplay_online_button = Button(800, 150, 200, 50, 'autoplay online', self.autoplay_online, 'red', 'green', False, True)
        self.buttons = [self.autoplay_button, self.bot_vs_bot_button, self.analysis_button, self.autoplay_online_button]

        self.start_game = Button(800, config.HEIGHT / 2 - 50, 200, 50, 'start', None, 'red', 'green', False, True)
    def run(self):
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    self.running = False

                self.handle_event(event)

    def draw(self):
        config.screen.fill('black')
        self.autoplay_button.draw(config.screen)
        self.bot_vs_bot_button.draw(config.screen)
        self.analysis_button.draw(config.screen)
        self.autoplay_online_button.draw(config.screen)
        self.start_game.draw(config.screen)
        draw_board(False)
        pygame.display.flip()

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.is_hovered = button.is_over(mouse_pos)
            self.start_game.is_hovered = self.start_game.is_over(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.is_over(mouse_pos):
                    button.is_selected = not button.is_selected
                    button.variable = not button.variable
