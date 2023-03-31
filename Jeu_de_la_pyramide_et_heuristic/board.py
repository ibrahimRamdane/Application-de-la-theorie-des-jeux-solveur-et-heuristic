# -*- coding: utf-8 -*-
from typing import Sequence
from exceptions import *
from copy import deepcopy

class Board:
    """Class that represents a board"""
    
    def __init__(self):
        self.__cells = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0], [0, 0]], [[0]]]
        self.__blackCount = 15
        self.__whiteCount = 15

    @property
    def blackMarbles(self):
        """Gets the number of black marbles"""
        return self.__blackCount

    @property
    def whiteMarbles(self):
        """Gets the number of white marbles"""
        return self.__whiteCount

    @property
    def cells(self):
        """Gets all the cells as a 3D matrix"""
        return deepcopy(self.__cells)

    def getMarbleCount(self, player:int) -> int:
        """Gets the marble count for the given player"""
        if player==-1: return self.blackMarbles
        elif player==1: return self.whiteMarbles
        else: raise Exception("Player must be -1 for black and 1 for white")

    def decreaseMarbleCount(self, player:int):
        """Decreases the marble count of the given player"""
        if player == -1:
            self.__blackCount-=1
        elif player == 1:
            self.__whiteCount-=1

    def increaseMarbleCount(self, player:int):
        """Increases the marble count of the given player"""
        if player == -1:
            self.__blackCount+=1
        elif player == 1:
            self.__whiteCount+=1


    def __cell_to_char(self, level:int, line:int, col:int) -> str:
        """Pretty print a cell"""
        cell = self.__cells[level][line][col]
        if (cell == 1): return 'W'
        elif (cell ==-1): return 'B'
        else: return '.'

    def getCell(self, niv:int, line:int, col:int) -> int:
        """Gets the value of the desired cell"""
        return self.__cells[niv][line][col]

    def emptyCell(self, niv:int, line:int, col:int):
        """Empties the given cell"""
        self.__cells[niv][line][col] = 0

    def setCell(self, player:int, niv:int, line:int, col:int):
        """Sets the given cell"""
        if player==-1 or player==1:
            self.__cells[niv][line][col] = player
        else:
            raise ForbiddenActionException

    def __str__(self) -> str:
        s = ""
        #line 1/7
        for i in range(4):
            s+= "%s " % (self.__cell_to_char(0, 0, i))
        s+='\n'

        #line 2/7
        s+= " "*10
        for i in range(3):
            s+= "%s " % (self.__cell_to_char(1, 0, i))
        s+='\n'

        #line 3/7
        for i in range(4):
            s+= "%s " % (self.__cell_to_char(0, 1, i))
        s+= " "*11
        for i in range(2):
            s+= "%s " % (self.__cell_to_char(2, 0, i))
        s+='\n'

        #line 4/7
        s+= " "*10
        for i in range(3):
            s+= "%s " % (self.__cell_to_char(1, 1, i))
        s+= " "*(3+6)
        s+= self.__cell_to_char(3, 0, 0)
        s+='\n'

        #line 5/7
        for i in range(4):
            s+= "%s " % (self.__cell_to_char(0, 2, i))
        s+= " "*11
        for i in range(2):
            s+= "%s " % (self.__cell_to_char(2, 1, i))
        s+='\n'

        #line 6/7
        s+= " "*10
        for i in range(3):
            s+= "%s " % (self.__cell_to_char(1, 2, i))
        s+='\n'

        #line 7/7
        for i in range(4):
            s+= "%s " % (self.__cell_to_char(0, 3, i))
        s+='\n'
        s+='\n'
        s+="remaining W:%s\tremaining B:%s"%(self.whiteMarbles, self.blackMarbles)
        return s

    def getTop(self):
        """Gets the top of the pyramid"""
        return self.getCell(3,0,0)

    def isTerminal(self) -> bool:
        """Indicates if the board is terminal (end of party)"""
        return self.getTop() !=0 or self.whiteMarbles == 0 or self.blackMarbles == 0

    def getWinner(self):
        """Gets the winner or None if it is not terminal"""
        if self.isTerminal():
            if self.getTop() != 0: return self.getTop()
            elif self.whiteMarbles == 0: return -1
            elif self.blackMarbles == 0: return 1
        return None

    
        
            
