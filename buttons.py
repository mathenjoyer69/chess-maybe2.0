import pygame

pygame.init()
font = pygame.font.SysFont(None, 24)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, state):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.is_selected = state

    def draw(self, surface):
        color = self.hover_color if self.is_hovered or self.is_selected else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=5)

        text_surface = font.render(self.text, True, (255, 255, 255) if self.is_hovered or self.is_selected else (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_over(self, pos):
        return self.rect.collidepoint(pos)