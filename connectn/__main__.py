from typing import Tuple, Callable
from connect_four import game as connect_four
from connect_four_inf import game as connect_four_inf
from connect_four_3d import game as connect_four_3d
from connect_n import game as connect_n

FINISHED_MODES: Tuple[Tuple[str, Callable[[], None]], ...] = (
    ("Connect 4", connect_four.start_game), 
    ("Connect 4 infinite", connect_four_inf.start_game),
    ("Connect N", connect_n.start_game),
    ("Connect 4 3D", connect_four_3d.start_game)
)

def main() -> None:
    game_mode = menu(FINISHED_MODES)   
    game_mode()
    
    
def menu(lookup: Tuple[Tuple[str, Callable[[], None]], ...]) -> Callable[[], None]:
    print("Choose mode:")
    for i, (name, _) in enumerate(lookup):
        print(f"{i + 1}: {name}")
    
    try: 
        return lookup[int(input("> ")) - 1 ][1]
    except (ValueError, IndexError):
        print("Invalid choice\n")
        return menu(lookup)
    
    
if __name__ == '__main__':
    main()