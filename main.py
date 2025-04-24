from time import sleep
import pygame
import chess
import pyautogui
import GameStates
import bot
import config
import MainScreen

chess_bot = bot.Bot()
main_screen = MainScreen.MainScreen()
player_color = main_screen.settings['player_color']
bot_vs_bot = main_screen.settings['bot_vs_bot']
custom_board_bool = main_screen.settings['custom_board_bool']
autoplay_bool = main_screen.settings['autoplay_bool']
analysis = main_screen.settings['analysis']
autoplay_online_bool = main_screen.settings['autoplay_online_bool']

pygame.init()

for piece, filename in config.PIECES.items():
    config.PIECE_IMAGES[piece] = pygame.image.load(f'assets/{filename}')
    config.PIECE_IMAGES[piece] = pygame.transform.scale(config.PIECE_IMAGES[piece], (config.SQUARE_SIZE, config.SQUARE_SIZE))

board = chess.Board() if not custom_board_bool else chess.Board(None)

def draw_board(flipped):
    for row in range(config.ROWS):
        for col in range(config.COLS):
            color = config.LIGHT_BROWN if (row + col) % 2 == 0 else config.DARK_BROWN
            actual_row = 7 - row if flipped else row
            actual_col = 7 - col if flipped else col
            pygame.draw.rect(config.screen, color,(actual_col * config.SQUARE_SIZE, actual_row * config.SQUARE_SIZE, config.SQUARE_SIZE, config.SQUARE_SIZE))


def draw_pieces(flipped):
    for row in range(config.ROWS):
        for col in range(config.COLS):
            actual_row = 7 - row if flipped else row
            actual_col = 7 - col if not flipped else col

            square = chess.square(actual_col, actual_row)
            piece = board.piece_at(square)
            if piece:
                piece_symbol = piece.symbol()
                config.screen.blit(config.PIECE_IMAGES[piece_symbol], (col * config.SQUARE_SIZE, row * config.SQUARE_SIZE))


def get_square_from_pos(pos, flipped):
    x, y = pos
    row, col = y // config.SQUARE_SIZE, x // config.SQUARE_SIZE
    actual_row = 7 - row if flipped else row
    actual_col = 7 - col if not flipped else col
    return actual_row, actual_col

def autoplay_online(move1,analysis):
    move_str = str(move1)
    if analysis:
        coordinates = config.analysis_coordinates
    else:
        coordinates = config.normal_coordinates

    first_mouse = move_str[:2]
    last_mouse = move_str[2:]
    first_m_coordinates = coordinates[first_mouse]
    last_m_coordinates = coordinates[last_mouse]
    print(first_m_coordinates,last_m_coordinates)
    pyautogui.moveTo(first_m_coordinates)
    sleep(0.5)
    pyautogui.dragTo(last_m_coordinates,button="left")

def uci_to_pgn(uci_moves):
    pgn_moves = []
    for i, move in enumerate(uci_moves, start=1):
        if i % 2 == 1:
            pgn_moves.append(f"{(i + 1) // 2}: {move.uci()}")
        else:
            pgn_moves[-1] += f" {move.uci()}"
    return " ".join(pgn_moves)

running = True
selected_square = None
flipped = player_color

counter = 0
moves_played = []
if custom_board_bool:
    custom_board = GameStates.CustomBoard(board, flipped)
    custom_board.run()

moves1 = []
if running and not autoplay_online_bool and not custom_board_bool and not bot_vs_bot:
    GameStates.NormalGame(board, bot.Bot(), flipped, autoplay_bool, autoplay_online_bool, player_color)

while running and autoplay_online_bool and not custom_board_bool and not bot_vs_bot:
    if moves_played:
        for i in moves_played:
            autoplay_online(i,analysis)
            sleep(1)
    draw_board(flipped)
    draw_pieces(flipped)
    pygame.display.flip()

    if not board.legal_moves:
        running = False
        if not board.is_check():
            print("draw")
            break
        if counter % 2 == 0:
            print("white won")
        else:
            print("black won")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square_from_pos(pygame.mouse.get_pos(), flipped)
            square = chess.square(col, row)
            if selected_square is None:
                if board.piece_at(square):
                    selected_square = square
            else:
                if board.piece_at(selected_square) and board.piece_at(selected_square).piece_type == chess.PAWN:
                    if chess.square_rank(square) == 7 or chess.square_rank(square) == 0:
                        move = chess.Move(selected_square, square, promotion=chess.QUEEN)
                    else:
                        move = chess.Move(selected_square, square)
                else:
                    move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)
                    counter += 1
                else:
                    print("illegal move")
                selected_square = None
            print(f"you clicked {board.piece_at(square)}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if counter % 2 != 0:
                    best_move = chess_bot.get_best_move(board)
                    print(f"ai chose: {best_move}")
                    board.push(best_move)
                    sleep(1)
                    autoplay_online(best_move,analysis)
                    counter += 1
                else:
                    print("its white's turn")
                    best_move = chess_bot.get_best_move(board)
                    board.push(best_move)
                    sleep(1)
                    autoplay_online(best_move, analysis)

        if autoplay_bool:
            if counter % 2 != 0:
                counter += 1
                best_move = chess_bot.get_best_move(board)
                print(best_move)
                sleep(1)
                board.push(best_move)
                sleep(1)
                autoplay_online(best_move,analysis)

play = True
moves = []
bot_counter = 0
if autoplay_online_bool:
    sleep(3)
while running and bot_vs_bot:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_board(flipped)
    draw_pieces(flipped)
    pygame.display.flip()
    keys = pygame.key.get_pressed()
    if board.is_checkmate():
        if counter % 2 == 0:
            print("black won")
        else:
            print("white won")
        break

    if keys[pygame.K_SPACE]:
        play = not play
        print("game state: ", play)

    if play:
        best_move = chess_bot.get_best_move(board)
        move_str = str(best_move)
        move_1,move_2 = move_str[:2],move_str[2:4]
        move_1_n,move_2_n = config.square_to_number[move_1],config.square_to_number[move_2]
        moves.append(best_move)
        if not autoplay_bool:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        board.push(best_move)
        else:
            board.push(best_move)
        sleep(0.05)
        moves_played.append(best_move)
        if autoplay_online_bool:
            autoplay_online(best_move,analysis)

print(uci_to_pgn(moves))
pygame.quit()