# demo.py

import sys
import os

# Добавляем путь к папке lab01
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))

from model import Player
from validate import validate_string, validate_int, validate_float, validate_experience
from collection import PlayerList

def print_header(text):
    """Печать заголовка."""
    print("\n" + "=" * 80)
    print(f" {text} ".center(80, "="))
    print("=" * 80)


def print_subheader(text):
    """Печать подзаголовка."""
    print(f"\n--- {text} ---")


def print_success(text):
    """Печать успешного сообщения."""
    print(f"  [OK] {text}")


def print_error(text):
    """Печать сообщения об ошибке."""
    print(f"  [ERROR] {text}")


def print_info(text):
    """Печать информационного сообщения."""
    print(f"  [i] {text}")


def create_sample_players():
   
    print_subheader("Создание тестовых игроков")
    
    players = [
        Player("Сашка", level=8, health=95.0, experience=7500),
        Player("КайАнжела", level=5, health=45.5, experience=4800),
        Player("Иен", level=6, health=100.0, experience=5900),
        Player("Артем", level=3, health=80.0, experience=2500),
        Player("Милана", level=2, health=100.0, experience=1500),
        Player("Дмитрий", level=10, health=30.0, experience=9000),
    ]
    
    for p in players:
        print(f"  Создан: {p.name} (ур. {p.level})")
    
    return players


def scenario_1_basic_operations():

    print_header("СЦЕНАРИЙ 1: БАЗОВЫЕ ОПЕРАЦИИ С КОЛЛЕКЦИЕЙ")
    
    # Создаем пустую коллекцию
    print_subheader("Создание пустой коллекции")
    player_list = PlayerList()
    print(f"  Коллекция создана. Размер: {len(player_list)}")
    
    # Создаем тестовых игроков
    players = create_sample_players()
    
    # Добавляем игроков в коллекцию
    print_subheader("Добавление игроков в коллекцию")
    for player in players[:3]:  # Добавляем первых трех
        try:
            player_list.add(player)
        except Exception as e:
            print_error(str(e))
    
    print_info(f"Текущий размер коллекции: {len(player_list)}")
    
    # Выводим всех игроков
    print_subheader("Все игроки в коллекции (get_all)")
    all_players = player_list.get_all()
    for i, player in enumerate(all_players, 1):
        print(f"  {i}. {player.name} (ур. {player.level}) - {player.title}")
    
    # Добавляем еще игроков
    print_subheader("Добавление остальных игроков")
    for player in players[3:]:
        try:
            player_list.add(player)
        except Exception as e:
            print_error(str(e))
    
    print_info(f"Размер коллекции после добавления: {len(player_list)}")
    
    # Показываем всю коллекцию через __str__
    print_subheader("Представление коллекции (__str__)")
    print(player_list)
    
    # Удаляем игрока
    print_subheader("Удаление игрока")
    try:
        player_list.remove(players[0])  # Удаляем Сашку
        print_success(f"Игрок '{players[0].name}' удален")
    except Exception as e:
        print_error(str(e))
    
    print_info(f"Размер коллекции после удаления: {len(player_list)}")
    print_info("Оставшиеся игроки:")
    for player in player_list.get_all():
        print(f"    - {player.name}")
    
    # Пробуем добавить дубликат
    print_subheader("Проверка защиты от дубликатов")
    try:
        player_list.add(players[1])  # Пытаемся добавить уже существующего
        print_error("Дубликат добавился (ошибка защиты)!")
    except ValueError as e:
        print_success(f"Защита сработала: {e}")
    
    # Пробуем добавить не Player
    print_subheader("Проверка типа добавляемого объекта")
    try:
        player_list.add("Не игрок")  # type: ignore
        print_error("Строка добавилась (ошибка типа)!")
    except TypeError as e:
        print_success(f"Защита сработала: {e}")
    
    return player_list


