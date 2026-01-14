# labyrinth_game/player_actions.py

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def move_player(game_state: dict, direction: str) -> None:
    current_room = game_state["current_room"]
    exits = ROOMS[current_room]["exits"]

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = exits[direction]

    if next_room == "treasure_room":
        if "rusty_key" in game_state["player_inventory"]:
            print(
                "Вы используете найденный ключ, чтобы открыть путь "
                "в комнату сокровищ."
            )
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return

    game_state["current_room"] = next_room
    game_state["steps_taken"] += 1

    describe_current_room(game_state)
    random_event(game_state)


def take_item(game_state: dict, item_name: str) -> None:
    room = ROOMS[game_state["current_room"]]
    items = room["items"]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжёлый.")
        return

    if item_name in items:
        items.remove(item_name)
        game_state["player_inventory"].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state: dict, item_name: str) -> None:
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Вы поднимаете факел — стало светлее.")
    elif item_name == "sword":
        print("Вы крепче сжимаете меч и чувствуете уверенность.")
    elif item_name == "bronze_box":
        print("Вы открываете бронзовую шкатулку.")
        if "rusty_key" not in inventory:
            print("Внутри ржавый ключ. Вы кладёте его в инвентарь.")
            inventory.append("rusty_key")
        else:
            print("Но внутри пусто.")
    else:
        print("Вы не знаете, как использовать этот предмет.")


def show_inventory(game_state: dict) -> None:
    inventory = game_state["player_inventory"]
    if not inventory:
        print("Ваш инвентарь пуст.")
    else:
        print("Инвентарь:", ", ".join(inventory))


def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
