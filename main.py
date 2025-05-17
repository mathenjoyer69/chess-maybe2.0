from GameStates import *
from functions import *
from preloading import *

def main():
    pygame.init()

    g = PreScreen()
    g.run()
    values = g.get_values()
    custom_board_bool = values['custom_board']
    autoplay_bool = values['autoplay']
    player_color = values['player_color']
    autoplay_online_bool = values['autoplay_online']
    bot_vs_bot = values['bot_vs_bot']
    analysis = values['analysis']
    print(custom_board_bool)
    board = chess.Board() if not custom_board_bool else chess.Board(None)
    if custom_board_bool:
        custom_board = CustomBoard(board, player_color, autoplay_bool, autoplay_online_bool)
        custom_board.run()

    if not autoplay_online_bool and not custom_board_bool and not bot_vs_bot:
        normal_game = NormalGame(board, chess_bot, player_color, autoplay_bool, autoplay_online_bool, player_color)
        normal_game.run()

    if autoplay_online_bool and not custom_board_bool and not bot_vs_bot:
        autoplay_online_game = AutoplayOnlineGame(board, chess_bot, autoplay_bool, analysis, player_color)
        autoplay_online_game.run()

    if bot_vs_bot:
        bot_vs_bot_game = BotVsBot(board, chess_bot, autoplay_online_bool, analysis, player_color)
        bot_vs_bot_game.run()

main()

pygame.quit()
