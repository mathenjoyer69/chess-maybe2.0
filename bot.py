import chess
import random
import pygame

class Bot:
    def __init__(self):
        self.passed_time = 0
        self.start_time = pygame.time.get_ticks() / 1000
        self.piece_values = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330, chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000}

        self.white_pawn_table = [
            0, 0, 0, 0, 0, 0, 0, 0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5, 5, 10, 70, 70, 10, 5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, -5, -10, 0, 0, -10, -5, 5,
            5, 10, 10, -20, -20, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0
        ]

        self.white_knight_table = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50
        ]

        self.white_bishop_table = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 5, 5, 5, 5, 5, 5, -10,
            -10, 0, 5, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20
        ]

        self.white_rook_table = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0
        ]

        self.white_queen_table = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -5, 0, 5, 5, 5, 5, 0, -5,
            0, 0, 5, 5, 5, 5, 0, -5,
            -10, 5, 5, 5, 5, 5, 0, -10,
            -10, 0, 5, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20
        ]

        self.white_king_midgame_table = [
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            20, 20, 0, 0, 0, 0, 20, 20,
            20, 30, 10, 0, 0, 10, 30, 20
        ]

        self.white_king_endgame_table = [
            -50, -40, -30, -20, -20, -30, -40, -50,
            -30, -20, -10, 0, 0, -10, -20, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -30, 0, 0, 0, 0, -30, -30,
            -50, -30, -30, -30, -30, -30, -30, -50
        ]

        self.black_pawn_table = list(reversed(self.white_pawn_table))
        self.black_knight_table = list(reversed(self.white_knight_table))
        self.black_bishop_table = list(reversed(self.white_bishop_table))
        self.black_rook_table = list(reversed(self.white_rook_table))
        self.black_queen_table = list(reversed(self.white_queen_table))
        self.black_king_midgame_table = list(reversed(self.white_king_midgame_table))
        self.black_king_endgame_table = list(reversed(self.white_king_endgame_table))

        self.transposition_table = {}

    @staticmethod
    def is_endgame(board):
        major_pieces = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and (piece.piece_type == chess.QUEEN or piece.piece_type == chess.ROOK):
                major_pieces += 1

        return major_pieces <= 3

    def evaluate(self, board):
        if board.is_checkmate():
            return float('-inf') if board.turn else float('inf')

        if board.is_stalemate() or board.is_insufficient_material():
            return

        value = 0
        piece_count = 0
        endgame = self.is_endgame(board)

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_count += 1
                piece_value = self.piece_values[piece.piece_type]

                advancement_bonus = 0
                if piece.piece_type == chess.PAWN:
                    if piece.color == chess.WHITE:
                        advancement_bonus = 10 * chess.square_rank(square)
                    else:
                        advancement_bonus = -10 * (7 - chess.square_rank(square))

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
                        if endgame:
                            value += self.white_king_endgame_table[square]
                        else:
                            value += self.white_king_midgame_table[square]
                else:
                    if piece.piece_type == chess.PAWN:
                        value -= self.black_pawn_table[square]
                    elif piece.piece_type == chess.KNIGHT:
                        value -= self.black_knight_table[square]
                    elif piece.piece_type == chess.BISHOP:
                        value -= self.black_bishop_table[square]
                    elif piece.piece_type == chess.ROOK:
                        value -= self.black_rook_table[square]
                    elif piece.piece_type == chess.QUEEN:
                        value -= self.black_queen_table[square]
                    elif piece.piece_type == chess.KING:
                        if endgame:
                            value -= self.black_king_endgame_table[square]
                        else:
                            value -= self.black_king_midgame_table[square]

        white_pawn_files = [0] * 8
        black_pawn_files = [0] * 8
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                file = chess.square_file(square)
                if piece.color == chess.WHITE:
                    white_pawn_files[file] += 1
                else:
                    black_pawn_files[file] += 1

        for i in range(8):
            if white_pawn_files[i] > 1:
                value -= 10 * (white_pawn_files[i] - 1)
            if black_pawn_files[i] > 1:
                value += 10 * (black_pawn_files[i] - 1)

        if board.has_kingside_castling_rights(chess.WHITE):
            value += 20
        if board.has_queenside_castling_rights(chess.WHITE):
            value += 15
        if board.has_kingside_castling_rights(chess.BLACK):
            value -= 20
        if board.has_queenside_castling_rights(chess.BLACK):
            value -= 15

        white_bishop_count = 0
        black_bishop_count = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.BISHOP:
                if piece.color == chess.WHITE:
                    white_bishop_count += 1
                else:
                    black_bishop_count += 1

        if white_bishop_count >= 2:
            value += 30
        if black_bishop_count >= 2:
            value -= 30

        self.current_time = pygame.time.get_ticks() / 1000
        self.passed_time = self.current_time - self.start_time
        return value

    def minimax(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board), None

        board_hash = board.fen()
        if board_hash in self.transposition_table and self.transposition_table[board_hash][0] >= depth:
            return self.transposition_table[board_hash][1], self.transposition_table[board_hash][2]

        best_move = None
        ordered_moves = []
        for move in board.legal_moves:
            if board.is_capture(move):
                ordered_moves.insert(0, move)
            else:
                ordered_moves.append(move)

        if maximizing:
            max_eval = float('-inf')
            for move in ordered_moves:
                board.push(move)

                if board.is_checkmate():
                    eval_val = float('inf')
                    board.pop()
                    return eval_val, move

                evaluation, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()

                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move

                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break

            self.transposition_table[board_hash] = (depth, max_eval, best_move)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in ordered_moves:
                board.push(move)

                if board.is_checkmate():
                    eval_val = float('-inf')
                    board.pop()
                    return eval_val, move

                evaluation, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()

                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move

                beta = min(beta, evaluation)
                if beta <= alpha:
                    break

            self.transposition_table[board_hash] = (depth, min_eval, best_move)
            return min_eval, best_move

    def get_best_move(self, board):
        num_of_pieces = sum(1 for square in chess.SQUARES if board.piece_at(square) is not None)
        if num_of_pieces > 20:
            depth = 3
        elif num_of_pieces > 10:
            depth = 4
        elif num_of_pieces > 5:
            depth = 5
        else:
            depth = 6

        print("transposition table length: ", len(self.transposition_table))
        self.transposition_table.clear()

        _, best_move = self.minimax(board, depth, float('-inf'), float('inf'), board.turn == chess.WHITE)

        if best_move:
            return best_move
        elif list(board.legal_moves):
            return random.choice(list(board.legal_moves))
        else:
            print("no legal moves")
            return None

    def get_move_time(self):
        return self.passed_time/100

