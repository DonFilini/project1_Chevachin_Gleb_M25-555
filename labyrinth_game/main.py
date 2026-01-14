from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state: dict, command: str) -> None:
    parts = command.split()
    if not parts:
        print("Введите команду.")
        return

    action = parts[0]
    arg = parts[1] if len(parts) > 1 else None

    if action in ("north", "south", "east", "west"):
        move_player(game_state, action)
        return

    match action:
        case "look":
            describe_current_room(game_state)

        case "inventory":
            show_inventory(game_state)

        case "go":
            if arg:
                move_player(game_state, arg)
            else:
                print("Укажите направление (например: go north).")

        case "take":
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет (например: take torch).")

        case "use":
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет (например: use torch).")

        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)

        case "help":
            show_help()

        case "quit" | "exit":
            print("Вы покидаете лабиринт...")
            game_state["game_over"] = True

        case _:
            print("Неизвестная команда. Введите help для списка команд.")


def main() -> None:
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input("> ")
        process_command(game_state, command)


if __name__ == "__main__":
    main()
