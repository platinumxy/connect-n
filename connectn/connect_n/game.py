from typing import Callable
from connect_four.game import Board as ConnectFourBoard
from connect_four.game import play_move, print_bar, get_colour

Cord = tuple[int, int]


class Board(ConnectFourBoard):
    __connect_n: int 
    def __init__(self, hight: int, width: int, connect_n: int):
        super().__init__(hight, width)
        self.__connect_n = connect_n

    def __game_won(self, cord: Cord) -> bool:
        assert self.__in_bounds(cord)
        
        init_col, init_row = cord 
        colour = self.__grid[init_col][init_row]  
        assert colour is not None
        
        valid:Callable[[int,int], bool] = lambda col, row: \
            self.__grid[col][row] == colour if self.__in_bounds((col, row)) else False
        
        for (col_d, row_d) in self.__DELTAS: 
            for i in range(1, self.__connect_n): 
                if not valid(init_col + (col_d * i), init_row + (row_d * i)):
                    break
            else:
                return True
        return False    

def start_game() -> None:
    b = Board(6,7, 5)
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
        