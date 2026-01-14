# labyrinth_game/player_actions.py

from labyrinth_game.constants import ROOMS




def move_player(game_state, direction):
    current_room = game_state["current_room"]
    exits = ROOMS[current_room]["exits"]

    if direction in exits:
        new_room = exits[direction]
        game_state["current_room"] = new_room
        game_state["steps_taken"] += 1
        from labyrinth_game.utils import describe_current_room
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    room = ROOMS[game_state["current_room"]]
    items = room["items"]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in items:
        items.remove(item_name)
        game_state["player_inventory"].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")



def use_item(game_state, item_name):
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    # torch
    if item_name == "torch":
        print("Вы подняли факел выше — стало светлее.")

    # sword
    elif item_name == "sword":
        print("Вы крепче сжали меч. Чувствуете уверенность.")

    # bronze_box
    elif item_name == "bronze_box":
        print("Вы открыли бронзовую шкатулку.")
        if "rusty_key" not in inventory:
            print("Внутри лежит ржавый ключ. Вы кладёте его в инвентарь.")
            inventory.append("rusty_key")
        else:
            print("Но внутри пусто.")

    else:
        print("Вы не знаете, как использовать этот предмет.")


def show_inventory(game_state):
    inventory = game_state["player_inventory"]

    if not inventory:
        print("Ваш инвентарь пуст.")
    else:
        print("Инвентарь:", ", ".join(inventory))


def get_input(prompt="> "):
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
