# labyrinth_game/utils.py

from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input


def describe_current_room(game_state):
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room["description"])

    if room["items"]:
        print("Заметные предметы:", ", ".join(room["items"]))

    exits = ", ".join(room["exits"].keys())
    print("Выходы:", exits)

    if room["puzzle"] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    room = ROOMS[game_state["current_room"]]

    if room["puzzle"] is None:
        print("Загадок здесь нет.")
        return

    question, answer = room["puzzle"]
    print(question)

    user_answer = get_input("Ваш ответ: ")

    if user_answer == answer:
        print("Верно! Вы решили загадку.")
        room["puzzle"] = None  # Убираем загадку

        # Награда — добавим ключ, если это treasure_room
        if game_state["current_room"] == "treasure_room":
            print("Вы слышите щелчок механизма. Кажется, сундук можно открыть.")
        else:
            # универсальная награда
            reward = "mysterious_token"
            print(f"Вы получаете награду: {reward}")
            game_state["player_inventory"].append(reward)

    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    room_name = game_state["current_room"]
    if room_name != "treasure_room":
        print("Здесь нечего открывать.")
        return

    room = ROOMS[room_name]

    # Проверка ключа
    if "treasure_key" in game_state["player_inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if "treasure_chest" in room["items"]:
            room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    # Если ключа нет — можно попробовать код
    print("Сундук заперт. Можно попробовать ввести код.")
    choice = get_input("Ввести код? (да/нет): ")

    if choice != "да":
        print("Вы отступаете от сундука.")
        return

    # Проверяем код
    if room["puzzle"] is None:
        print("Код уже был введён ранее.")
        return

    question, correct_code = room["puzzle"]
    print(question)
    code = get_input("Введите код: ")

    if code == correct_code:
        print("Код верный! Сундук открывается.")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Неверный код. Сундук остаётся закрытым.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
