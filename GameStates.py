import pygame
import chess
import config

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
                pygame.draw.rect(config.screen, color, (actual_col * config.SQUARE_SIZE, actual_row * config.SQUARE_SIZE, config.SQUARE_SIZE, config.SQUARE_SIZE))

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
    def __init__(self, board, bot, flipped, autoplay, autoplay_online, player_color, custom_board=False, bot_vs_bot=False):
        self.board = board
        self.bot = bot
        self.flipped = flipped
        self.autoplay = autoplay
        self.autoplay_online = autoplay_online
        self.custom_board = custom_board
        self.bot_vs_bot = bot_vs_bot
        self.running = True
        self.counter = 0
        self.selected_square = None
        self.moves_played = []
        self.moves1 = []
        self.player_color = player_color

    def draw_board(self):
        for row in range(config.ROWS):
            for col in range(config.COLS):
                color = config.LIGHT_BROWN if (row + col) % 2 == 0 else config.DARK_BROWN
                actual_row = 7 - row if self.flipped else row
                actual_col = 7 - col if self.flipped else col
                pygame.draw.rect(config.screen, color, (actual_col * config.SQUARE_SIZE, actual_row * config.SQUARE_SIZE, config.SQUARE_SIZE, config.SQUARE_SIZE))

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

    def run(self):
        while self.running and not self.autoplay_online and not self.custom_board and not self.bot_vs_bot:
            self.update_screen()

            if not self.player_color and self.autoplay:
                self.make_bot_move()

            if not any(self.board.legal_moves):
                self.check_game_end()
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse()
                elif event.type == pygame.KEYDOWN and not self.autoplay:
                    self.handle_keydown(event)

            if self.autoplay:
                self.handle_autoplay()

    def update_screen(self):
        self.draw_board()
        self.draw_pieces()
        pygame.display.flip()

    def make_bot_move(self):
        bot_move = self.bot.get_best_move(self.board)
        if bot_move in self.board.legal_moves:
            self.board.push(bot_move)
            self.moves1.append(bot_move)
            self.player_color = not self.player_color

    def check_game_end(self):
        self.running = False
        if not self.board.is_check():
            print("draw")
        elif self.counter % 2 == 0:
            print("black won")
        else:
            print("white won")

    def handle_mouse(self):
        row, col = self.get_square_from_pos(pygame.mouse.get_pos())
        square = chess.square(col, row)
        print(square)
        if self.selected_square is None:
            if self.board.piece_at(square):
                self.selected_square = square
        else:
            self.make_move(square)
            self.selected_square = None

        print(f"you clicked {self.board.piece_at(square)}")

    def make_move(self, to_square):
        if self.board.piece_at(self.selected_square) and self.board.piece_at(self.selected_square).piece_type == chess.PAWN:
            if chess.square_rank(to_square) in [0, 7]:
                move = chess.Move(self.selected_square, to_square, promotion=chess.QUEEN)
            else:
                move = chess.Move(self.selected_square, to_square)
        else:
            move = chess.Move(self.selected_square, to_square)

        if move in self.board.legal_moves:
            self.board.push(move)
            self.moves1.append(move)
            self.moves_played.append(move)
            self.counter += 1
            self.flipped = not self.flipped
            print(move)
        else:
            print("illegal move")

    def handle_keydown(self, event):
        if event.key == pygame.K_SPACE:
            best_move = self.bot.get_best_move(self.board)
            if best_move in self.board.legal_moves:
                self.board.push(best_move)
                self.moves1.append(best_move)
                print(f"bot chose: {best_move}")
        elif event.key == pygame.K_d:
            self.autoplay = not self.autoplay
            print("autoplay: ", self.autoplay)
        elif event.key == pygame.K_a:
            self.autoplay_online = not self.autoplay_online
            self.autoplay = True
            print("autoplay online: ", self.autoplay_online)

    def handle_autoplay(self):
        if self.counter % 2 != 0:
            best_move = self.bot.get_best_move(self.board)
            print(f"bot move: {best_move}")
            if best_move in self.board.legal_moves:
                self.board.push(best_move)
                self.moves1.append(best_move)
                self.moves_played.append(best_move)
                self.counter += 1
                self.flipped = not self.flipped

class AutoPlayOnline:
    def __init__(self, autoplay_online_bool, flipped, player_color, board):
        self.board = board