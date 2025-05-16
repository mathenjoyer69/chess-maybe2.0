from GameStates import *
from functions import *
import config

def main():
    pygame.init()
    board = chess.Board() if not custom_board_bool else chess.Board(None)

    if config.custom_board_bool:
        custom_board = CustomBoard(board, player_color, autoplay_bool, autoplay_online_bool)
        custom_board.run()

    if not autoplay_online_bool and not config.custom_board_bool and not bot_vs_bot:
        normal_game = NormalGame(board, chess_bot, player_color, autoplay_bool, autoplay_online_bool, player_color)
        normal_game.run()

    if autoplay_online_bool and not config.custom_board_bool and not bot_vs_bot:
        autoplay_online_game = AutoplayOnlineGame(board, chess_bot, autoplay_bool, analysis, player_color)
        autoplay_online_game.run()

    if bot_vs_bot:
        bot_vs_bot_game = BotVsBot(board, chess_bot, autoplay_online_bool, analysis, player_color)
        bot_vs_bot_game.run()

if config.start:
    main()

pygame.quit()