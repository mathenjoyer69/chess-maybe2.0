from config import *
import chess

def draw_board(flipped):
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            actual_row = 7 - row if flipped else row
            actual_col = 7 - col if flipped else col
            pygame.draw.rect(screen, color,(actual_col * SQUARE_SIZE, actual_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(flipped, board):
    for row in range(ROWS):
        for col in range(COLS):
            actual_row = 7 - row if flipped else row
            actual_col = 7 - col if not flipped else col

            square = chess.square(actual_col, actual_row)
            piece = board.piece_at(square)
            if piece:
                piece_symbol = piece.symbol()
                screen.blit(PIECE_IMAGES[piece_symbol], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_square_from_pos(pos, flipped):
    x, y = pos
    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
    actual_row = 7 - row if flipped else row
    actual_col = 7 - col if not flipped else col
    return actual_row, actual_col

def check_game_end(board):
    running = False
    if board.is_checkmate():
        print("black won") if board.turn == chess.WHITE else print("white won")
    return running
