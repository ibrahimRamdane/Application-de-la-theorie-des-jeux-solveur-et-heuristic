# -*- coding: utf-8 -*-
from board import *
from actions import *
from players import *
from aiplayer import AIPlayer, AIPlayer2
from time import time_ns

board = Board()
player1 = AIPlayer2()
player1.name = "player1 (%s)" % (player1.name)
player1.player = -1

player2 = AIPlayer()
#player2 = HumanPlayer("bibi")
player2.name = "player2 (%s)" % (player2.name)
player2.player = 1

current_player = 0
players = [player1, player2]

print(board)
print()

while not board.isTerminal():
    print("current player: %s" % (players[current_player].name))
    start = time_ns()
    action = players[current_player].getNextMove(board)
    print("Temps d'execution: %d ms" % ((time_ns()-start)/1000000.0))
    action.apply(players[current_player].player, board)
    current_player = 1-current_player
    print(board)
    print()

winner = board.getWinner()
if winner == -1:
    print(player1.name+" won")
elif winner == 1:
    print(player2.name+" won")
else:
    print("No winner")
