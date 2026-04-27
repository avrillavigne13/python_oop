import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab03'))

from base import Player

from typing import List, Optional, Iterator

class PlayerList:

    def __init__(self):
        # Создаем пустой список, в котором будем хранить всех игроков
        self._items: List[Player] = []
    
    
    def add(self, player: Player) -> None:
        
        # Проверяем, что переданный объект - это игрок (класс Player)
        if not isinstance(player, Player):
            raise TypeError(f"Можно добавлять только объекты Player, получен {type(player).__name__}")
        
        # Проверяем, нет ли уже игрока с таким именем (запрещаем дубликаты)
        if self._find_by_name(player.name) is not None:
            raise ValueError(f"Игрок с именем '{player.name}' уже существует в коллекции")
        
        # Добавляем игрока в конец списка
        self._items.append(player)
        print(f"  Игрок '{player.name}' добавлен в коллекцию")
    
    def remove(self, player: Player) -> None:
        
        # Проверяем, есть ли такой игрок в списке
        if player not in self._items:
            raise ValueError(f"Игрок '{player.name}' не найден в коллекции")
        
        # Удаляем игрока из списка
        self._items.remove(player)
        print(f"  Игрок '{player.name}' удален из коллекции")
    
    def remove_at(self, index: int) -> Player:
       
        # Проверяем, что индекс существует в списке
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0-{len(self._items)-1})")
        
        # Удаляем и возвращаем игрока по индексу
        removed = self._items.pop(index)
        print(f"  Игрок '{removed.name}' удален по индексу {index}")
        return removed
    
    def get_all(self) -> List[Player]:
        
        # Возвращаем копию списка, чтобы нельзя было изменить внутренний список напрямую
        return self._items.copy()
    
    
    def _find_by_name(self, name: str) -> Optional[Player]:
     
        # Перебираем всех игроков и сравниваем имена (без учета регистра)
        for player in self._items:
            if player.name.lower() == name.lower():
                return player
        return None
    
    def find_by_name(self, name: str) -> Optional[Player]:
    
        return self._find_by_name(name)
    
    def find_by_level(self, level: int) -> List[Player]:
    
        # Создаем список, куда будем добавлять подходящих игроков
        result = []
        for player in self._items:
            if player.level == level:
                result.append(player)
        return result
    
    def find_by_title(self, title: str) -> List[Player]:
    
        # Перебираем игроков и проверяем титул
        result = []
        for player in self._items:
            if player.title == title:
                result.append(player)
        return result
    
    def find_alive(self) -> 'PlayerList':
     
        # Создаем новую пустую коллекцию
        alive_list = PlayerList()
        # Добавляем в неё всех живых игроков
        for player in self._items:
            if player.is_alive:
                alive_list.add(player)
        return alive_list
    
    
    def __len__(self) -> int:
   
        return len(self._items)
    
    def __iter__(self) -> Iterator[Player]:
    
        # Возвращаем итератор из внутреннего списка
        return iter(self._items)
    
    def __getitem__(self, index: int) -> Player:
    
        # Проверяем, что индекс правильный
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0-{len(self._items)-1})")
        return self._items[index]
    
    def __contains__(self, player: Player) -> bool:
    
        return player in self._items
    
    def __str__(self) -> str:
    
        if len(self._items) == 0:
            return "PlayerList (пусто)"
        
        result = f"PlayerList ({len(self._items)} игроков):\n"
        for i, player in enumerate(self._items):
            result += f"  [{i}] {player.name} (ур. {player.level}) - {player.title}\n"
        return result
    
    def __repr__(self) -> str:
    
        return f"PlayerList({self._items})"
    
    
    def sort_by_name(self, reverse: bool = False) -> 'PlayerList':
       
        # Создаем новую коллекцию
        sorted_list = PlayerList()
        # Копируем всех игроков
        sorted_list._items = self._items.copy()
        # Сортируем по имени (используем lambda для получения имени)
        sorted_list._items.sort(key=lambda p: p.name, reverse=reverse)
        return sorted_list
    
    def sort_by_level(self, reverse: bool = False) -> 'PlayerList':
       
        sorted_list = PlayerList()
        sorted_list._items = self._items.copy()
        # Сортируем по уровню
        sorted_list._items.sort(key=lambda p: p.level, reverse=reverse)
        return sorted_list
    
    def sort(self, key: str, reverse: bool = False) -> 'PlayerList':
       
        # Список разрешенных атрибутов для сортировки
        allowed_keys = ['name', 'level', 'health', 'experience']
        if key not in allowed_keys:
            raise ValueError(f"Неверный ключ сортировки. Доступно: {allowed_keys}")
        
        sorted_list = PlayerList()
        sorted_list._items = self._items.copy()
        # Сортируем, получая значение атрибута через getattr
        sorted_list._items.sort(key=lambda p: getattr(p, key), reverse=reverse)
        return sorted_list
    
    def get_warriors(self):
        """Получить только воинов."""
        from models import Warrior
        return [p for p in self._items if isinstance(p, Warrior)]

    def get_mages(self):
        """Получить только магов."""
        from models import Mage
        return [p for p in self._items if isinstance(p, Mage)]

    def get_archers(self):
        """Получить только лучников."""
        from models import Archer
        return [p for p in self._items if isinstance(p, Archer)]

    def find_by_type(self, player_type: str):
        """Поиск по типу игрока."""
        return [p for p in self._items if p.get_player_type() == player_type]
    
        # === НОВЫЕ МЕТОДЫ ДЛЯ ЛР-4 (добавить в класс PlayerList) ===
    
    def get_printable(self):
        """Получить все объекты, реализующие интерфейс Printable."""
        try:
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from lab04.interfaces import Printable
            return [p for p in self._items if isinstance(p, Printable)]
        except ImportError:
            return []
    
    def get_comparable(self):
        """Получить все объекты, реализующие интерфейс Comparable."""
        try:
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from lab04.interfaces import Comparable
            return [p for p in self._items if isinstance(p, Comparable)]
        except ImportError:
            return []
    
    def get_damageable(self):
        """Получить все объекты, реализующие интерфейс Damageable."""
        try:
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from lab04.interfaces import Damageable
            return [p for p in self._items if isinstance(p, Damageable)]
        except ImportError:
            return []
    
    def sort_by_power(self, reverse: bool = True):
        """Сортировка по силе (использует calculate_power)."""
        sorted_list = PlayerList()
        sorted_list._items = self._items.copy()
        try:
            sorted_list._items.sort(key=lambda p: p.calculate_power(), reverse=reverse)
        except AttributeError:
            sorted_list._items.sort(key=lambda p: p.level, reverse=reverse)
        return sorted_list