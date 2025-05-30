from GameStates import *
from functions import *
from preloading import *
import sys

def main():
    board = chess.Board()
    pygame.init()
    game = PreScreen(board)
    game.run()
    if not game.quit:
        sys.exit()
    values = game.get_values()
    custom_board_bool = values['custom_board']
    autoplay_bool = values['autoplay']
    player_color = values['player_color']
    autoplay_online_bool = values['autoplay_online']
    bot_vs_bot = values['bot_vs_bot']
    analysis = values['analysis']

    if custom_board_bool:
        custom_board = CustomBoard(chess.Board(None), player_color, autoplay_bool, autoplay_online_bool)
        custom_board.run()
        board = custom_board.get_board()
        custom_board_bool = False
        if custom_board.back_to_main.variable:
            main()

    if not autoplay_online_bool and not custom_board_bool and not bot_vs_bot:
        normal_game = NormalGame(board, chess_bot, player_color, autoplay_bool, autoplay_online_bool, player_color)
        print(board)
        normal_game.run()
        if normal_game.back_to_main.variable:
            main()

    if autoplay_online_bool and not custom_board_bool and not bot_vs_bot:
        autoplay_online_game = AutoplayOnlineGame(board, chess_bot, autoplay_bool, analysis, player_color)
        autoplay_online_game.run()
        if autoplay_online_game.back_to_main.variable:
            main()

    if bot_vs_bot:
        bot_vs_bot_game = BotVsBot(board, chess_bot, autoplay_online_bool, analysis, player_color)
        bot_vs_bot_game.run()
        if bot_vs_bot_game.back_to_main.variable:
            main()

main()

pygame.quit()