from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Callable

Cord = Tuple[int, int]

class Board:
    __DELTAS: Tuple[Cord, ...] = (
        (-1, 1), (0, 1), (1, 1),
        (-1, 0),        (1, 0),
        (-1, -1), (0, -1), (1, -1)
    )
     
    # access grid[col][row]
    __grid: List[List[Optional[bool]]]
    __h: int
    __w: int
    
    def __init__(self, hight: int, width: int): 
        self.__grid = [[None for _ in range(hight)] for _ in range(width)]
        self.__h = hight
        self.__w = width
        
    def __in_bounds(self, cord: Cord) -> bool: 
        col, row = cord
        return (0 <= col < self.__w) and (0 <= row < self.__h)
    
    """Returns if a token can be placed in a colum, will return None if the cord isnt in bounds"""
    def __can_play_in_col(self, col: int) -> Optional[bool]:
        return (None in self.__grid[col]) if self.__in_bounds((col, 0)) else None
    
    """Attempt to play a move in a colum, will return None if move cannot be made, otherwise will return a bool to indicate if the games been won"""
    def play_in_colum(self, col: int, colour: bool) -> Optional[bool]: 
        if self.__can_play_in_col(col) != False : return None 
    
        self.__grid[col][row_ptr := self.__grid[col].index(None)] = colour
        return self.__game_won((col, row_ptr))
    
    def __game_won(self, cord:Cord) -> bool:
        assert self.__in_bounds(cord)
        
        init_col, init_row = cord 
        colour = self.__grid[init_col][init_row]  
        assert colour is not None
        
        valid = lambda col, row: \
            self.__grid[col][row] == colour if self.__in_bounds((col, row)) else False
        
        for (col_d, row_d) in self.__DELTAS: 
            for i in range(1,5): 
                if not valid(init_col + (col_d * i), init_row + (row_d * i)):
                    break
            else:
                return True
        return False    
                
    def __str__(self) -> str: ...