import chess
import random

class Bot:
    def __init__(self):
        self.piece_values = {chess.PAWN: 75,chess.KNIGHT: 320,chess.BISHOP: 330,chess.ROOK: 500,chess.QUEEN: 900,chess.KING: 20000}

        self.white_pawn_table = [
            0, 0, 0, 0, 0, 0, 0, 0,
            10, 10, 10, 10, 10, 10, 10, 10,
            0, 40, 0, 5, 5, 0, 40, 0,
            10, 10, 20, 60, 60, 20, 10, 10,
            5, 5, 10, 20, 20, 10, 5, 5,
            -5, 0, 0, -10, -10, 0, 0, -5,
            5, -5, -10, 0, 0, -10, -5, 5,
            0, 0, 0, 0, 0, 0, 0, 0
        ]

        self.white_knight_table = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50
        ]

        self.white_bishop_table = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 10, 15, 15, 10, 0, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -20, -10, -10, -10, -10, -10, -10, -20
        ]

        self.white_rook_table = [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 20, 20, 20, 20, 20, 20, 5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            0, 0, 0, 5, 5, 0, 0, 0
        ]

        self.white_queen_table = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -5, 0, 5, 10, 10, 5, 0, -5,
            -5, 0, 5, 10, 10, 5, 0, -5,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20
        ]

        self.white_king_table = [
            -50, -30, -30, -30, -30, -30, -30, -50,
            -30, -30, 0, 0, 0, 0, -30, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -20, -10, 0, 0, -10, -20, -30,
            -50, -40, -30, -20, -20, -30, -40, -50
        ]

        self.black_pawn_table = list(reversed(self.white_pawn_table))
        self.black_knight_table = list(reversed(self.white_knight_table))
        self.black_bishop_table = list(reversed(self.white_bishop_table))
        self.black_rook_table = list(reversed(self.white_rook_table))
        self.black_queen_table = list(reversed(self.white_queen_table))
        self.black_king_table = list(reversed(self.white_king_table))

    def evaluate(self, board):
        value = 0
        piece_count = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_count += 1
                piece_value = self.piece_values[piece.piece_type]
                advancement_bonus = 0

                if piece.piece_type == chess.PAWN:
                    advancement_bonus = 10 * chess.square_rank(square) if piece.color == chess.WHITE else -10 * (7 - chess.square_rank(square))

                if piece.color == chess.WHITE:
                    value += piece_value + advancement_bonus
                else:
                    value -= piece_value + advancement_bonus

        legal_moves = len(list(board.legal_moves))
        value += 3 * legal_moves if board.turn == chess.WHITE else -3 * legal_moves

        if piece_count < 10:
            value += 20 if board.turn == chess.WHITE else -20

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                mirrored_square = chess.square_mirror(square)

                if piece.color == chess.WHITE:
                    if piece.piece_type == chess.PAWN:
                        value += self.white_pawn_table[square]
                    elif piece.piece_type == chess.KNIGHT:
                        value += self.white_knight_table[square]
                    elif piece.piece_type == chess.BISHOP:
                        value += self.white_bishop_table[square]
                    elif piece.piece_type == chess.ROOK:
                        value += self.white_rook_table[square]
                    elif piece.piece_type == chess.QUEEN:
                        value += self.white_queen_table[square]
                    elif piece.piece_type == chess.KING:
                        value += self.white_king_table[square]

                else:
                    if piece.piece_type == chess.PAWN:
                        value -= self.black_pawn_table[mirrored_square]
                    elif piece.piece_type == chess.KNIGHT:
                        value -= self.black_knight_table[mirrored_square]
                    elif piece.piece_type == chess.BISHOP:
                        value -= self.black_bishop_table[mirrored_square]
                    elif piece.piece_type == chess.ROOK:
                        value -= self.black_rook_table[mirrored_square]
                    elif piece.piece_type == chess.QUEEN:
                        value -= self.black_queen_table[mirrored_square]
                    elif piece.piece_type == chess.KING:
                        value -= self.black_king_table[mirrored_square]

        value += 3 * legal_moves if board.turn == chess.WHITE else -3 * legal_moves
        return value

    def minimax(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                evaluation, _ = self.minimax(board, depth - 1, alpha, beta, False)
                if board.is_checkmate():
                    board.pop()
                    return evaluation, move
                board.pop()
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                evaluation, _ = self.minimax(board, depth - 1, alpha, beta, True)
                if board.is_checkmate():
                    board.pop()
                    return evaluation, move
                board.pop()
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_best_move(self, board):
        num_of_good_pieces = 0
        depth = 4
        for square in chess.SQUARES:
            if board.piece_at(square) != chess.PAWN and board.piece_at(square) is not None and board.piece_at(square) != "K":
                num_of_good_pieces += 1
        if num_of_good_pieces < 5:
            depth = 5
        if num_of_good_pieces < 4:
            depth = 6
        _, best_move = self.minimax(board, depth, float('-inf'), float('inf'), board.turn)
        if best_move:
            return best_move
        else:
            if board.legal_moves:
                return random.choice(list(board.legal_moves))
            else:
                print("no legal moves")