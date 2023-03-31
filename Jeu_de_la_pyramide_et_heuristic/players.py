# -*- coding: utf-8 -*-
from abc import ABC
from copy import deepcopy
from typing import Sequence, Tuple
from board import Board
from actions import *

class Player(ABC):
    """Abstract class for a player"""

    def __init__(self, name:str):
        self.name = name
        self.player = 0

    @staticmethod
    def __doesPlayerMakeASquare(player:int, board:Board, pos:Tuple[int,int,int]) -> bool:
        """Indicates if the payer has at least one square"""
        size = 4 - pos[0]
        for i in range(-1, 2):
            line = pos[1] + i
            if not 0 <= line < size-1:
                continue
            for j in range(-1, 2):
                col = pos[2] + j
                if not 0 <= col < size-1:
                    continue
                sumcells = board.getCell(pos[0], line, col)+board.getCell(pos[0], line+1, col)+board.getCell(pos[0], line, col+1)+board.getCell(pos[0], line+1, col+1)+player
                if sumcells == player * 4:
                    return True
        return False

    @staticmethod
    def getPossibleMoves(player:int, board: Board) -> Sequence[Action]:
        """Gets the possible moves for the given player and board"""

        if not (player==-1 or player==1): raise Exception("The player must be set to -1 or 1")
        playermarblecount = board.getMarbleCount(player)
        moves_that_give_a_square = []
        
        #we first find all the moves that consist in reusing a marble   
        savemarbleactions = []    
        if playermarblecount<15:
            for lev in range(0,3):
                size = 4 - lev
                count0 = 0
                for i in range(size):
                    for j in range(size):
                        cell = board.getCell(lev, i, j)
                        if cell == 0: count0+=1
                        elif cell == player:
                            if Action._canBeMoved(board, lev, i, j): 
                                board.emptyCell(lev,i,j)
                                #find all the possible destinations
                                for destlev in range(lev+1, 4):
                                    destsize = 4-destlev
                                    for k in range(destsize):
                                        for l in range(destsize):
                                            if Action._canBePut(board, destlev, k, l): 
                                                if Player.__doesPlayerMakeASquare(player, board, (destlev,k,l)):
                                                    moves_that_give_a_square.append(MoveMarble((lev,i,j), (destlev,k,l)))
                                                else:
                                                    savemarbleactions.append(MoveMarble((lev,i,j), (destlev,k,l)))
                                board.setCell(player, lev, i, j)
                if count0 == size*size: break

        # Now we can return the use of a new marble
        newmarbleactions = []
        if playermarblecount>0:
            for lev in range(3, -1, -1):
                size = 4 - lev
                for i in range(size):
                    for j in range(size):
                        if Action._canBePut(board, lev, i, j):
                            if Player.__doesPlayerMakeASquare(player, board, (lev,i,j)):
                                moves_that_give_a_square.append(NewMarble((lev, i, j)))
                            else:
                                newmarbleactions.append(NewMarble((lev, i, j)))

        #now we treat 
        specialactions = []
        boardcopy = deepcopy(board)
        for action in moves_that_give_a_square:
            action.apply(player, boardcopy)
            #find all the candidate marbles
            candidates = []
            for lev in range(2, -1, -1):
                size = 4 - lev
                for i in range(size):
                    for j in range(size):
                        if boardcopy.getCell(lev, i, j) == player and Action._canBeMoved(boardcopy, lev, i, j):
                            candidates.append((lev, i, j))
            for i in range(len(candidates)):
                for j in range(i+1, len(candidates)):
                    specialactions.append(MakeSquare(action, [candidates[i], candidates[j]]))
            for c in candidates:
                specialactions.append(MakeSquare(action, [c]))
            action.unapply(player, boardcopy)

        #return the actions
        return newmarbleactions + savemarbleactions + specialactions  

                

    @abstractclassmethod
    def getNextMove(self, board: Board) -> Action:
        """Gets the next move"""
        pass





class HumanPlayer(Player):
    """Implements a human player"""
    def __init__(self, name:str):
        super().__init__(name)

    def getNextMove(self, board: Board) -> Action:
        print("Possible moves for you:")
        possible = Player.getPossibleMoves(self.player, board)
        digits = len(str(len(possible)-1))
        for i in range(len(possible)):
            print(str(i).rjust(digits) + str(possible[i]))
        print()
        move = -1
        while not 0<=move<len(possible):
            move = int(input("Which move (0-%d)?"%(len(possible)-1)))
        return possible[move]
