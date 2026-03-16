from model import Player


def print_header(text):
    """Печать заголовка."""
    print("\n" + "=" * 70)
    print(f" {text} ".center(70, "="))
    print("=" * 70)


def print_subheader(text):
    """Печать подзаголовка."""
    print(f"\n--- {text} ---")


def print_success(text):
    """Печать успешного сообщения."""
    print(f"  ✓ {text}")


def print_error(text):
    """Печать сообщения об ошибке."""
    print(f"  ✗ {text}")


def print_info(text):
    """Печать информационного сообщения."""
    print(f"  → {text}")


def scenario_1_creation_and_validation():
    """Сценарий 1: Создание игроков и проверка валидации."""
    print_header("СЦЕНАРИЙ 1: СОЗДАНИЕ ИГРОКОВ И ВАЛИДАЦИЯ")
    
    # Успешное создание
    print_subheader("Успешное создание")
    player1 = Player("Стив", level=5, health=80.5, experience=4500)
    print(player1)
    print(f"\nRepr для разработчика: {repr(player1)}")
    
    # Создание с параметрами по умолчанию
    print_subheader("Создание с параметрами по умолчанию")
    player2 = Player("Сашка")
    print(player2)
    
    # Демонстрация валидации (некорректное создание)
    print_subheader("Ошибки валидации")
    
    test_cases = [
        ("Пустое имя", lambda: Player("")),
        ("Имя слишком длинное (21 символ)", lambda: Player("А" * 21)),
        ("Уровень 0 (меньше минимального)", lambda: Player("Тест", level=0)),
        ("Уровень 15 (больше максимального)", lambda: Player("Тест", level=15)),
        ("Здоровье -10", lambda: Player("Тест", health=-10)),
        ("Здоровье 150", lambda: Player("Тест", health=150)),
        ("Опыт 6000 для уровня 5 (максимум 5000)", lambda: Player("Тест", level=5, experience=6000)),
    ]
    
    for description, test_func in test_cases:
        try:
            print(f"\n  Тест: {description}")
            test_func()
        except (TypeError, ValueError) as e:
            print_error(f"{e}")
    
    return player1, player2


def scenario_2_state_and_behavior(player):
    """Сценарий 2: Демонстрация состояний и поведения."""
    print_header(f"СЦЕНАРИЙ 2: СОСТОЯНИЯ И ПОВЕДЕНИЕ (игрок {player.name})")
    
    print_subheader("Начальное состояние")
    print(player)
    
    # Демонстрация получения урона
    print_subheader("Получение урона")
    result = player.take_damage(30.0)
    print_info(result)
    print_info(f"Жив: {player.is_alive}")
    
    # Демонстрация лечения
    print_subheader("Лечение")
    result = player.heal(20.0)
    print_info(result)
    
    # Демонстрация добавления опыта
    print_subheader("Добавление опыта")
    result = player.add_experience(800)
    print_info(result)
    
    # Прямое изменение через setter
    print_subheader("Прямое изменение здоровья через setter")
    try:
        player.health = 90.0
        print_success(f"Здоровье изменено на {player.health}")
        print_info(f"Жив: {player.is_alive}")
    except ValueError as e:
        print_error(f"{e}")
    
    # Попытка некорректного изменения
    print_subheader("Попытка некорректного изменения здоровья")
    try:
        player.health = -50.0
    except ValueError as e:
        print_error(f"{e}")
    
    print_subheader("Итоговое состояние")
    print(player)


def scenario_3_level_up_and_death():
    """Сценарий 3: Повышение уровня и смерть игрока."""
    print_header("СЦЕНАРИЙ 3: ПОВЫШЕНИЕ УРОВНЯ И СМЕРТЬ")
    
    # Создаем игрока, близкого к повышению уровня
    player = Player("Скалли_Милана", level=2, experience=1800, health=50.0)
    print_subheader("Начальное состояние (близок к повышению уровня)")
    print(player)
    
    # Добавляем опыт для повышения уровня
    print_subheader("Добавление опыта для повышения уровня")
    result = player.add_experience(300)  # Должен стать 3 уровень
    print_info(result)
    
    print_subheader("После повышения уровня")
    print(player)  # Здоровье должно восстановиться до 100
    
    # Смерть игрока
    print_subheader("Смерть игрока")
    result = player.take_damage(150.0)  # Больше чем здоровье
    print_info(result)
    print_info(f"Жив: {player.is_alive}")
    
    # Попытка действия мертвого игрока
    print_subheader("Попытка действий мертвого игрока")
    result = player.heal(50.0)
    print_info(result)
    
    result = player.add_experience(100)
    print_info(result)
    
    # Воскрешение
    print_subheader("Воскрешение игрока")
    result = player.revive()
    print_info(result)
    
    print_subheader("После воскрешения")
    print(player)


def scenario_4_magic_methods():
    """Сценарий 4: Демонстрация магических методов."""
    print_header("СЦЕНАРИЙ 4: МАГИЧЕСКИЕ МЕТОДЫ")
    
    players = [
        Player("Сашка", level=8, health=95.0, experience=7500),
        Player("КайАнжела", level=5, health=45.5, experience=4800),
        Player("Иен", level=6, health=100.0, experience=5900),
        Player("КимЧенЫн", level=10, health=30.0, experience=9000),
        Player("Артем", level=3, health=80.0, experience=2500),  
    ]
    
    print_subheader("Список игроков (__repr__)")
    for i, p in enumerate(players, 1):
        print(f"  {i}. {repr(p)}")
    
    # Демонстрация __str__
    print_subheader("Строковое представление (__str__)")
    print(players[2])  # КайАнжела
    
    # Демонстрация __eq__
    print_subheader("Сравнение игроков (__eq__ по имени)")
    print_info(f"players[0] (Сашка) == players[4] (КимЧенЫн): {players[0] == players[4]}")
    print_info(f"players[1] (КайАнжела) == players[2] (Иен): {players[1] == players[2]}")
    
    # Демонстрация __lt__ для сортировки
    print_subheader("Сортировка по уровню (__lt__)")
    sorted_players = sorted(players)
    for p in sorted_players:
        print(f"  Ур. {p.level:2d} | {p.name:8} | {p.title}")
    
    # Доступ к атрибутам класса
    print_subheader("Атрибуты класса")
    print_info(f"MAX_LEVEL (макс. уровень): {Player.MAX_LEVEL}")
    print_info(f"MIN_LEVEL (мин. уровень): {Player.MIN_LEVEL}")
    print_info(f"EXPERIENCE_PER_LEVEL (опыта для уровня): {Player.EXPERIENCE_PER_LEVEL}")
    print_info(f"TITLES (титулы): {Player.TITLES}")
    
    # Доступ через экземпляр
    print_subheader("Доступ через экземпляр")
    print_info(f"player.MAX_LEVEL: {players[0].MAX_LEVEL}")


def main():
    """Главная функция демонстрации."""
    print_header("ЛАБОРАТОРНАЯ РАБОТА №1: КЛАСС PLAYER")
    print("Реализация на оценку 5")
    
    # Сценарий 1
    player1, player2 = scenario_1_creation_and_validation()
    
    # Сценарий 2
    scenario_2_state_and_behavior(player1)
    
    # Сценарий 3
    scenario_3_level_up_and_death()
    
    # Сценарий 4
    scenario_4_magic_methods()
    
    print_header("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")


if __name__ == "__main__":
    main()