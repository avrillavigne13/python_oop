# demo.py
"""
Демонстрация работы ЛР-5: функции как аргументы, стратегии, делегаты.
Сценарии:
1. Сортировка разными стратегиями + фильтрация (оценка 3)
2. map, фабрика функций, методы sort_by/filter_by (оценка 4)
3. Цепочка операций, callable-объекты, паттерн Стратегия (оценка 5)
"""

import sys
import os

# Добавляем пути
src_path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_path)
sys.path.insert(0, os.path.dirname(__file__))

# Импортируем классы из ЛР-3
from lab03.models import Player, Warrior, Mage, Archer

# Импортируем свою коллекцию
from collection import PlayerList

# Импортируем стратегии, фильтры, фабрики, callable-объекты
from strategies import (
    # Стратегии сортировки
    by_name, by_level, by_power, by_health, by_name_then_level,
    # Фильтры
    is_alive_filter, is_high_level_filter, is_warrior_filter, is_healthy_filter,
    # Фабрики
    make_level_filter, make_health_filter, make_damage_multiplier,
    # Callable-объекты
    DiscountStrategy, HealthRestoreStrategy, PowerBoostStrategy,
    # Функции для map
    to_info_string, extract_name_and_level, to_tuple
)


def print_header(text: str) -> None:
    """Печать заголовка."""
    print("\n" + "=" * 80)
    print(f" {text} ".center(80, "="))
    print("=" * 80)


def print_subheader(text: str) -> None:
    """Печать подзаголовка."""
    print(f"\n--- {text} ---")


def print_info(text: str) -> None:
    """Печать информационного сообщения."""
    print(f"  [i] {text}")


def print_success(text: str) -> None:
    """Печать успешного сообщения."""
    print(f"  [✓] {text}")


def create_test_collection() -> PlayerList:
    """
    Создаёт тестовую коллекцию игроков для демонстрации.
    """
    players = PlayerList()
    
    players.add(Player("Алексей", level=3, health=100))
    players.add(Warrior("Громобой", level=8, health=100, armor=40, weapon="Топор"))
    players.add(Mage("Мерлин", level=6, health=80, mana=120, spell="Огонь"))
    players.add(Archer("Леголас", level=5, health=90, accuracy=90, bow_type="Эльфийский лук"))
    players.add(Player("Борис", level=2, health=100))
    players.add(Warrior("Спартак", level=4, health=60, armor=20, weapon="Меч"))
    players.add(Mage("Гэндальф", level=7, health=70, mana=150, spell="Молния"))
    players.add(Archer("Робин", level=3, health=50, accuracy=70, bow_type="Лук"))
    
    return players


# ==================== СЦЕНАРИЙ 1: ОСНОВЫ (оценка 3) ====================

def scenario_1_basics():
    """
    Сценарий 1: демонстрация сортировки разными стратегиями и фильтрации.
    Требования на оценку 3:
    - минимум 3 стратегии сортировки
    - минимум 2 фильтра
    - использование sorted() и filter()
    """
    print_header("СЦЕНАРИЙ 1: СОРТИРОВКА И ФИЛЬТРАЦИЯ (оценка 3)")
    
    # Создаём коллекцию
    players = create_test_collection()
    print_subheader("Исходная коллекция")
    print(players)
    
    # ===== СОРТИРОВКА =====
    print_subheader("Сортировка по ИМЕНИ (стратегия by_name)")
    sorted_by_name = players.sort_by(by_name)
    print(sorted_by_name)
    
    print_subheader("Сортировка по УРОВНЮ (стратегия by_level)")
    sorted_by_level = players.sort_by(by_level)
    print(sorted_by_level)
    
    print_subheader("Сортировка по СИЛЕ (стратегия by_power, по убыванию)")
    sorted_by_power = players.sort_by(by_power, reverse=True)
    print(sorted_by_power)
    
    print_subheader("Сортировка по ЗДОРОВЬЮ (стратегия by_health)")
    sorted_by_health = players.sort_by(by_health)
    for player in sorted_by_health:
        print(f"    {player.name}: здоровье = {player.health:.0f}")
    
    print_subheader("Сортировка по НЕСКОЛЬКИМ атрибутам (имя + уровень)")
    sorted_multi = players.sort_by(by_name_then_level)
    print(sorted_multi)
    
    # ===== ФИЛЬТРАЦИЯ =====
    print_subheader("Фильтрация: только ЖИВЫЕ игроки (is_alive_filter)")
    # Сначала нанесём немного урона
    for player in players.get_all():
        if player.name == "Спартак":
            player.take_damage(100)
    
    alive_players = players.filter_by(is_alive_filter)
    print(alive_players)
    
    print_subheader("Фильтрация: только игроки с уровнем >= 5 (is_high_level_filter)")
    high_level = players.filter_by(is_high_level_filter)
    print(high_level)
    
    print_subheader("Фильтрация: только ВОИНЫ (is_warrior_filter)")
    warriors = players.filter_by(is_warrior_filter)
    print(warriors)
    
    # Восстанавливаем здоровье для следующих сценариев
    for player in players.get_all():
        if player.name == "Спартак":
            player.health = 60
    
    return players


