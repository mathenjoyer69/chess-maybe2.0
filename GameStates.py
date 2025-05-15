from time import sleep
import pyautogui
import pygame.mouse

from functions import *
import config

class CustomBoard:
    def __init__(self, board, flipped, autoplay, autoplay_online):
        self.board = board
        self.flipped = flipped
        self.selected_square = None
        self.running = True
        self.moves_played = []
        self.counter = 0
        self.autoplay_bool = autoplay
        self.autoplay_online_bool = autoplay_online

    def run(self):
        while self.running:
            print(config.custom_board_bool)
            draw_board(self.flipped)
            draw_pieces(self.flipped, self.board)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = get_square_from_pos(pygame.mouse.get_pos(), self.flipped)
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
            config.custom_board_bool = False


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

        self.autoplay_button = Button(800, 0, 200, 50, 'auto play', 'red', 'green', self.autoplay)

    def run(self):
        while self.running and not self.autoplay_online and not self.custom_board and not self.bot_vs_bot:
            self.update_screen()

            if not self.player_color and self.autoplay:
                self.make_bot_move()

            if not any(self.board.legal_moves):
                check_game_end(self.board)
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse()
                elif event.type == pygame.KEYDOWN and not self.autoplay:
                    self.handle_keydown(event)

                self.handle_event(event)

            if self.autoplay:
                self.handle_autoplay()

    def update_screen(self):
        draw_board(self.flipped)
        draw_pieces(self.flipped, self.board)
        self.autoplay_button.draw(screen)
        pygame.display.flip()

    def make_bot_move(self):
        bot_move = self.bot.get_best_move(self.board)
        if bot_move in self.board.legal_moves:
            self.board.push(bot_move)
            self.moves1.append(bot_move)
            self.player_color = not self.player_color

    def handle_mouse(self):
        (mx, my) = pygame.mouse.get_pos()
        if mx <= 800:
            row, col = get_square_from_pos((mx, my), self.flipped)
            square = chess.square(col, row)
            print(square)
            if self.selected_square is None:
                if self.board.piece_at(square):
                    self.selected_square = square
            else:
                self.make_move(square)
                self.selected_square = None

            if col < 7:
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

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            self.autoplay_button.is_hovered = self.autoplay_button.is_over(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.autoplay_button.is_over(mouse_pos):
                self.autoplay = not self.autoplay
                config.autoplay_bool = self.autoplay
                self.autoplay_button.is_selected = not self.autoplay_button.is_selected

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
            coordinates = analysis_coordinates
        else:
            coordinates = normal_coordinates

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

            draw_board(self.flipped)
            draw_pieces(self.flipped, self.board)
            pygame.display.flip()

            if self.board.is_checkmate():
                check_game_end(self.board)

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
            coordinates = analysis_coordinates
        else:
            coordinates = normal_coordinates

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
            self.sync_moves_online()
            draw_board(self.flipped)
            draw_pieces(self.flipped, self.board)
            pygame.display.flip()

            if self.board.is_checkmate():
                winner = "white" if self.counter % 2 == 0 else "black"
                print(f"{winner} won")
                self.running = False

            self.handle_events()

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
        row, col = get_square_from_pos(pygame.mouse.get_pos(), self.flipped)
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