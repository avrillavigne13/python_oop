# collection.py
"""
Расширенная коллекция для ЛР-5.
Добавлены методы:
- sort_by(key_func) — сортировка по переданной стратегии
- filter_by(predicate) — фильтрация по переданному условию
- apply(func) — применение функции ко всем элементам
- chain() — поддержка цепочек операций (для оценки 5)
"""

from typing import List, Callable, Optional, Iterator, Any
import copy


class PlayerList:
    """
    Класс-контейнер для хранения объектов Player.
    Расширен для поддержки функций-стратегий.
    """
    
    def __init__(self, items: Optional[List] = None):
        """
        Конструктор.
        
        Аргументы:
            items: начальный список элементов (опционально)
        """
        self._items = items.copy() if items else []
    
    def add(self, player) -> None:
        """Добавить игрока в коллекцию."""
        if self._find_by_name(player.name) is not None:
            raise ValueError(f"Игрок с именем '{player.name}' уже существует")
        
        self._items.append(player)
        print(f"  Добавлен: {player.to_string() if hasattr(player, 'to_string') else player.name}")
    
    def remove(self, player) -> None:
        """Удалить игрока из коллекции."""
        if player not in self._items:
            raise ValueError(f"Игрок '{player.name}' не найден")
        
        self._items.remove(player)
        print(f"  Удален: {player.name}")
    
    def get_all(self) -> List:
        """Получить всех игроков (копию)."""
        return self._items.copy()
    
    def _find_by_name(self, name: str):
        for player in self._items:
            if player.name.lower() == name.lower():
                return player
        return None
    
    def find_by_name(self, name: str):
        return self._find_by_name(name)
    
    # ========== НОВЫЕ МЕТОДЫ ДЛЯ ЛР-5 ==========
    
    # ---------- Сортировка (задание на 3 и 4) ----------
    
    def sort_by(self, key_func: Callable, reverse: bool = False) -> 'PlayerList':
        """
        Сортирует коллекцию по переданной функции-стратегии.
        
        Аргументы:
            key_func: функция, возвращающая значение для сравнения
            reverse: если True, сортировка по убыванию
        
        Возвращает:
            новую отсортированную коллекцию (исходная не меняется)
        
        Пример:
            sorted_players = players.sort_by(by_power, reverse=True)
        """
        sorted_list = PlayerList()
        sorted_list._items = self._items.copy()
        sorted_list._items.sort(key=key_func, reverse=reverse)
        return sorted_list
    
    # ---------- Фильтрация (задание на 3 и 4) ----------
    
    def filter_by(self, predicate: Callable[[Any], bool]) -> 'PlayerList':
        """
        Фильтрует коллекцию по переданной функции-предикату.
        
        Аргументы:
            predicate: функция, возвращающая True/False для каждого элемента
        
        Возвращает:
            новую коллекцию с отфильтрованными элементами
        
        Пример:
            alive_players = players.filter_by(is_alive_filter)
        """
        filtered_list = PlayerList()
        filtered_list._items = [item for item in self._items if predicate(item)]
        return filtered_list
    
    # ---------- Применение функции (задание на 5) ----------
    
    def apply(self, func: Callable[[Any], None]) -> 'PlayerList':
        """
        Применяет функцию ко всем элементам коллекции.
        Функция должна изменять состояние объектов.
        
        Аргументы:
            func: функция, которая принимает элемент и ничего не возвращает
        
        Возвращает:
            ту же коллекцию (для цепочек вызовов)
        
        Пример:
            players.apply(lambda p: p.take_damage(10))
        """
        for item in self._items:
            func(item)
        return self
    
    # ---------- Преобразование (map) (задание на 4) ----------
    
    def map_to(self, transform_func: Callable[[Any], Any]) -> List:
        """
        Преобразует каждый элемент коллекции с помощью функции.
        
        Аргументы:
            transform_func: функция преобразования
        
        Возвращает:
            список результатов преобразования
        
        Пример:
            names = players.map_to(lambda p: p.name)
        """
        return [transform_func(item) for item in self._items]
    
    # ---------- Цепочка операций (задание на 5) ----------
    
    def chain(self) -> 'PlayerList':
        """
        Возвращает ссылку на себя для цепочек вызовов.
        
        Пример:
            result = (collection
                .filter_by(is_alive)
                .sort_by(by_power)
                .apply(apply_damage))
        """
        return self
    
    # ---------- Встроенные операции (для удобства) ----------
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __iter__(self) -> Iterator:
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
            if hasattr(player, 'to_string'):
                result += f"  [{i}] {player.to_string()}\n"
            else:
                result += f"  [{i}] {player.name}\n"
        return result
    
    def __repr__(self) -> str:
        return f"PlayerList({self._items})"