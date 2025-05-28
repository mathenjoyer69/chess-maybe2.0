import datetime
import chess
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
        self.player_color_button = ColorButton(800, 250, 200, 50, 'white', 'black', False)
        #self.blitz_button
        self.buttons = [self.autoplay_button, self.bot_vs_bot_button, self.analysis_button, self.autoplay_online_button, self.custom_board_button]
        self.start_game = Button(800, config.HEIGHT / 2 - 50, 200, 50, 'start', self.running, 'red', 'green', False, True)
        font1 = pygame.font.SysFont(None, 35)
        x = datetime.datetime.now()
        self.text_surface = font1.render(f'chess game by ariel', True, (255, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=(config.WIDTH//2-100, config.HEIGHT//2))
        self.rect = pygame.Rect(self.text_rect.x, self.text_rect.y, self.text_rect.width, self.text_rect.height)
        self.text_surface1 = font1.render(f'date: {x.strftime("%x")}', True, (255, 0, 0))
        self.text_rect1 = self.text_surface1.get_rect(center=(config.WIDTH//2-100, config.HEIGHT//2+self.text_rect.height))
        self.rect1 = pygame.Rect(self.text_rect1.x, self.text_rect1.y, self.text_rect1.width, self.text_rect1.height)
        self.texts = [(self.text_surface, self.text_rect), (self.text_surface1, self.text_rect1)]

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
        if not self.player_color_button.is_selected:
            self.player_color_button.draw_black(config.screen)
        else:
            self.player_color_button.draw_white(config.screen)
        self.start_game.draw(config.screen)
        draw_board(self.player_color_button.is_selected)
        draw_pieces(self.player_color_button.is_selected, self.board)
        pygame.draw.rect(config.screen, 'black', self.rect)
        pygame.draw.rect(config.screen, 'black', self.rect1)
        for surface, rect in self.texts:
            config.screen.blit(surface, rect)
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
            if self.player_color_button.is_over(mouse_pos):
                self.player_color_button.is_selected = not self.player_color_button.is_selected
            if self.start_game.is_over(mouse_pos):
                self.start_game.is_selected = not self.start_game.is_selected
                self.running = False
        if self.custom_board_button.variable:
            self.board = chess.Board(None)
        else:
            self.board = chess.Board()
    def get_values(self):
        return {'autoplay':self.autoplay_button.variable, 'bot_vs_bot':self.bot_vs_bot_button.variable,
                'analysis':self.analysis_button.variable, 'autoplay_online':self.autoplay_online_button.variable,
                'custom_board':self.custom_board_button.variable, 'player_color':self.player_color_button.is_selected}
