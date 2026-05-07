import sys
import os
from typing import Callable, Any, TYPE_CHECKING

# Добавляем путь к lab03 для импорта классов
src_path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_path)

# Импортируем классы из ЛР-3
from lab03.models import Player, Warrior, Mage, Archer


# ========== 1. СТРАТЕГИИ СОРТИРОВКИ (для задания на 3) ==========

def by_name(player: 'Player') -> str:
    """
    Стратегия сортировки по имени.
    Возвращает имя игрока для сравнения.
    """
    return player.name


def by_level(player: 'Player') -> int:
    """
    Стратегия сортировки по уровню.
    Возвращает уровень игрока.
    """
    return player.level


def by_power(player: 'Player') -> float:
    """
    Стратегия сортировки по силе.
    Возвращает силу игрока (уровень * здоровье% * бонус класса).
    """
    return player.calculate_power()


def by_health(player: 'Player') -> float:
    """
    Стратегия сортировки по здоровью.
    """
    return player.health


def by_name_then_level(player: 'Player') -> tuple:
    """
    Стратегия сортировки по нескольким атрибутам (сначала имя, потом уровень).
    Возвращает кортеж для многоуровневой сортировки.
    """
    return (player.name, player.level)


# ========== 2. ФУНКЦИИ-ФИЛЬТРЫ (для задания на 3) ==========

def is_alive_filter(player: 'Player') -> bool:
    """
    Фильтр: оставляет только живых игроков.
    """
    return player.is_alive


def is_high_level_filter(player: 'Player') -> bool:
    """
    Фильтр: оставляет игроков с уровнем 5 и выше.
    """
    return player.level >= 5


def is_warrior_filter(player: 'Player') -> bool:
    """
    Фильтр: оставляет только воинов.
    """
    from models import Warrior
    return isinstance(player, Warrior)


def is_mage_filter(player: 'Player') -> bool:
    """
    Фильтр: оставляет только магов.
    """
    from models import Mage
    return isinstance(player, Mage)


def is_healthy_filter(player: 'Player') -> bool:
    """
    Фильтр: оставляет игроков с здоровьем больше 50.
    """
    return player.health > 50


# ========== 3. ФАБРИКИ ФУНКЦИЙ (для задания на 4) ==========

def make_level_filter(min_level: int) -> Callable[[Player], bool]:
    """
    Фабрика функций: создаёт фильтр по минимальному уровню.
    
    Аргументы:
        min_level: минимальный уровень для фильтрации
    
    Возвращает:
        функцию, которая принимает игрока и возвращает True, если его уровень >= min_level
    
    Пример:
        high_level = make_level_filter(7)
        result = list(filter(high_level, players))
    """
    def filter_by_level(player: 'Player') -> bool:
        return player.level >= min_level
    return filter_by_level


def make_health_filter(min_health: float) -> Callable[[Player], bool]:
    """
    Фабрика функций: создаёт фильтр по минимальному здоровью.
    """
    def filter_by_health(player: 'Player') -> bool:
        return player.health >= min_health
    return filter_by_health


def make_power_threshold(threshold: float) -> Callable[[Player], bool]:
    """
    Фабрика функций: создаёт фильтр по минимальной силе.
    """
    def filter_by_power(player: 'Player') -> bool:
        return player.calculate_power() >= threshold
    return filter_by_power


def make_damage_multiplier(multiplier: float) -> Callable[[Player], None]:
    """
    Фабрика функций: создаёт функцию для нанесения урона с множителем.
    
    Аргументы:
        multiplier: множитель урона (например, 1.5 для усиленной атаки)
    
    Возвращает:
        функцию, которая применяет урон равный level * 10 * multiplier
    """
    def apply_damage(player: 'Player') -> None:
        damage = player.level * 10 * multiplier
        player.take_damage(damage)
    return apply_damage


# ========== 4. CALLABLE-ОБЪЕКТЫ (для задания на 5) ==========

class DiscountStrategy:
    """
    Стратегия начисления опыта в зависимости от типа игрока.
    Callable-объект: реализует метод __call__.
    """
    
    def __init__(self, warrior_bonus: float = 1.0, mage_bonus: float = 1.2, archer_bonus: float = 1.0):
        """
        Аргументы:
            warrior_bonus: множитель опыта для воина
            mage_bonus: множитель опыта для мага
            archer_bonus: множитель опыта для лучника
        """
        self.warrior_bonus = warrior_bonus
        self.mage_bonus = mage_bonus
        self.archer_bonus = archer_bonus
    
    def __call__(self, player: 'Player') -> None:
        """
        Применяет стратегию к игроку: добавляет опыт с учётом бонуса класса.
        """
        from models import Warrior, Mage, Archer
        
        if isinstance(player, Warrior):
            bonus = self.warrior_bonus
        elif isinstance(player, Mage):
            bonus = self.mage_bonus
        elif isinstance(player, Archer):
            bonus = self.archer_bonus
        else:
            bonus = 1.0
        
        exp_amount = int(50 * bonus)
        player.add_experience(exp_amount)


class HealthRestoreStrategy:
    """
    Стратегия восстановления здоровья.
    Можно менять величину лечения (через параметр или через метод).
    """
    
    def __init__(self, amount: float = 30.0):
        """
        Аргументы:
            amount: количество восстанавливаемого здоровья
        """
        self.amount = amount
    
    def set_amount(self, amount: float) -> None:
        """Изменяет величину лечения (демонстрация гибкости)."""
        self.amount = amount
    
    def __call__(self, player: 'Player') -> None:
        """Лечит игрока."""
        player.heal(self.amount)


class PowerBoostStrategy:
    """
    Стратегия временного усиления (для демонстрации apply с изменением состояния).
    """
    
    def __init__(self, boost_percent: float = 20.0):
        """
        Аргументы:
            boost_percent: процент увеличения силы (условно, добавляем опыт)
        """
        self.boost_percent = boost_percent
    
    def __call__(self, player: 'Player') -> None:
        """Увеличивает силу игрока (добавляем опыт пропорционально уровню)."""
        exp_boost = int(player.level * 100 * (self.boost_percent / 100))
        player.add_experience(exp_boost)
        print(f"    {player.name} получил +{exp_boost} опыта (усиление {self.boost_percent}%)")


# ========== 5. ФУНКЦИИ ДЛЯ MAP (для задания на 4) ==========

def to_info_string(player: 'Player') -> str:
    """
    Преобразует игрока в информационную строку.
    Для использования в map().
    """
    return f"{player.name} (ур.{player.level}, сила: {player.calculate_power():.2f})"


def extract_name_and_level(player: 'Player') -> dict:
    """
    Преобразует игрока в словарь с именем и уровнем.
    """
    return {"name": player.name, "level": player.level, "power": round(player.calculate_power(), 2)}


def to_tuple(player: 'Player') -> tuple:
    """
    Преобразует игрока в кортеж (имя, уровень, сила).
    """
    return (player.name, player.level, round(player.calculate_power(), 2))


# ========== 6. ДОКУМЕНТАЦИЯ ==========

__doc__ = """
Модуль strategies.py содержит:
- 5+ стратегий сортировки (by_name, by_level, by_power, by_health, by_name_then_level)
- 5+ функций-фильтров (is_alive_filter, is_high_level_filter, и др.)
- 3 фабрики функций (make_level_filter, make_health_filter, make_power_threshold)
- 3 callable-объекта (DiscountStrategy, HealthRestoreStrategy, PowerBoostStrategy)
- 3 функции для map (to_info_string, extract_name_and_level, to_tuple)
"""