# lab04/collection.py
"""
Коллекция для ЛР-4 (полностью независимая).
"""

from typing import List, Optional, Iterator


class PlayerList:
    """Класс-контейнер для хранения объектов Player."""
    
    def __init__(self):
        self._items = []
    
    def add(self, player) -> None:
        """Добавить игрока."""
        # Проверяем дубликаты по имени
        if self._find_by_name(player.name) is not None:
            raise ValueError(f"Игрок с именем '{player.name}' уже существует")
        
        self._items.append(player)
        print(f"  Добавлен: {player.to_string()}")
    
    def remove(self, player) -> None:
        """Удалить игрока."""
        if player not in self._items:
            raise ValueError(f"Игрок '{player.name}' не найден")
        
        self._items.remove(player)
        print(f"  Удален: {player.name}")
    
    def get_all(self):
        return self._items.copy()
    
    def _find_by_name(self, name: str):
        for player in self._items:
            if player.name.lower() == name.lower():
                return player
        return None
    
    def find_by_name(self, name: str):
        return self._find_by_name(name)
    
    # === Методы для ЛР-4 ===
    
    def get_printable(self):
        """Получить все объекты, реализующие интерфейс Printable."""
        from lab04.interfaces import Printable
        return [p for p in self._items if isinstance(p, Printable)]
    
    def get_comparable(self):
        """Получить все объекты, реализующие интерфейс Comparable."""
        from lab04.interfaces import Comparable
        return [p for p in self._items if isinstance(p, Comparable)]
    
    def get_damageable(self):
        """Получить все объекты, реализующие интерфейс Damageable."""
        from lab04.interfaces import Damageable
        return [p for p in self._items if isinstance(p, Damageable)]
    
    def sort_by_power(self, reverse: bool = True):
        """Сортировка по силе."""
        sorted_list = PlayerList()
        sorted_list._items = self._items.copy()
        sorted_list._items.sort(key=lambda p: p.calculate_power(), reverse=reverse)
        return sorted_list
    
    # === Магические методы ===
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self):
        return iter(self._items)
    
    def __getitem__(self, index: int):
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона")
        return self._items[index]
    
    def __contains__(self, player) -> bool:
        return player in self._items
    
    def __str__(self) -> str:
        if len(self._items) == 0:
            return "PlayerList (пусто)"
        
        result = f"PlayerList ({len(self._items)} игроков):\n"
        for i, player in enumerate(self._items):
            result += f"  [{i}] {player.to_string()}\n"
        return result