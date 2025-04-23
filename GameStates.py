import pygame
import chess

class CustomBoard:
    def __init__(self, board, flipped=False):
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
            print("Select a square first 😡")
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
            col = 7 - col
        return row, col

    def draw_board(self):
        # Replace with your draw_board logic
        draw_board(self.flipped)

    def draw_pieces(self):
        # Replace with your draw_pieces logic
        draw_pieces(self.flipped)
