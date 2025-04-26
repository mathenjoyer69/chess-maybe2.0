import pygame
import chess
import GameStates
import bot
import MainScreen

chess_bot = bot.Bot()
pygame.init()
main_screen = MainScreen.MainScreen()
player_color = main_screen.settings['player_color']
bot_vs_bot = main_screen.settings['bot_vs_bot']
custom_board_bool = main_screen.settings['custom_board_bool']
autoplay_bool = main_screen.settings['autoplay_bool']
analysis = main_screen.settings['analysis']
autoplay_online_bool = main_screen.settings['autoplay_online_bool']

board = chess.Board() if not custom_board_bool else chess.Board(None)

if custom_board_bool:
    custom_board = GameStates.CustomBoard(board, player_color)
    custom_board.run()

if not autoplay_online_bool and not custom_board_bool and not bot_vs_bot:
    normal_game = GameStates.NormalGame(board, chess_bot, player_color, autoplay_bool, autoplay_online_bool, player_color)
    normal_game.run()

if autoplay_online_bool and not custom_board_bool and not bot_vs_bot:
    autoplay_online_game = GameStates.AutoplayOnlineGame(board, chess_bot, autoplay_bool, analysis, player_color)
    autoplay_online_game.run()

if bot_vs_bot:
    bot_vs_bot_game = GameStates.BotVsBot(board, chess_bot, autoplay_online_bool, analysis, player_color)
    bot_vs_bot_game.run()

pygame.quit()