def scenario_2_search_and_iteration(collection: PlayerList):
    """
    Сценарий 2: Поиск и итерация (на оценку 4).
    find_by_*, __len__, __iter__.
    """
    print_header("СЦЕНАРИЙ 2: ПОИСК И ИТЕРАЦИЯ")
    
    # Демонстрация __len__
    print_subheader("Количество игроков (__len__)")
    print_info(f"В коллекции {len(collection)} игроков")
    
    # Демонстрация __iter__ (for ... in ...)
    print_subheader("Перебор всех игроков (__iter__)")
    for i, player in enumerate(collection):
        print(f"  {i+1}. {player.name} - ур. {player.level}, здоровье: {player.health}")
    
    # Поиск по имени
    print_subheader("Поиск по имени (find_by_name)")
    search_name = "Иен"
    found = collection.find_by_name(search_name)
    if found:
        print_success(f"Найден игрок: {found.name} (ур. {found.level})")
    else:
        print_error(f"Игрок '{search_name}' не найден")
    
    # Поиск несуществующего
    search_name = "Несуществующий"
    found = collection.find_by_name(search_name)
    if found:
        print_error(f"Найден {found.name} (ошибка!)")
    else:
        print_success(f"Игрок '{search_name}' не найден - верно")
    
    # Поиск по уровню
    print_subheader("Поиск по уровню (find_by_level)")
    target_level = 5
    found_players = collection.find_by_level(target_level)
    print_info(f"Игроки {target_level} уровня:")
    for player in found_players:
        print(f"    - {player.name}")
    
    # Поиск по титулу
    print_subheader("Поиск по титулу (find_by_title)")
    target_title = "Ветеран"
    found_players = collection.find_by_title(target_title)
    print_info(f"Игроки с титулом '{target_title}':")
    for player in found_players:
        print(f"    - {player.name} (ур. {player.level})")
    
    # Проверка оператора in (__contains__)
    print_subheader("Проверка наличия (оператор 'in')")
    sample_player = collection.find_by_name("Артем")
    if sample_player:
        print_info(f"Проверка: 'Артем' in коллекция? {sample_player in collection}")
    
    non_existent = Player("Тест", level=1)
    print_info(f"Проверка: 'Тест' in коллекция? {non_existent in collection}")


def scenario_3_indexing_and_deletion(collection: PlayerList):
    """
    Сценарий 3: Индексация и удаление по индексу (на оценку 5).
    __getitem__, remove_at.
    """
    print_header("СЦЕНАРИЙ 3: ИНДЕКСАЦИЯ И УДАЛЕНИЕ ПО ИНДЕКСУ")
    
    # Демонстрация __getitem__
    print_subheader("Доступ по индексу (__getitem__)")
    print_info(f"Первый игрок (индекс 0): {collection[0].name}")
    print_info(f"Последний игрок (индекс {len(collection)-1}): {collection[len(collection)-1].name}")
    
    # Пробуем получить несуществующий индекс
    print_subheader("Проверка обработки ошибки индекса")
    try:
        invalid = collection[100]
        print_error(f"Не должно быть доступа: {invalid}")
    except IndexError as e:
        print_success(f"Ошибка индекса обработана: {e}")
    
    # Удаление по индексу
    print_subheader("Удаление по индексу (remove_at)")
    print_info(f"До удаления: {len(collection)} игроков")
    
    # Удаляем первого игрока
    removed = collection.remove_at(0)
    print_info(f"Удален игрок: {removed.name}")
    print_info(f"После удаления: {len(collection)} игроков")
    
    print_info("Оставшиеся игроки:")
    for i, player in enumerate(collection):
        print(f"    [{i}] {player.name}")
    
    # Пробуем удалить по неверному индексу
    print_subheader("Проверка удаления по неверному индексу")
    try:
        collection.remove_at(999)
        print_error("Удаление по неверному индексу сработало!")
    except IndexError as e:
        print_success(f"Ошибка обработана: {e}")


def scenario_4_sorting_and_filtering(collection: PlayerList):
    """
    Сценарий 4: Сортировка и фильтрация (на оценку 5).
    sort_by_*, sort, find_alive.
    """
    print_header("СЦЕНАРИЙ 4: СОРТИРОВКА И ФИЛЬТРАЦИЯ")
    
    # Сначала добавим еще несколько игроков для полноты демонстрации
    print_subheader("Добавляем дополнительных игроков")
    try:
        new_players = [
            Player("Алексей", level=7, health=80.0, experience=6500),
            Player("Борис", level=4, health=60.0, experience=3500),
            Player("Виктория", level=9, health=90.0, experience=8500),
        ]
        for p in new_players:
            collection.add(p)
    except ValueError as e:
        print_error(str(e))
    
    # Сортировка по имени
    print_subheader("Сортировка по имени (sort_by_name)")
    sorted_by_name = collection.sort_by_name()
    print_info("Игроки в алфавитном порядке:")
    for player in sorted_by_name:
        print(f"    - {player.name} (ур. {player.level})")
    
    # Сортировка по имени в обратном порядке
    print_subheader("Сортировка по имени (обратный порядок)")
    sorted_by_name_desc = collection.sort_by_name(reverse=True)
    print_info("Игроки в обратном алфавитном порядке:")
    for player in sorted_by_name_desc:
        print(f"    - {player.name} (ур. {player.level})")
    
    # Сортировка по уровню
    print_subheader("Сортировка по уровню (sort_by_level)")
    sorted_by_level = collection.sort_by_level()
    print_info("Игроки по возрастанию уровня:")
    for player in sorted_by_level:
        print(f"    - {player.name}: уровень {player.level}")
    
    # Универсальная сортировка
    print_subheader("Универсальная сортировка (sort)")
    sorted_by_health = collection.sort(key="health", reverse=True)
    print_info("Игроки по убыванию здоровья:")
    for player in sorted_by_health:
        print(f"    - {player.name}: здоровье {player.health}")
    
    # Фильтрация - живые игроки
    print_subheader("Фильтрация: только живые игроки (find_alive)")
    # Сначала нанесем немного урона некоторым игрокам
    print_info("Наносим урон некоторым игрокам...")
    for player in collection:
        if player.name in ["КайАнжела", "Дмитрий"]:
            player.take_damage(100)  # Убиваем их
    
    alive_players = collection.find_alive()
    print_info(f"Живых игроков: {len(alive_players)} из {len(collection)}")
    for player in alive_players:
        print(f"    - {player.name}: здоровье {player.health}")
    
    # Воскрешаем одного для следующего сценария
    print_info("Воскрешаем КайАнжелу...")
    for player in collection:
        if player.name == "КайАнжела":
            player.revive()
            break


