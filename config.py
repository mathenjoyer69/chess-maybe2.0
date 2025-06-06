import pygame
import bot

WIDTH, HEIGHT = 1000, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = 800 // COLS
DARK_BROWN = (79, 55, 42)
LIGHT_BROWN = (237, 204, 155)
start = False
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 24)
PIECE_IMAGES = {}
PIECES = {'p': 'bp.png', 'r': 'br.png', 'n': 'bn.png', 'b': 'bb.png', 'q': 'bq.png', 'k': 'bk.png', 'P': 'p.png', 'R': 'r.png', 'N': 'n.png', 'B': 'b.png', 'Q': 'q.png', 'K': 'k.png'}
for piece, filename in PIECES.items():
    PIECE_IMAGES[piece] = pygame.image.load(f'assets/{filename}')
    PIECE_IMAGES[piece] = pygame.transform.scale(PIECE_IMAGES[piece], (SQUARE_SIZE, SQUARE_SIZE))
pygame.display.set_caption("chess")

square_to_number = {"a1":0,"a2":8,"a3":16,"a4":24,"a5":32,"a6":40,"a7":48,"a8":56,
                    "b1":1,"b2":9,"b3":17,"b4":25,"b5":33,"b6":41,"b7":49,"b8":57,
                    "c1":2,"c2":10,"c3":18,"c4":26,"c5":34,"c6":42,"c7":50,"c8":58,
                    "d1":3,"d2":11,"d3":19,"d4":27,"d5":35,"d6":43,"d7":51,"d8":59,
                    "e1":4,"e2":12,"e3":20,"e4":28,"e5":36,"e6":44,"e7":52,"e8":60,
                    "f1":5,"f2":13,"f3":21,"f4":29,"f5":37,"f6":45,"f7":53,"f8":61,
                    "g1":6,"g2":14,"g3":22,"g4":30,"g5":38,"g6":46,"g7":54,"g8":62,
                    "h1":7,"h2":15,"h3":23,"h4":31,"h5":39,"h6":47,"h7":55,"h8":63}

analysis_coordinates = {"a1": (435, 905), "a2": (435, 805), "a3": (435, 705), "a4": (435, 605), "a5": (435, 505),
                        "a6": (435, 405), "a7": (435, 305), "a8": (435, 205),
                        "b1": (535, 905), "b2": (535, 805), "b3": (535, 705), "b4": (535, 605), "b5": (535, 505),
                        "b6": (535, 405), "b7": (535, 305), "b8": (535, 205),
                        "c1": (635, 905), "c2": (635, 805), "c3": (635, 705), "c4": (635, 605), "c5": (635, 505),
                        "c6": (635, 405), "c7": (635, 305), "c8": (635, 205),
                        "d1": (735, 905), "d2": (735, 805), "d3": (735, 705), "d4": (735, 605), "d5": (735, 505),
                        "d6": (735, 405), "d7": (735, 305), "d8": (735, 205),
                        "e1": (835, 905), "e2": (835, 805), "e3": (835, 705), "e4": (835, 605), "e5": (835, 505),
                        "e6": (835, 405), "e7": (835, 305), "e8": (835, 205),
                        "f1": (935, 905), "f2": (935, 805), "f3": (935, 705), "f4": (935, 605), "f5": (935, 505),
                        "f6": (935, 405), "f7": (935, 305), "f8": (935, 205),
                        "g1": (1035, 905), "g2": (1035, 805), "g3": (1035, 705), "g4": (1035, 605), "g5": (1035, 505),
                        "g6": (1035, 405), "g7": (1035, 305), "g8": (1035, 205),
                        "h1": (1135, 905), "h2": (1135, 805), "h3": (1135, 705), "h4": (1135, 605), "h5": (1135, 505),
                        "h6": (1135, 405), "h7": (1135, 305), "h8": (1135, 205),
                        }

normal_coordinates = {"a1": (275, 905), "a2": (275, 805), "a3": (275, 705), "a4": (275, 605), "a5": (275, 505),
                      "a6": (275, 405), "a7": (275, 305), "a8": (275, 205),
                      "b1": (375, 905), "b2": (375, 805), "b3": (375, 705), "b4": (375, 605), "b5": (375, 505),
                      "b6": (375, 405), "b7": (375, 305), "b8": (375, 205),
                      "c1": (475, 905), "c2": (475, 805), "c3": (475, 705), "c4": (475, 605), "c5": (475, 505),
                      "c6": (475, 405), "c7": (475, 305), "c8": (475, 205),
                      "d1": (575, 905), "d2": (575, 805), "d3": (575, 705), "d4": (575, 605), "d5": (575, 505),
                      "d6": (575, 405), "d7": (575, 305), "d8": (575, 205),
                      "e1": (675, 905), "e2": (675, 805), "e3": (675, 705), "e4": (675, 605), "e5": (675, 505),
                      "e6": (675, 405), "e7": (675, 305), "e8": (675, 205),
                      "f1": (775, 905), "f2": (775, 805), "f3": (775, 705), "f4": (775, 605), "f5": (775, 505),
                      "f6": (775, 405), "f7": (775, 305), "f8": (775, 205),
                      "g1": (875, 905), "g2": (875, 805), "g3": (875, 705), "g4": (875, 605), "g5": (875, 505),
                      "g6": (875, 405), "g7": (875, 305), "g8": (875, 205),
                      "h1": (975, 905), "h2": (975, 805), "h3": (975, 705), "h4": (975, 605), "h5": (975, 505),
                      "h6": (975, 405), "h7": (975, 305), "h8": (975, 205),
                      }

chess_bot = bot.Bot()