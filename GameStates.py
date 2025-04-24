import pygame
import chess
import config
import functions
from main import running


class CustomBoard:
    def __init__(self, board, flipped):
        self.board = board
        self.flipped = flipped
        self.selected_square = None
        self.running = True
        self.moves_played = []
        self.counter = 0

    def run(self):
        while self.running:
            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = self.get_square_from_pos(pygame.mouse.get_pos())
                    self.selected_square = chess.square(col, row)

                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

    def handle_keydown(self, event):
        if self.selected_square is None:
            print("select a square first 😡")
            return

        is_shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
        piece_color = chess.BLACK if is_shift_pressed else chess.WHITE

        key = event.key
        if key == pygame.K_p:
            self.board.set_piece_at(self.selected_square, chess.Piece(chess.PAWN, piece_color))
        elif key == pygame.K_r:
            self.board.set_piece_at(self.selected_square, chess.Piece(chess.ROOK, piece_color))
        elif key == pygame.K_n:
            self.board.set_piece_at(self.selected_square, chess.Piece(chess.KNIGHT, piece_color))
        elif key == pygame.K_b:
            self.board.set_piece_at(self.selected_square, chess.Piece(chess.BISHOP, piece_color))
        elif key == pygame.K_q:
            self.board.set_piece_at(self.selected_square, chess.Piece(chess.QUEEN, piece_color))
        elif key == pygame.K_k:
            self.board.set_piece_at(self.selected_square, chess.Piece(chess.KING, piece_color))
        elif key == pygame.K_BACKSPACE:
            self.board.remove_piece_at(self.selected_square)
        elif key == pygame.K_SPACE:
            self.running = False

    def get_square_from_pos(self, pos):
        x, y = pos
        square_size = 100
        row = y // square_size
        col = x // square_size
        if self.flipped:
            row = 7 - row
            col = col
        else:
            col = 7 - col
            row = row
        return row, col

    def draw_board(self):
        for row in range(config.ROWS):
            for col in range(config.COLS):
                color = config.LIGHT_BROWN if (row + col) % 2 == 0 else config.DARK_BROWN
                actual_row = 7 - row if self.flipped else row
                actual_col = 7 - col if self.flipped else col
                pygame.draw.rect(config.screen, color, (
                actual_col * config.SQUARE_SIZE, actual_row * config.SQUARE_SIZE, config.SQUARE_SIZE,
                config.SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(config.ROWS):
            for col in range(config.COLS):
                actual_row = 7 - row if self.flipped else row
                actual_col = 7 - col if not self.flipped else col

                square = chess.square(actual_col, actual_row)
                piece = self.board.piece_at(square)
                if piece:
                    piece_symbol = piece.symbol()
                    config.screen.blit(config.PIECE_IMAGES[piece_symbol], (col * config.SQUARE_SIZE, row * config.SQUARE_SIZE))

class NormalGame:
    def __init__(self, board, flipped):
        self.flipped = flipped
        self.board = board
        self.selected_square = None
        self.running = True

    def draw_board(self):
        for row in range(config.ROWS):
            for col in range(config.COLS):
                color = config.LIGHT_BROWN if (row + col) % 2 == 0 else config.DARK_BROWN
                actual_row = 7 - row if self.flipped else row
                actual_col = 7 - col if self.flipped else col
                pygame.draw.rect(config.screen, color, (
                actual_col * config.SQUARE_SIZE, actual_row * config.SQUARE_SIZE, config.SQUARE_SIZE,
                config.SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(config.ROWS):
            for col in range(config.COLS):
                actual_row = 7 - row if self.flipped else row
                actual_col = 7 - col if not self.flipped else col

                square = chess.square(actual_col, actual_row)
                piece = self.board.piece_at(square)
                if piece:
                    piece_symbol = piece.symbol()
                    config.screen.blit(config.PIECE_IMAGES[piece_symbol], (col * config.SQUARE_SIZE, row * config.SQUARE_SIZE))

    def run(self):
        self.draw_board()
        self.draw_pieces()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False