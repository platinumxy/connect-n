from typing import Iterable, List, Optional, Tuple, Callable

Cord2D = Tuple[int, int]
Cord3D = Tuple[int, int, int]

def get_colour(colour: bool) -> str:
    return "X" if colour else "O"

class Board: 
    __DELTAS: Tuple[Cord3D, ...] = (
        (-1, 1, -1),  (0, 1, -1),  (1, 1, -1),
        (-1, 0, -1),  (0, 0, -1),   (1, 0, -1),
        (-1, -1, -1), (0, -1, -1), (1, -1, -1),
        
        (-1, 1, 0),   (0, 1, 0),   (1, 1, 0),
        (-1, 0, 0),                (1, 0, 0),
        (-1, -1, 0),  (0, -1, 0),  (1, -1, 0),

        (-1, 1, 1),   (0, 1, 1),   (1, 1, 1),
        (-1, 0, 1),   (0, 0, 1),   (1, 0, 1),
        (-1, -1, 1),  (0, -1, 1),  (1, -1, 1)
    )

    # access grid[x][y][z]
    __GRID: List[List[List[Optional[bool]]]]
    __X: int
    __Y: int
    __Z: int

    def __init__(self, x: int = 5, y: int = 5 , z: int = 5):
        self.__GRID = [[[None for _ in range(z)] for _ in range(y)] for _ in range(x)]
        self.__X = x
        self.__Y = y
        self.__Z = z

    def __Y_iter(self) -> Iterable[int]:
        for y in range(self.__Y):
            yield y
    def __X_iter(self) -> Iterable[int]:
        for x in range(self.__X - 1, -1, -1):
            yield x
    def __Z_iter(self) -> Iterable[int]:
        for z in range(self.__Z - 1, -1, -1):
            yield z


    def __in_bounds(self, cord: Cord3D) -> bool:
        x, y, z = cord
        return (0 <= x < self.__X) and (0 <= y < self.__Y) and (0 <= z < self.__Z)
    
    def __can_place(self, cord: Cord2D) -> Optional[bool]:
        x, y = cord
        return (None in self.__GRID[x][y]) if self.__in_bounds((x, y, 0)) else None
    
    def __game_won(self, cord: Cord3D) -> bool:
        assert self.__in_bounds(cord)
        
        x, y, z = cord
        colour = self.__GRID[x][y][z]
        assert colour is not None
        
        valid: Callable[[int, int, int], bool] = lambda x, y, z: \
            self.__GRID[x][y][z] == colour if self.__in_bounds((x, y, z)) else False
        
        for (x_d, y_d, z_d) in self.__DELTAS:
            for i in range(1, 4):
                if not valid(x + (x_d * i), y + (y_d * i), z + (z_d * i)):
                    break
            else:
                return True
        return False

    def play_move(self, cord: Cord2D, colour: bool) -> Optional[bool]:
        if self.__can_place(cord) != True: 
            return None

        x, y = cord
        z_ptr = self.__GRID[x][y].index(None)
        self.__GRID[x][y][z_ptr] = colour
        return self.__game_won((x, y, z_ptr))
    
    def get_layer(self, cord: Tuple[Optional[int],Optional[int],Optional[int]]) -> List[List[Optional[bool]]]:
        assert self.__in_bounds(tuple(0 if c is None else c for c in cord))# type: ignore
        assert cord.count(None) == 2
        x, y, z = cord
        
        if x is not None:
            return [[self.__GRID[x][y][z] for y in self.__Y_iter()] for x in self.__X_iter()] # type: ignore
        elif y is not None:
            return [[self.__GRID[x][y][z] for z in self.__Z_iter()] for x in self.__X_iter()]
        elif z is not None:
            return [[self.__GRID[x][y][z] for y in self.__Y_iter()] for x in self.__X_iter()]

        raise ValueError("Invalid state")
        
    def show_layer(self, cord: Tuple[Optional[int],Optional[int],Optional[int]]) -> None:
        assert self.__in_bounds(tuple(0 if c is None else c for c in cord)) # type: ignore
        assert cord.count(None) == 2

        for row in self.get_layer(cord):
            print(" ".join(get_colour(v) if v is not None else '.' for v in row))
        
    def show_cube(self) -> None:
        print("-"*20)
        for z in self.__Z_iter():
            self.show_layer((None,None, z))
            print("- "*10)

 
def start_game() -> None:
    try:
        b = Board(5, 5, 5)
        while True:
            b.show_cube()
            print(f"{get_colour(True)} move")
            while True:
                try: 
                    col = int(input("Col: ")) - 1
                    row = int(input("Row: ")) - 1
                    if (ret := b.play_move((col, row), True)) is not None:
                        break
                    print("Invalid move\n")
                except ValueError:
                    print("Invalid input\n")
            if ret:
                print(f"{get_colour(True)} wins!")
                break
            b.show_cube()
            print(f"{get_colour(False)} move")
            while True:
                try:
                    col = int(input("Col: ")) - 1
                    row = int(input("Row: ")) - 1
                    if (ret := b.play_move((col, row), False)) is not None:
                        break
                    print("Invalid move\n")
                except ValueError:
                    print("Invalid input\n")
            if ret:
                print(f"{get_colour(False)} wins!")
                break
    except Exception as e:
        print(f"An error occurred: {e}")