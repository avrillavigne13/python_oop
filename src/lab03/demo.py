import sys
import os


sys.path.insert(0, os.path.dirname(__file__))  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab02')) 

from base import Player
from collection import PlayerList
from models import Warrior, Mage, Archer


def print_header(text):
    print("\n" + "=" * 80)
    print(f" {text} ".center(80, "="))
    print("=" * 80)


def print_subheader(text):
    print(f"\n--- {text} ---")


def print_info(text):
    print(f"  [i] {text}")


def scenario_1_inheritance():
    print_header("СЦЕНАРИЙ 1: НАСЛЕДОВАНИЕ")
    
    common = Player("Обычный", level=3, health=80)
    warrior = Warrior("Алексей", level=5, armor=30, weapon="Меч")
    mage = Mage("Елена", level=4, mana=100, spell="Молния")
    archer = Archer("Дмитрий", level=3, accuracy=75, bow_type="Лук")
    
    print_subheader("Созданные объекты")
    print(f"  {common}")
    print(f"  {warrior}")
    print(f"  {mage}")
    print(f"  {archer}")
    
    print_subheader("Проверка типов (isinstance)")
    print_info(f"Воин является Player? {isinstance(warrior, Player)}")
    print_info(f"Маг является Warrior? {isinstance(mage, Warrior)}")
    print_info(f"Маг является Mage? {isinstance(mage, Mage)}")
    
    return warrior, mage, archer


def scenario_2_polymorphism():
    print_header("СЦЕНАРИЙ 2: ПОЛИМОРФИЗМ")
    
    players = [
        Player("Обычный", level=5, health=100),
        Warrior("Воин", level=5, health=100, armor=30),
        Mage("Маг", level=5, health=100, mana=100),
        Archer("Лучник", level=5, health=100, accuracy=80)
    ]
    
    print_subheader("Метод get_player_type() - разное поведение")
    for p in players:
        print(f"  {p.name}: {p.get_player_type()}")
    
    print_subheader("Метод calculate_power() - разный расчёт силы")
    for p in players:
        print(f"  {p.name}: сила = {p.calculate_power():.2f}")
    
    print_subheader("Метод take_damage() - разная реакция на урон")
    for p in players:
        result = p.take_damage(40)
        print(f"  {p.name}: {result}")
        p.health = 100


def scenario_3_collection():
    print_header("СЦЕНАРИЙ 3: КОЛЛЕКЦИЯ РАЗНЫХ ТИПОВ")
    
    guild = PlayerList()
    
    guild.add(Player("Странник", level=2))
    guild.add(Warrior("Громобой", level=5, armor=40, weapon="Топор"))
    guild.add(Mage("Мерлин", level=4, mana=120, spell="Огонь"))
    guild.add(Archer("Леголас", level=6, accuracy=90, bow_type="Эльфийский лук"))
    
    print_subheader("Все игроки в коллекции")
    print(guild)
    
    print_subheader("Фильтрация по типу")
    print_info(f"Всего игроков: {len(guild)}")
    print_info(f"Воинов: {len(guild.get_warriors())}")
    print_info(f"Магов: {len(guild.get_mages())}")
    print_info(f"Лучников: {len(guild.get_archers())}")


def scenario_4_polymorphic_collection():
    print_header("СЦЕНАРИЙ 4: ПОЛИМОРФИЗМ В КОЛЛЕКЦИИ")
    
    party = PlayerList()
    party.add(Warrior("Ахиллес", level=8, armor=50, weapon="Копье"))
    party.add(Mage("Цирцея", level=7, mana=140, spell="Превращение"))
    party.add(Archer("Артемида", level=6, accuracy=85, bow_type="Лук"))
    
    print_subheader("Особые атаки каждого класса")
    for player in party:
        if isinstance(player, Warrior):
            print(f"  {player.power_attack()}")
        elif isinstance(player, Mage):
            print(f"  {player.cast_spell()}")
        elif isinstance(player, Archer):
            print(f"  {player.critical_shot()}")


def scenario_5_game_simulation():
    print_header("СЦЕНАРИЙ 5: ИГРОВАЯ СИМУЛЯЦИЯ")
    
    heroes = PlayerList()
    heroes.add(Warrior("Ричард", level=3, armor=30, weapon="Меч"))
    heroes.add(Mage("Моргана", level=3, mana=100, spell="Огненный шар"))
    heroes.add(Archer("Робин", level=3, accuracy=75, bow_type="Лук"))
    
    print_subheader("Отряд героев")
    print(heroes)
    
    print_subheader("Герои получают опыт")
    for player in heroes:
        print_info(player.add_experience(800))
    
    print_subheader("Сражение с драконом")
    for player in heroes:
        print_info(f"\nДракон атакует {player.name}!")
        print(f"  {player.take_damage(45)}")


def main():
    print_header("ЛАБОРАТОРНАЯ РАБОТА №3: НАСЛЕДОВАНИЕ И ПОЛИМОРФИЗМ")
    print("Вариант 6 - Игрок (Player)")
    
    scenario_1_inheritance()
    scenario_2_polymorphism()
    scenario_3_collection()
    scenario_4_polymorphic_collection()
    scenario_5_game_simulation()
    
    print_header("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")


if __name__ == "__main__":
    main()