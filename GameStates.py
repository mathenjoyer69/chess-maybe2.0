import time
import pyautogui
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
        self.custom_bool = False
        self.start_game = Button(800, HEIGHT//2, 200, 50, 'start game', None, 'red', 'green', False, True)
        self.back_to_main = Button(800, HEIGHT//2+50, 200, 50, 'back', False, 'red', 'green', False, True)

    def run(self):
        while self.running:
            config.screen.fill('black')
            (mx, my) = pygame.mouse.get_pos()
            draw_board(self.flipped)
            draw_pieces(self.flipped, self.board)
            self.start_game.draw(config.screen)
            self.back_to_main.draw(config.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mx <= 800:
                        row, col = get_square_from_pos((mx, my), self.flipped)
                        self.selected_square = chess.square(col, row)
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

                self.handle_event(event)

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
            self.running = False

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            self.start_game.is_hovered = self.start_game.is_over(mouse_pos)
            self.back_to_main.is_hovered = self.back_to_main.is_over(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_game.is_over(mouse_pos):
                self.start_game.is_selected = not self.start_game.is_selected
                self.running = False

            if self.back_to_main.is_over(mouse_pos):
                self.custom_bool = not self.custom_bool
                self.back_to_main.is_selected = not self.back_to_main.is_selected
                self.running = False

class NormalGame:
    def __init__(self, board, bot, flipped, autoplay, autoplay_online, player_color, custom_board=False, bot_vs_bot=False):
        self.board = board
        self.bot = bot
        self.flipped = flipped
        self.original_flipped = flipped
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
        self.reset = False
        self.autoplay_button = Button(800, HEIGHT//2 - 50, 200, 50, 'auto play', self.autoplay, 'red', 'green', self.autoplay, True)
        self.timer = ChessClock(800, HEIGHT//2, 200, 50)
        self.reset_button = Button(800, HEIGHT//2 + 50, 200, 50, 'reset game', None, 'white', 'green', self.reset, True)
        self.back_to_main = Button(800, HEIGHT//2 - 100, 200, 50, 'back', False, 'red', 'green', False, True)

    def run(self):
        while self.running and not self.autoplay_online and not self.custom_board and not self.bot_vs_bot:
            for event in pygame.event.get():
                self.handle_event(event)
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse()

            self.update_screen()

            if not self.player_color and self.autoplay:
                self.make_bot_move()

            if not any(self.board.legal_moves):
                check_game_end(self.board)
                break

            if self.timer.win_by_time():
                print(f'{self.timer.winner} won by time')
                break

            if self.autoplay:
                self.handle_autoplay()

    def update_screen(self):
        screen.fill('black')
        draw_board(self.flipped)
        draw_pieces(self.flipped, self.board)
        self.autoplay_button.draw(screen)
        self.reset_button.draw(screen)
        self.timer.update(self.board.turn == chess.WHITE, self.bot.get_move_time())
        self.bot.passed_time = 0
        self.timer.draw(screen)
        self.back_to_main.draw(config.screen)
        pygame.display.flip()

    def make_bot_move(self):
        self.bot.start_time = pygame.time.get_ticks() / 1000
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
            print(self.autoplay_button.variable, 1111)
            if not self.autoplay_button.variable:
                self.flipped = not self.flipped
            print(move)
        else:
            print("illegal move")

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            self.autoplay_button.is_hovered = self.autoplay_button.is_over(mouse_pos)
            self.reset_button.is_hovered = self.reset_button.is_over(mouse_pos)
            self.back_to_main.is_hovered = self.back_to_main.is_over(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.autoplay_button.is_over(mouse_pos):
                self.autoplay_button.variable = not self.autoplay_button.variable
                self.autoplay = not self.autoplay
                self.autoplay_button.is_selected = not self.autoplay_button.is_selected

            if self.back_to_main.is_over(mouse_pos):
                self.back_to_main.is_selected = not self.back_to_main.is_selected
                self.back_to_main.variable = not self.back_to_main.variable
                self.running = False

            if self.reset_button.is_over(mouse_pos):
                self.reset_button.is_over(mouse_pos)
                self.reset_button.is_selected = not self.reset_button.is_selected
                if self.reset_button.is_selected:
                    self.board = chess.Board()
                    self.flipped = self.original_flipped
                    self.reset_button.is_selected = False

            if self.timer.is_over(mouse_pos):
                self.timer.is_selected = not self.timer.is_selected
                self.timer.start_time = pygame.time.get_ticks() / 1000

    def handle_autoplay(self):
        if self.counter % 2 != 0:
            best_move = self.bot.get_best_move(self.board)
            print(f"bot move: {best_move}")
            if best_move in self.board.legal_moves:
                self.board.push(best_move)
                self.moves1.append(best_move)
                self.moves_played.append(best_move)
                self.counter += 1
#                self.flipped = not self.flipped

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
        self.clock = pygame.time.Clock()
        self.last_move_time = time.time()
        self.move_delay = 0.5
        self.bot_thread = None
        self.bot_is_moving = False

        self.pause_button = Button(800, HEIGHT//2, 200, 50, 'pause', False, 'red', 'green', False, True)
        self.back_to_main = Button(800, HEIGHT//2 - 50, 200, 50, 'back', False, 'red', 'green', False, True)
        #self.buttons = [self.pause_button]
        if self.autoplay_online_bool:
            time.sleep(3)

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
        time.sleep(0.5)
        pyautogui.dragTo(last_m_coordinates, button="left")

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.play = not self.play
                self.handle_event(event)

            if self.board.is_checkmate():
                check_game_end(self.board)

            current_time = time.time()
            if self.play and (current_time - self.last_move_time >= self.move_delay):
                self.make_move()
                self.last_move_time = current_time

    def draw(self):
        config.screen.fill('black')
        draw_board(self.flipped)
        draw_pieces(self.flipped, self.board)
        self.pause_button.draw(config.screen)
        self.back_to_main.draw(config.screen)
        pygame.display.flip()

    def make_move(self):
        if not self.pause_button.variable:
            best_move = self.bot.get_best_move(self.board)

            self.moves.append(best_move)
            self.board.push(best_move)
            self.moves_played.append(best_move)

            if self.autoplay_online_bool:
                self.autoplay_online(best_move, self.analysis_mode)

            self.counter += 1

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEMOTION:
            self.pause_button.is_hovered = self.pause_button.is_over(mouse_pos)
            self.back_to_main.is_hovered = self.back_to_main.is_over(mouse_pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.pause_button.is_over(mouse_pos):
                self.pause_button.is_selected = not self.pause_button.is_selected
                self.pause_button.variable = not self.pause_button.variable

            if self.back_to_main.is_over(mouse_pos):
                self.back_to_main.is_selected = not self.back_to_main.is_selected
                self.back_to_main.variable = not self.back_to_main.variable
                self.running = False

class AutoplayOnlineGame:
    def __init__(self, board, bot, autoplay_bool, analysis, flipped):
        self.board = board
        self.bot = bot
        self.autoplay_bool = autoplay_bool
        self.analysis = analysis
        self.flipped = flipped
        self.running = True
        self.selected_square = None
        self.last_move_time = time.time()
        self.move_delay = 1.0

        self.reset_button = Button(800, HEIGHT//2 + 50, 200, 50, 'reset game', None, 'white', 'green', False, True)
        self.back_to_main = Button(800, HEIGHT//2 - 100, 200, 50, 'back', False, 'red', 'green', False, True)
        self.buttons = [self.reset_button, self.back_to_main]

    @staticmethod
    def autoplay_online(move1, analysis):
        move_str = str(move1)
        coordinates = analysis_coordinates if analysis else normal_coordinates

        start = coordinates[move_str[:2]]
        end = coordinates[move_str[2:]]
        pyautogui.moveTo(start)
        pyautogui.dragTo(end, duration=0.4, button="left")

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

            if self.board.is_checkmate():
                check_game_end(self.board)

    def update(self):
        current_time = time.time()
        if self.autoplay_bool and current_time - self.last_move_time >= self.move_delay:
            self.autoplay_bot_move()
            self.last_move_time = current_time

    def draw(self):
        screen.fill('black')
        draw_board(self.flipped)
        draw_pieces(self.flipped, self.board)
        for button in self.buttons:
            button.draw(screen)
        pygame.display.flip()

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    button.is_hovered = button.is_over(mouse_pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_to_main.is_over(mouse_pos):
                    self.back_to_main.variable = not self.back_to_main.variable
                    self.running = False
                elif self.reset_button.is_over(mouse_pos):
                    self.board.reset()
                else:
                    self.handle_board_click(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.manual_bot_move()

    def handle_board_click(self, pos):
        px, py = pos
        if px <= 800:
            row, col = get_square_from_pos((px, py), self.flipped)
            square = chess.square(col, row)

            if self.selected_square is None:
                if self.board.piece_at(square):
                    self.selected_square = square
            else:
                move = chess.Move(self.selected_square, square)
                piece = self.board.piece_at(self.selected_square)
                if piece and piece.piece_type == chess.PAWN and chess.square_rank(square) in [0, 7]:
                    move.promotion = chess.QUEEN

                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.autoplay_online(move, self.analysis)
                else:
                    print("Illegal move attempted")

                self.selected_square = None

    def manual_bot_move(self):
        best_move = self.bot.get_best_move(self.board)
        if best_move:
            print(f"Bot chose: {best_move}")
            self.board.push(best_move)
            self.autoplay_online(best_move, self.analysis)

    def autoplay_bot_move(self):
        best_move = self.bot.get_best_move(self.board)
        if best_move:
            print(f"Autoplay move: {best_move}")
            self.board.push(best_move)
            self.autoplay_online(best_move, self.analysis)
