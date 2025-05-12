from typing import List, Optional, Tuple, Callable

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
        if self.__can_play_in_col(col) != True : return None 
    
        self.__grid[col][row_ptr := self.__grid[col].index(None)] = colour
        return self.__game_won((col, row_ptr))
    
    def __game_won(self, cord:Cord) -> bool:
        assert self.__in_bounds(cord)
        
        init_col, init_row = cord 
        colour = self.__grid[init_col][init_row]  
        assert colour is not None
        
        valid:Callable[[int,int], bool] = lambda col, row: \
            self.__grid[col][row] == colour if self.__in_bounds((col, row)) else False
        
        for (col_d, row_d) in self.__DELTAS: 
            for i in range(1,4): 
                if not valid(init_col + (col_d * i), init_row + (row_d * i)):
                    break
            else:
                return True
        return False    
                
    def __str__(self) -> str:
        out = ""
        for row in range(self.__h - 1, -1, -1):
            for col in range(self.__w):
                out += f"{get_colour(v) if (v := self.__grid[col][row]) is not None else '.'} "
            out += "\n"
        return out

def get_colour(colour: bool) -> str: return "X" if colour else "O"

def print_bar() -> None:
    print("\n" + "-"*20 + "\n")

def get_col() -> int:
   try:
       return int(input("Col: ")) - 1
   except ValueError:
        print("Invalid input\n")
        return get_col()

def play_move(board: Board, player: bool) -> bool:
    print(f"{get_colour(player)} move")
    while True:
        col = get_col()
        if (ret := board.play_in_colum(col, player)) is not None:
            return ret
        print("Invalid move\n")


def start_game() -> None:
    b = Board(6,7)
    while True: 
        print(b)
        if play_move(b, True): 
            print(f"{get_colour(True)} wins!")
            break
        print_bar()
        print(b)

        if play_move(b, False): 
            print(b)
            print(f"{get_colour(False)} wins!")
            break
        print_bar()
        