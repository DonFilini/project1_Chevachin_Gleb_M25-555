import math

from labyrinth_game.constants import COMMANDS, ROOMS
from labyrinth_game.player_actions import get_input


def pseudo_random(seed: int, modulo: int) -> int:
    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(frac * modulo)


def trigger_trap(game_state: dict) -> None:
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]

    if inventory:
        idx = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы потеряли предмет: {lost_item}")
        return

    roll = pseudo_random(game_state["steps_taken"], 10)
    if roll < 3:
        print("Ловушка сработала смертельно. Вы погибли.")
        game_state["game_over"] = True
    else:
        print("Вы чудом уцелели, но это было опасно.")


def random_event(game_state: dict) -> None:
    seed = game_state["steps_taken"]

    if pseudo_random(seed, 10) != 0:
        return

    event_type = pseudo_random(seed + 1, 3)
    room = ROOMS[game_state["current_room"]]
    inventory = game_state["player_inventory"]

    if event_type == 0:
        print("Вы замечаете на полу монетку.")
        room["items"].append("coin")

    elif event_type == 1:
        print("Вы слышите шорох где-то в темноте...")
        if "sword" in inventory:
            print("Вы вскидываете меч, и существо отступает.")

    elif event_type == 2:
        if game_state["current_room"] == "trap_room" and "torch" not in inventory:
            print("Что-то не так с полом под вами...")
            trigger_trap(game_state)


def describe_current_room(game_state: dict) -> None:
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room["description"])

    if room["items"]:
        print("Заметные предметы:", ", ".join(room["items"]))

    print("Выходы:", ", ".join(room["exits"].keys()))

    if room["puzzle"]:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state: dict) -> None:
    room = ROOMS[game_state["current_room"]]

    if room["puzzle"] is None:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room["puzzle"]
    print(question)

    user_answer = get_input("Ваш ответ: ")

    alternatives = {
        "10": ["10", "десять"],
        "шаг шаг шаг": ["шаг шаг шаг"],
        "тишина": ["тишина"],
        "резонанс": ["резонанс"],
    }
    valid_answers = alternatives.get(correct_answer, [correct_answer])

    if user_answer in valid_answers:
        print("Верно! Вы решили загадку.")
        room["puzzle"] = None

        if game_state["current_room"] == "library":
            print("В награду вы находите ключ от сокровищницы (treasure_key).")
            game_state["player_inventory"].append("treasure_key")
        elif game_state["current_room"] == "trap_room":
            print("Механизм ловушки отключён.")
        else:
            print("Вы получаете таинственный жетон.")
            game_state["player_inventory"].append("token")
    else:
        print("Неверно. Попробуйте снова.")
        if game_state["current_room"] == "trap_room":
            trigger_trap(game_state)


def attempt_open_treasure(game_state: dict) -> None:
    room = ROOMS["treasure_room"]
    inventory = game_state["player_inventory"]

    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if "treasure_chest" in room["items"]:
            room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    print("Сундук заперт. Можно попробовать ввести код.")
    choice = get_input("Ввести код? (да/нет): ")

    if choice != "да":
        print("Вы отступаете от сундука.")
        return

    question, correct_code = room["puzzle"]
    print(question)
    code = get_input("Введите код: ")

    if code == correct_code:
        print("Код верный! Сундук открывается.")
        if "treasure_chest" in room["items"]:
            room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Неверный код. Сундук остаётся закрытым.")


def show_help(commands: dict = COMMANDS) -> None:
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd.ljust(16)} — {desc}")
