import pygame


class Button:
    def __init__(self, width, height, x, y, color, text):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.button_rect = pygame.rect()