def scenario_5_comprehensive_demo():
    """
    Сценарий 5: Комплексная демонстрация всех возможностей.
    Создание новой коллекции с нуля.
    """
    print_header("СЦЕНАРИЙ 5: КОМПЛЕКСНАЯ ДЕМОНСТРАЦИЯ")
    
    # Создаем новую коллекцию
    print_subheader("Создание новой коллекции")
    tournament = PlayerList()
    
    # Добавляем игроков для турнира
    tournament_players = [
        Player("Елена", level=5, health=100.0, experience=4500),
        Player("Максим", level=7, health=85.0, experience=6800),
        Player("Ольга", level=3, health=95.0, experience=2800),
        Player("Сергей", level=9, health=70.0, experience=8800),
        Player("Татьяна", level=4, health=100.0, experience=3800),
    ]
    
    print_info("Добавляем игроков в турнирную таблицу:")
    for p in tournament_players:
        tournament.add(p)
    
    # Показываем исходное состояние
    print_subheader("Исходное состояние турнирной таблицы")
    print(tournament)
    
    # Сортировка для определения мест
    print_subheader("Турнирная таблица по уровню (сильнейшие сверху)")
    ranked = tournament.sort_by_level(reverse=True)
    print_info("Рейтинг игроков:")
    for i, player in enumerate(ranked, 1):
        print(f"  {i}. {player.name} - уровень {player.level} ({player.title})")
    
    # Симуляция боев
    print_subheader("Симуляция боев")
    for i in range(len(tournament) - 1):
        attacker = tournament[i]
        defender = tournament[i + 1]
        print_info(f"Бой: {attacker.name} vs {defender.name}")
        defender.take_damage(30)
        if not defender.is_alive:
            print_info(f"  {defender.name} повержен!")
    
    print_subheader("Состояние после боев")
    for player in tournament:
        status = "ЖИВ" if player.is_alive else "МЕРТВ"
        print(f"  {player.name}: здоровье {player.health} - {status}")
    
    # Получаем выживших
    print_subheader("Выжившие участники")
    survivors = tournament.find_alive()
    print_info(f"Выжило {len(survivors)} из {len(tournament)} игроков")
    for player in survivors:
        print(f"  - {player.name} (ур. {player.level})")
    
    # Итоговая статистика
    print_subheader("Итоговая статистика")
    print_info(f"Всего игроков в турнире: {len(tournament)}")
    print_info(f"Максимальный уровень: {max(p.level for p in tournament)}")
    print_info(f"Минимальный уровень: {min(p.level for p in tournament)}")
    print_info(f"Среднее здоровье: {sum(p.health for p in tournament) / len(tournament):.1f}")


def main():
    """Главная функция демонстрации."""
    print_header("ЛАБОРАТОРНАЯ РАБОТА №2: КЛАСС PLAYERLIST")
    print("Реализация на оценку 5 - Вариант 6")
    
    # Запускаем все сценарии
    # Сценарий 1 - базовые операции
    collection = scenario_1_basic_operations()
    
    # Сценарий 2 - поиск и итерация
    scenario_2_search_and_iteration(collection)
    
    # Сценарий 3 - индексация и удаление по индексу
    scenario_3_indexing_and_deletion(collection)
    
    # Сценарий 4 - сортировка и фильтрация
    scenario_4_sorting_and_filtering(collection)
    
    # Сценарий 5 - комплексная демонстрация
    scenario_5_comprehensive_demo()
    
    print_header("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("Реализовано:")
    print("  [3] - Базовые операции: add, remove, get_all, проверка типа")
    print("  [4] - Поиск (name/level/title), __len__, __iter__, защита от дубликатов")
    print("  [5] - Индексация (__getitem__), remove_at, сортировка, фильтрация")


if __name__ == "__main__":
    main()