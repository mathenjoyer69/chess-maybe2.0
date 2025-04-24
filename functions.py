import config
import chess

class Functions:
    def __init__(self, board, flipped):
        self.flipped = flipped
        self.board = board

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
