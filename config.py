import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
DARK_BROWN = (79, 55, 42)
LIGHT_BROWN = (237, 204, 155)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
PIECE_IMAGES = {}
PIECES = {'p': 'bp.png', 'r': 'br.png', 'n': 'bn.png', 'b': 'bb.png', 'q': 'bq.png', 'k': 'bk.png', 'P': 'p.png', 'R': 'r.png', 'N': 'n.png', 'B': 'b.png', 'Q': 'q.png', 'K': 'k.png'}
pygame.display.set_caption("chess")