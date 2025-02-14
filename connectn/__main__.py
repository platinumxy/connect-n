from typing import Tuple, Callable
from connect_four import game as connect_four

FINISHED_MODES: Tuple[Tuple[str, Callable[[], None]]] = (
    ("Connect 4", connect_four.start_game), 
)

def main() -> None:
    game_mode = menu(FINISHED_MODES)   
    game_mode()
    
    
def menu(lookup: Tuple[Tuple[str, Callable[[], None]]]) -> Callable[[], None]:
    print("Choose mode:")
    for i, (name, _) in enumerate(lookup):
        print(f"{i}: {name}")
    
    try: 
        return lookup[int(input("> "))][1]
    except (ValueError, IndexError):
        print("Invalid choice\n")
        return menu(lookup)
    
    
if __name__ == '__main__':
    main()