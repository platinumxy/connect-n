from typing import List, Optional, Tuple, Callable, Dict, Set

Cord = Tuple[int, int]

class Board:
    __DELTAS: Tuple[Cord, ...] = (
        (-1, 1), (0, 1), (1, 1),
        (-1, 0),        (1, 0),
        (-1, -1), (0, -1), (1, -1)
    )
    __grid: Dict[int, Dict[int, Optional[bool]]]
    
    def __init__(self):
        self.__grid = {}
        
    def __in_bounds(self, cord: Cord) -> bool:
        col, row = cord
        return abs(col) >= 0 and abs(row) >= 0

    def play_in_col(self, col: int, colour: bool) -> Optional[bool]:
        if self.__in_bounds((col, 0)) != True: return None
        
        column:Dict[int, Optional[bool]] = self.__grid.get(col, {})
        i = 0 
        while i in column.keys() and column[i] is not None:
            i += 1
        column[i] = colour
        self.__grid[col] = column
        
        return self.__game_won((col, i))

    def __game_won(self, cord:Cord) -> bool:
        assert self.__in_bounds(cord)
        
        init_col, init_row = cord 
        colour = self.__grid[init_col][init_row]  
        assert colour is not None
        
        valid:Callable[[int,int], bool] = lambda col, row: \
            self.__grid.get(col, {}).get(row) == colour if self.__in_bounds((col, row)) else False
        
        for (col_d, row_d) in self.__DELTAS: 
            for i in range(1,4): 
                if not valid(init_col + (col_d * i), init_row + (row_d * i)):
                    break
            else:
                return True
        return False    
    
    def __str__(self) -> str:
        return self.build_grid()

    def build_grid(self) -> str:
        out = ""
        col_vals = {col for col, rows in self.__grid.items() if rows is not None}
        max_row = max((row for column in self.__grid.values() for row in column.keys()), default=-1)

        for r_i in range(max_row, -1, -1):
            for c_i in range(min(col_vals), max(col_vals) + 1):

                if r_i in self.__grid.get(c_i, {}):
                    out += f"{get_colour(self.__grid[c_i][r_i]):^{len(str(max(col_vals, default=0))) + 1}}"
                else:
                    out += ' ' * (len(str(max(col_vals, default=0))) + 1)
            out += '\n'
            
        col_width = len(str(max(col_vals, default=0))) + 1
        out += ''.join([f"{str(c_i + 1):^{col_width}}" for c_i in range(min(col_vals, default=-1), max(col_vals, default=-1) + 1)]) + '\n'

        return out
    
def get_colour(colour: Optional[bool]) -> str:
    if colour is None:
        return ' '
    return 'X' if colour else 'O'

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
        if (ret := board.play_in_col(col, player)) is not None:
            return ret
        print("Invalid move\n")

def print_bar() -> None:
    print("\n" + "-"*20 + "\n")

def start_game() -> None:
    b = Board()
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
