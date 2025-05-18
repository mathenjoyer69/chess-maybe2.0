import config
from buttons import *
from functions import draw_board, draw_pieces


class PreScreen:
    def __init__(self, board):
        self.running = True
        self.quit = True
        self.board = board
        self.autoplay_button = Button(800, 0, 200, 50, 'auto play', False, 'red', 'green', False, True)
        self.bot_vs_bot_button = Button(800, 50, 200, 50, 'bot vs bot', False, 'red', 'green', False, True)
        self.analysis_button = Button(800, 100, 200, 50, 'analysis', False, 'red', 'green', False, True)
        self.autoplay_online_button = Button(800, 150, 200, 50, 'autoplay online', False, 'red', 'green', False, True)
        self.custom_board_button = Button(800, 200, 200, 50, 'custom board', False, 'red', 'green', False, True)
        self.player_color_button = Button(800, 250, 200, 50, 'white', False, 'white', 'black', False, True)
        #self.blitz_button
        self.buttons = [self.autoplay_button, self.bot_vs_bot_button, self.analysis_button, self.autoplay_online_button, self.custom_board_button, self.player_color_button]
        self.start_game = Button(800, config.HEIGHT / 2 - 50, 200, 50, 'start', self.running, 'red', 'green', False, True)

    def run(self):
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = False
                    self.running = False

                self.handle_event(event)

    def draw(self):
        config.screen.fill('black')
        for button in self.buttons:
            button.draw(config.screen)
        self.start_game.draw(config.screen)
        draw_board(self.player_color_button.variable)
        draw_pieces(self.player_color_button.variable, self.board)
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
            if self.start_game.is_over(mouse_pos):
                self.start_game.is_selected = not self.start_game.is_selected
                self.running = False

    def get_values(self):
        return {'autoplay':self.autoplay_button.variable, 'bot_vs_bot':self.bot_vs_bot_button.variable,
                'analysis':self.analysis_button.variable, 'autoplay_online':self.autoplay_online_button.variable,
                'custom_board':self.custom_board_button.variable, 'player_color':self.player_color_button.variable}