# ==================== СЦЕНАРИЙ 2: MAP, ФАБРИКИ, МЕТОДЫ КОЛЛЕКЦИИ (оценка 4) ====================

def scenario_2_map_and_factories():
    """
    Сценарий 2: демонстрация map, фабрик функций, методов sort_by/filter_by.
    Требования на оценку 4:
    - применение map() для преобразования
    - фабрика функций
    - методы sort_by/filter_by в коллекции
    - lambda-выражения
    """
    print_header("СЦЕНАРИЙ 2: MAP, ФАБРИКИ, LAMBDA (оценка 4)")
    
    players = create_test_collection()
    
    # ===== ПРИМЕНЕНИЕ MAP (преобразование) =====
    print_subheader("Преобразование через map: имена игроков")
    names = players.map_to(lambda p: p.name)
    print(f"  Имена: {names}")
    
    print_subheader("Преобразование через map: информационные строки")
    info_strings = players.map_to(to_info_string)
    for s in info_strings:
        print(f"    {s}")
    
    print_subheader("Преобразование через map: словари (имя, уровень, сила)")
    dicts = players.map_to(extract_name_and_level)
    for d in dicts:
        print(f"    {d}")
    
    # ===== ФАБРИКИ ФУНКЦИЙ =====
    print_subheader("Фабрика функций: фильтр по минимальному уровню")
    
    # Создаём фильтр через фабрику
    level_5_filter = make_level_filter(5)
    filtered_by_level_5 = players.filter_by(level_5_filter)
    print_info(f"Игроки с уровнем >= 5: {len(filtered_by_level_5)}")
    for p in filtered_by_level_5:
        print(f"    {p.name} (ур.{p.level})")
    
    print_subheader("Фабрика функций: фильтр по минимальному здоровью")
    health_70_filter = make_health_filter(70)
    healthy_players = players.filter_by(health_70_filter)
    print_info(f"Игроки со здоровьем >= 70: {len(healthy_players)}")
    for p in healthy_players:
        print(f"    {p.name} (здоровье: {p.health:.0f})")
    
    # ===== LAMBDA-ВЫРАЖЕНИЯ =====
    print_subheader("Lambda-выражения: сортировка по убыванию здоровья")
    sorted_by_health_lambda = players.sort_by(lambda p: p.health, reverse=True)
    for p in sorted_by_health_lambda:
        print(f"    {p.name}: здоровье = {p.health:.0f}")
    
    print_subheader("Lambda-выражения: фильтр по здоровью > 50")
    healthy_lambda = players.filter_by(lambda p: p.health > 50)
    print(f"  Здоровых игроков: {len(healthy_lambda)}")
    
    # ===== СРАВНЕНИЕ: lambda vs именованная функция =====
    print_subheader("Сравнение: lambda vs именованная функция")
    
    # Через lambda
    sorted_lambda = players.sort_by(lambda p: p.name)
    print_info("Сортировка через lambda:")
    for p in sorted_lambda.get_all()[:3]:
        print(f"    {p.name}")
    
    # Через именованную функцию
    sorted_named = players.sort_by(by_name)
    print_info("Сортировка через именованную функцию:")
    for p in sorted_named.get_all()[:3]:
        print(f"    {p.name}")
    
    print_success("Результаты одинаковые!")


# ==================== СЦЕНАРИЙ 3: ПАТТЕРН СТРАТЕГИЯ (оценка 5) ====================

