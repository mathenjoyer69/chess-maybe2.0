import pygame
import chess
import config
from time import sleep
import pyautogui

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
        if self.board.is_checkmate():
            winner = "black" if self.counter % 2 == 0 else "white"
            print(f"{winner} won")

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
            if chess.square_rank(to_square) == 0 or chess.square_rank(to_square) == 7:
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
            print("playing: ", self.autoplay)

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

class BotVsBot:
    def __init__(self, board, bot, autoplay_online, analysis, flipped):
        self.board = board
        self.bot = bot
        self.autoplay_online_bool = autoplay_online
        self.analysis_mode = analysis
        self.flipped = flipped
        self.running = True
        self.play = True
        self.moves = []
        self.moves_played = []
        self.counter = 0

        if self.autoplay_online_bool:
            sleep(3)

    def draw_board(self):
        for row in range(config.ROWS):
            for col in range(config.COLS):
                color = config.LIGHT_BROWN if (row + col) % 2 == 0 else config.DARK_BROWN
                actual_row = 7 - row if self.flipped else row
                actual_col = 7 - col if self.flipped else col
                pygame.draw.rect(config.screen, color, (actual_col * config.SQUARE_SIZE, actual_row * config.SQUARE_SIZE, config.SQUARE_SIZE,   config.SQUARE_SIZE))

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

    @staticmethod
    def uci_to_pgn(uci_moves):
        pgn_moves = []
        for i, move in enumerate(uci_moves, start=1):
            if i % 2 == 1:
                pgn_moves.append(f"{(i + 1) // 2}: {move.uci()}")
            else:
                pgn_moves[-1] += f" {move.uci()}"
        return " ".join(pgn_moves)

    @staticmethod
    def autoplay_online(move1, analysis):
        move_str = str(move1)
        if analysis:
            coordinates = config.analysis_coordinates
        else:
            coordinates = config.normal_coordinates

        first_mouse = move_str[:2]
        last_mouse = move_str[2:]
        first_m_coordinates = coordinates[first_mouse]
        last_m_coordinates = coordinates[last_mouse]
        print(first_m_coordinates, last_m_coordinates)
        pyautogui.moveTo(first_m_coordinates)
        sleep(0.5)
        pyautogui.dragTo(last_m_coordinates, button="left")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.play = not self.play
                    print("playing", self.play)

            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()

            if self.board.is_checkmate():
                winner = "black" if self.counter % 2 == 0 else "white"
                print(f"{winner} won")
                break

            if self.play:
                self.make_move()
                sleep(0.05)

        print(self.uci_to_pgn(self.moves))

    def make_move(self):
        best_move = self.bot.get_best_move(self.board)

        self.moves.append(best_move)
        self.board.push(best_move)
        self.moves_played.append(best_move)

        if self.autoplay_online_bool:
            self.autoplay_online(best_move, self.analysis_mode)

        self.counter += 1

class AutoplayOnlineGame:
    def __init__(self, board, bot, autoplay_bool, analysis, flipped):
        self.board = board
        self.bot = bot
        self.autoplay_bool = autoplay_bool
        self.analysis = analysis
        self.flipped = flipped
        self.running = True
        self.counter = 0
        self.moves_played = []
        self.selected_square = None

    @staticmethod
    def autoplay_online(move1, analysis):
        move_str = str(move1)
        if analysis:
            coordinates = config.analysis_coordinates
        else:
            coordinates = config.normal_coordinates

        first_mouse = move_str[:2]
        last_mouse = move_str[2:]
        first_m_coordinates = coordinates[first_mouse]
        last_m_coordinates = coordinates[last_mouse]
        print(first_m_coordinates, last_m_coordinates)
        pyautogui.moveTo(first_m_coordinates)
        sleep(0.5)
        pyautogui.dragTo(last_m_coordinates, button="left")

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
        while self.running:
            self.sync_moves_online()
            self.draw()

            if self.board.is_checkmate():
                winner = "black" if self.counter % 2 == 0 else "white"
                print(f"{winner} won")
                self.running = False

            self.handle_events()

    def draw(self):
        self.draw_board()
        self.draw_pieces()
        pygame.display.flip()

    def sync_moves_online(self):
        if self.moves_played:
            for move in self.moves_played:
                self.autoplay_online(move, self.analysis)
                sleep(1)
            self.moves_played.clear()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

    def handle_mouse_click(self):
        row, col = self.get_square_from_pos(pygame.mouse.get_pos())
        square = chess.square(col, row)

        if self.selected_square is None:
            if self.board.piece_at(square):
                self.selected_square = square
        else:
            piece = self.board.piece_at(self.selected_square)
            if piece and piece.piece_type == chess.PAWN and (chess.square_rank(square) in [0, 7]):
                move = chess.Move(self.selected_square, square, promotion=chess.QUEEN)
            else:
                move = chess.Move(self.selected_square, square)

            if move in self.board.legal_moves:
                self.board.push(move)
                self.counter += 1
            else:
                print("illegal move")

            self.selected_square = None
            print(f"you clicked {self.board.piece_at(square)}")

    def handle_keydown(self, event):
        if event.key == pygame.K_SPACE:
            best_move = self.bot.get_best_move(self.board)
            if best_move:
                print(f"bot chose: {best_move}")
                self.board.push(best_move)
                self.moves_played.append(best_move)
                sleep(1)
                self.autoplay_online(best_move, self.analysis)
                self.counter += 1
        elif self.autoplay_bool:
            self.autoplay_bot_move()

    def autoplay_bot_move(self):
        best_move = self.bot.get_best_move(self.board)
        if best_move:
            print(f"autoplay move: {best_move}")
            self.board.push(best_move)
            self.moves_played.append(best_move)
            sleep(1)
            self.autoplay_online(best_move, self.analysis)
            self.counter += 1