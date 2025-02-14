from typing import Tuple, List, Dict, Callable

FINISHED_MODES: List[Tuple[str, Callable[[], None]]] = [
    ("nan", lambda: None), 
]


def main() -> None:
    game_mode = menu(FINISHED_MODES)   
    game_mode()
    
    
def menu(lookup: List[Tuple[str, Callable[[], None]]]) -> Callable[[], None]:
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