# interfaces.py
"""
Абстрактные классы (интерфейсы) для ЛР-4.
"""

from abc import ABC, abstractmethod
from typing import Any


class Printable(ABC):
    """
    Интерфейс "Печатаемый".
    Требует реализовать метод для получения строкового представления.
    """
    
    @abstractmethod
    def to_string(self) -> str:
        """Возвращает строковое представление объекта."""
        pass


class Comparable(ABC):
    """
    Интерфейс "Сравниваемый".
    Требует реализовать метод для сравнения объектов.
    """
    
    @abstractmethod
    def compare_to(self, other: Any) -> int:
        """
        Сравнивает текущий объект с другим.
        Возвращает: -1 (меньше), 0 (равно), 1 (больше)
        """
        pass


class Damageable(ABC):
    """
    Интерфейс "Получающий урон".
    Требует реализовать методы получения урона и лечения.
    """
    
    @abstractmethod
    def take_damage(self, amount: float) -> str:
        """Получить урон."""
        pass
    
    @abstractmethod
    def heal(self, amount: float) -> str:
        """Вылечиться."""
        pass