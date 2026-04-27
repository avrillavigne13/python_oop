# lab04/demo.py
import sys
import os

src_path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_path)
sys.path.insert(0, os.path.dirname(__file__))

from lab04.interfaces import Printable, Comparable, Damageable
from lab04.models import Player, Warrior, Mage, Archer
from lab04.collection import PlayerList


def print_header(text):
    print("\n" + "=" * 80)
    print(f" {text} ".center(80, "="))
    print("=" * 80)


def print_subheader(text):
    print(f"\n--- {text} ---")


def print_info(text):
    print(f"  [i] {text}")


def scenario_1_interfaces():
    print_header("СЦЕНАРИЙ 1: ИНТЕРФЕЙСЫ (оценка 3)")
    
    player = Player("Обычный", level=3)
    warrior = Warrior("Алексей", level=5, armor=30, weapon="Меч")
    mage = Mage("Елена", level=4, mana=100, spell="Молния")
    archer = Archer("Дмитрий", level=3, accuracy=75, bow_type="Лук")
    
    print_subheader("Созданные объекты")
    print(f"  {player.to_string()}")
    print(f"  {warrior.to_string()}")
    print(f"  {mage.to_string()}")
    print(f"  {archer.to_string()}")
    
    print_subheader("Проверка реализации интерфейсов")
    print_info(f"Player реализует Printable? {isinstance(player, Printable)}")
    print_info(f"Warrior реализует Printable? {isinstance(warrior, Printable)}")
    print_info(f"Player реализует Comparable? {isinstance(player, Comparable)}")
    print_info(f"Player реализует Damageable? {isinstance(player, Damageable)}")
    
    return player, warrior, mage, archer


def scenario_2_polymorphism_and_comparable():
    print_header("СЦЕНАРИЙ 2: ПОЛИМОРФИЗМ И СРАВНЕНИЕ (оценка 4)")
    
    warrior = Warrior("Воин", level=5, health=100, armor=30, weapon="Меч")
    mage = Mage("Маг", level=5, health=100, mana=10, spell="Молния")
    
    warrior_power = warrior.calculate_power()
    mage_power = mage.calculate_power()
    
    print_info(f"{warrior.name}: сила = {warrior_power:.2f}")
    print_info(f"{mage.name}: сила = {mage_power:.2f}")
    
    result = warrior.compare_to(mage)
    print_info(f"Результат compare_to: {result}")
    
    print_subheader("Результат сравнения")
    if result < 0:
        print(f"  {warrior.name} СЛАБЕЕ, чем {mage.name}")
    elif result > 0:
        print(f"  {warrior.name} СИЛЬНЕЕ, чем {mage.name}")
    else:
        print(f"  {warrior.name} и {mage.name} РАВНЫ по силе")


def scenario_3_collection_with_interfaces():
    print_header("СЦЕНАРИЙ 3: КОЛЛЕКЦИЯ И ИНТЕРФЕЙСЫ (оценка 5)")
    
    guild = PlayerList()
    
    print_subheader("Добавление игроков")
    guild.add(Player("Странник", level=2))
    guild.add(Warrior("Громобой", level=5, armor=40, weapon="Топор"))
    guild.add(Mage("Мерлин", level=4, mana=120, spell="Огонь"))
    guild.add(Archer("Леголас", level=6, accuracy=90, bow_type="Эльфийский лук"))
    
    print_subheader("Все игроки")
    print(guild)
    
    print_subheader("Фильтрация по интерфейсу Printable")
    printable = guild.get_printable()
    print_info(f"Printable объектов: {len(printable)} из {len(guild)}")
    
    print_subheader("Фильтрация по интерфейсу Comparable")
    comparable = guild.get_comparable()
    print_info(f"Comparable объектов: {len(comparable)} из {len(guild)}")
    
    print_subheader("Сортировка по силе")
    sorted_by_power = guild.sort_by_power(reverse=True)
    print_info("Игроки от сильнейшего к слабейшему:")
    for i, player in enumerate(sorted_by_power, 1):
        print(f"    {i}. {player.name:12} | сила: {player.calculate_power():.2f}")


def scenario_4_test_damageable():
    print_header("СЦЕНАРИЙ 4: ТЕСТИРОВАНИЕ DAMAGEABLE")
    
    heroes = PlayerList()
    heroes.add(Warrior("Ричард", level=3, health=100, armor=30, weapon="Меч"))
    heroes.add(Mage("Моргана", level=3, health=100, mana=100, spell="Огненный шар"))
    heroes.add(Archer("Робин", level=3, health=100, accuracy=75, bow_type="Лук"))
    
    print_subheader("Получение урона")
    for player in heroes:
        print(f"  {player.take_damage(30)}")
    
    print_subheader("Лечение")
    for player in heroes:
        print(f"  {player.heal(20)}")


def main():
    print_header("ЛАБОРАТОРНАЯ РАБОТА №4: ИНТЕРФЕЙСЫ")
    print("Вариант 6 - Игрок (Player)")
    print("Оценка 5 - интерфейсы: Printable, Comparable, Damageable")
    
    scenario_1_interfaces()
    scenario_2_polymorphism_and_comparable()
    scenario_3_collection_with_interfaces()
    scenario_4_test_damageable()
    
    print_header("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")


if __name__ == "__main__":
    main()