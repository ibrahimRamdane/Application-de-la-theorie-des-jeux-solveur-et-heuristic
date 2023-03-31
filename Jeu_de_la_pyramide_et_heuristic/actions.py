# -*- coding: utf-8 -*-
from abc import ABC, abstractclassmethod
from typing import Sequence, Set, Tuple
from board import Board
from exceptions import *

class Action(ABC):
    """ Represents a possible action for a player"""

    def __init__(self, dest):
        self.dest = dest

    @abstractclassmethod
    def apply(self, player:int, board:Board):
        """Apply the current action, for the given player, on the given board"""
        pass

    @abstractclassmethod
    def unapply(self, player:int, board:Board):
        """Unapply the current action, for the given player, on the given board"""
        pass

    @abstractclassmethod
    def isPossible(self, player:int, board:Board) -> bool:
        """Indicates if the current action is possible, given the player and the board"""
        pass

    @staticmethod
    def _wellFormed(pos) -> bool:
        """Indicates if a position is well formed. A position is a tuple (level, line, column) where each index is 0-based"""
        if not isinstance(pos, tuple): return False
        if len(pos) != 3: return False
        if not (0<=pos[0]<=3): return False
        if pos[0] == 0 and not (0<=pos[1]<=3 and 0<=pos[2]<=3): return False
        if pos[0] == 1 and not (0<=pos[1]<=2 and 0<=pos[2]<=2): return False
        if pos[0] == 2 and not (0<=pos[1]<=1 and 0<=pos[2]<=1): return False
        if pos[0] == 3 and not (pos[1]==0 and pos[2]==0): return False
        return True


    @staticmethod
    def _canBeMoved(board: Board, niv:int, line:int, col:int) -> bool:
        """Indicates if the marble at the given position on the given board can be moved"""
        if 0 <= niv < 3:
            nextlevel = niv+1
            upper = 3-nextlevel
            for i in range(-1,1):
                for j in range(-1,1):
                    if 0<= line+i<=upper and 0<= col+j<=upper and board.getCell(nextlevel, line+i, col+j): return False
            return True
        else:
            return False

    @staticmethod
    def _canBePut(board: Board, niv:int, line:int, col:int) -> bool:
        """Indicates if it is possible to put a marble at the given position on the given board"""
        #the cell must be empty
        if board.getCell(niv, line, col) != 0: return False

        #cannot go to next level if it is not on a square
        if 0 < niv:
            levelbelow = niv-1
            for i in range(2):
                for j in range(2):
                    if board.getCell(levelbelow, line+i, col+j) == 0: return False
        return True

class MoveMarble(Action):
    """Represents an action that consists in moving a marble"""

    def __init__(self, origin, dest):
        super().__init__(dest)
        self.origin = origin
        
    def __str__(self) -> str:
        return "Niv:%s, li:%s, col:%s -> Niv:%s, li:%s, col:%s"%(self.origin[0], self.origin[1], self.origin[2], self.dest[0], self.dest[1], self.dest[2])

    def apply(self, player:int, board:Board):
        board.emptyCell(self.origin[0], self.origin[1], self.origin[2])
        board.setCell(player, self.dest[0], self.dest[1], self.dest[2])

    def unapply(self, player:int, board:Board):
        board.setCell(player, self.origin[0], self.origin[1], self.origin[2])
        board.emptyCell(self.dest[0], self.dest[1], self.dest[2])

    def isPossible(self, player:int, board:Board) -> bool:
        if not self.__check_before_apply: return True
        if not Action._wellFormed(self.dest) or not Action._wellFormed(self.origin): return False
        if not Action._canBePut(board, self.dest[0], self.dest[1], self.dest[2]): return False
        
        # There are some specific rules to check
        # The moved marble must belong to the player (and of course there must be marble)
        if board.getCell(self.origin[0], self.origin[1], self.origin[2]) != player: return False
        # A marble cannot be move if a marble lies on it in the next level
        return Action._canBeMoved(board, self.origin[0], self.origin[1], self.origin[2])

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, MoveMarble):
            return self.dest == __o.dest and self.origin == __o.origin
        else:
            return False

class NewMarble(Action):
    """Represents an action that consists in moving a marble from the reserve"""

    def __init__(self, dest):        
        super().__init__(dest)

    def __str__(self) -> str:
        return "-> Niv:%s, li:%s, col:%s"%(self.dest[0], self.dest[1], self.dest[2])

    def apply(self, player:int, board:Board):
        board.decreaseMarbleCount(player)
        board.setCell(player, self.dest[0], self.dest[1], self.dest[2])

    def unapply(self, player:int, board:Board):
        board.increaseMarbleCount(player)
        board.emptyCell(self.dest[0], self.dest[1], self.dest[2])

    def isPossible(self, player:int, board:Board) -> bool:            
        if not self.__check_before_apply: return True
        if not Action._wellFormed(self.dest): return False
        if not Action._canBePut(board, self.dest[0], self.dest[1], self.dest[2]): return False
        return board.getMarbleCount(player)>0

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, NewMarble):
            return self.dest == __o.dest
        else:
            return False

class MakeSquare(Action):
    def __init__(self, action:Action, seq:Sequence[Tuple[int, int, int]]):
        self.firingAction = action
        self.removeMarbles = seq

    def __str__(self) -> str:
        string = ""
        for s in self.removeMarbles:
            if len(string) >0: string+=", "
            string+= "(Lev: %s, Line:%s, Col:%s)"%(s[0], s[1], s[2])
            
        return "Make a square by %s and remove %s" % (self.firingAction, string)
    
    def apply(self, player:int, board:Board):
        self.firingAction.apply(player, board)
        for s in self.removeMarbles:
            board.emptyCell(s[0], s[1], s[2])
            board.increaseMarbleCount(player)

    def unapply(self, player:int, board:Board):
        for s in self.removeMarbles:
            board.setCell(player, s[0], s[1], s[2])
            board.decreaseMarbleCount(player)
        self.firingAction.unapply(player, board)

    def isPossible(self, player:int, board:Board) -> bool:            
        if not self.__check_before_apply: return True
        if not self.firingAction.isPossible(player, board): return False
        for s in self.removeMarbles:
            if not Action._wellFormed(s): return False
            if not Action._canBeMoved(self.dest[0], self.dest[1], self.dest[2]): return False
        return True

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, MakeSquare):
            if self.firingAction != __o.firingAction: return False
            set = Set(self.removeMarbles)
            set.difference_update(__o.removeMarbles)
            return len(set) == 0
        else:
            return False
