import pygame
import bot

pygame.init()
font = pygame.font.SysFont(None, 24)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, state, use_able):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.is_selected = state
        self.use_able = use_able

    def draw(self, surface):
        color = self.hover_color if self.is_hovered or self.is_selected else self.color
        if not self.use_able:
            color = (100, 100, 100)

        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=5)

        text_surface = font.render(self.text, True, (255, 255, 255) if self.is_hovered or self.is_selected else (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

class ChessClock:
    def __init__(self, x, y, width, height):
        self.start_time = pygame.time.get_ticks() / 1000
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_selected = False
        #self.mode = mode
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(x, y, width, height)
        self.black_time_seconds = 300
        self.white_time_seconds = 300
        self.black_time = self.seconds_to_minutes(self.black_time_seconds)
        self.white_time = self.seconds_to_minutes(self.white_time_seconds)
        self.timer = f"{int(self.white_time['minutes'])}:{int(self.white_time['seconds'])} || {int(self.black_time['minutes'])}:{int(self.black_time['seconds'])}"

    @staticmethod
    def seconds_to_minutes(seconds):
        minutes = seconds // 60
        reminder_seconds = seconds - (minutes * 60)
        return {'minutes' : minutes, 'seconds' : reminder_seconds}

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=5)

        text_surface = font.render(self.timer, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, turn, bot_time):
        current_time = pygame.time.get_ticks() / 1000
        passed_time = current_time - self.start_time

        if turn:
            self.white_time_seconds -= passed_time
            self.black_time_seconds -= bot_time
        else:
            self.black_time_seconds -= passed_time


        self.start_time = current_time

        self.white_time = self.seconds_to_minutes(self.white_time_seconds)
        self.black_time = self.seconds_to_minutes(self.black_time_seconds)

        self.timer = f"{int(self.white_time['minutes'])}:{int(self.white_time['seconds'])} || {int(self.black_time['minutes'])}:{int(self.black_time['seconds'])}"