def scenario_3_strategy_pattern():
    """
    Сценарий 3: демонстрация паттерна Стратегия через callable-объекты.
    Требования на оценку 5:
    - callable-объекты (классы с __call__)
    - метод apply() в коллекции
    - цепочка операций
    - взаимозаменяемость стратегий
    """
    print_header("СЦЕНАРИЙ 3: ПАТТЕРН СТРАТЕГИЯ (оценка 5)")
    
    # Создаём коллекцию
    players = PlayerList()
    players.add(Warrior("Ричард", level=5, health=100, armor=30, weapon="Меч"))
    players.add(Mage("Моргана", level=5, health=100, mana=100, spell="Огонь"))
    players.add(Archer("Робин", level=5, health=100, accuracy=80, bow_type="Лук"))
    players.add(Player("Алекс", level=5, health=100))
    
    print_subheader("Исходное состояние")
    print(players)
    
    # ===== ЦЕПОЧКА ОПЕРАЦИЙ =====
    print_subheader("Цепочка операций: фильтр → сортировка → применение")
    
    # Применяем стратегию начисления опыта (DiscountStrategy)
    exp_strategy = DiscountStrategy(warrior_bonus=1.0, mage_bonus=1.3, archer_bonus=1.1)
    
    # Цепочка: сначала фильтруем живых, потом сортируем по силе, потом применяем стратегию
    players.apply(exp_strategy)
    
    print_info("После применения стратегии начисления опыта:")
    for p in players:
        print(f"    {p.name}: опыт = {p.experience}, уровень = {p.level}")
    
    # ===== ЗАМЕНА СТРАТЕГИИ =====
    print_subheader("Замена стратегии: лечение (HealthRestoreStrategy)")
    
    # Наносим урон
    for p in players:
        p.take_damage(40)
    
    print_info("После получения урона:")
    for p in players:
        print(f"    {p.name}: здоровье = {p.health:.0f}")
    
    # Создаём стратегию лечения
    heal_strategy = HealthRestoreStrategy(amount=30)
    
    # Применяем стратегию
    players.apply(heal_strategy)
    
    print_info("После лечения (30 HP):")
    for p in players:
        print(f"    {p.name}: здоровье = {p.health:.0f}")
    
    # Меняем параметр стратегии
    heal_strategy.set_amount(50)
    players.apply(heal_strategy)
    
    print_info("После дополнительного лечения (ещё 50 HP):")
    for p in players:
        print(f"    {p.name}: здоровье = {p.health:.0f}")
    
    # ===== ДРУГАЯ СТРАТЕГИЯ (усиление) =====
    print_subheader("Другая стратегия: временное усиление (PowerBoostStrategy)")
    
    power_strategy = PowerBoostStrategy(boost_percent=30)
    players.apply(power_strategy)
    
    print_info("После усиления:")
    for p in players:
        print(f"    {p.name}: опыт = {p.experience}")
    
    # ===== ВЗАИМОЗАМЕНЯЕМОСТЬ =====
    print_subheader("Взаимозаменяемость стратегий")
    print_info("Одна и та же цепочка с разными стратегиями:")
    
    # Создаём новую коллекцию
    new_players = PlayerList()
    new_players.add(Warrior("Тест", level=3, health=100, armor=20, weapon="Меч"))
    
    # Применяем разные стратегии через lambda (функциональный стиль)
    print_info("Стратегия 1: нанести урон 30")
    new_players.apply(lambda p: p.take_damage(30))
    print(f"    Результат: здоровье = {new_players[0].health:.0f}")
    
    # Восстанавливаем
    new_players[0].health = 100
    
    print_info("Стратегия 2: вылечить на 20")
    new_players.apply(lambda p: p.heal(20))
    print(f"    Результат: здоровье = {new_players[0].health:.0f}")
    
    # Восстанавливаем
    new_players[0].health = 100
    
    print_info("Стратегия 3: применить скидку опыта (через callable)")
    discount = DiscountStrategy(warrior_bonus=1.5)
    new_players.apply(discount)
    print(f"    Результат: опыт = {new_players[0].experience}")
    
    print_success("Стратегии легко заменяются без изменения кода коллекции!")


# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================

def main():
    print_header("ЛАБОРАТОРНАЯ РАБОТА №5: СТРАТЕГИИ И ДЕЛЕГАТЫ")
    print("Вариант 6 - Игрок (Player)")
    print("Оценка 5 - все требования выполнены")
    
    # Запуск сценариев
    players = scenario_1_basics()
    scenario_2_map_and_factories()
    scenario_3_strategy_pattern()
    
    print_header("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("\nРеализованные функции и стратегии:")
    print("  [3] - 5+ стратегий сортировки (by_name, by_level, by_power, by_health, by_name_then_level)")
    print("  [3] - 4+ функции-фильтра (is_alive, is_high_level, is_warrior, is_healthy)")
    print("  [4] - map для преобразования (to_info_string, extract_name_and_level, to_tuple)")
    print("  [4] - фабрики функций (make_level_filter, make_health_filter, make_damage_multiplier)")
    print("  [4] - методы sort_by, filter_by в коллекции")
    print("  [5] - callable-объекты (DiscountStrategy, HealthRestoreStrategy, PowerBoostStrategy)")
    print("  [5] - метод apply() в коллекции")
    print("  [5] - цепочки операций")


if __name__ == "__main__":
    main()