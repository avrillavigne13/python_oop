from typing import TypeVar, Generic, Callable, Optional, List, Protocol, Any

# ========== 1. TypeVar для Generic-коллекции ==========

T = TypeVar('T')
"""TypeVar для элементов коллекции. Может быть любым типом."""

R = TypeVar('R')
"""TypeVar для результата map-преобразования. Может отличаться от T."""



class TypedCollection(Generic[T]):
    """
    Обобщённая (generic) коллекция для хранения объектов одного типа.
    
    Пример использования:
        players: TypedCollection[Player] = TypedCollection()
        players.add(Player("Сашка"))
        players.add(Warrior("Гром"))
    
    Тип элементов фиксируется при создании коллекции.
    """
    
    def __init__(self) -> None:
        """Конструктор. Создаёт пустую коллекцию."""
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        """
        Добавить элемент в коллекцию.
        
        Аргументы:
            item: элемент типа T
        """
        # Проверка на дубликаты по имени (для Player)
        if hasattr(item, 'name') and self._find_by_name(item.name) is not None:
            raise ValueError(f"Элемент с именем '{item.name}' уже существует")
        
        self._items.append(item)
        print(f"  Добавлен: {self._get_display_str(item)}")
    
    def remove(self, item: T) -> None:
        """
        Удалить элемент из коллекции.
        
        Аргументы:
            item: элемент типа T для удаления
        """
        if item not in self._items:
            raise ValueError(f"Элемент не найден")
        
        self._items.remove(item)
        print(f"  Удален: {self._get_display_str(item)}")
    
    def remove_at(self, index: int) -> T:
        """
        Удалить элемент по индексу.
        
        Аргументы:
            index: индекс элемента для удаления
        
        Возвращает:
            удалённый элемент
        """
        if index < 0 or index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0-{len(self._items)-1})")
        
        removed = self._items.pop(index)
        print(f"  Удален по индексу {index}: {self._get_display_str(removed)}")
        return removed
    
    def get_all(self) -> List[T]:
        """
        Получить все элементы коллекции.
        
        Возвращает:
            копию списка всех элементов
        """
        return self._items.copy()
    
    def _find_by_name(self, name: str) -> Optional[T]:
        """Внутренний метод поиска по имени (для объектов с атрибутом name)."""
        for item in self._items:
            if hasattr(item, 'name') and item.name.lower() == name.lower():
                return item
        return None
    
    def find_by_name(self, name: str) -> Optional[T]:
        """
        Найти элемент по имени.
        
        Аргументы:
            name: имя для поиска
        
        Возвращает:
            найденный элемент или None
        """
        return self._find_by_name(name)
    
    def _get_display_str(self, item: T) -> str:
        """Вспомогательный метод для получения строки для вывода."""
        if hasattr(item, 'to_string'):
            return item.to_string()
        elif hasattr(item, 'name'):
            return str(item.name)
        else:
            return str(item)
    
    
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Найти первый элемент, удовлетворяющий условию.
        
        Аргументы:
            predicate: функция, принимающая элемент и возвращающая bool
        
        Возвращает:
            первый подходящий элемент или None
        
        Пример:
            player = players.find(lambda p: p.level > 5)
        """
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        Получить все элементы, удовлетворяющие условию.
        
        Аргументы:
            predicate: функция, принимающая элемент и возвращающая bool
        
        Возвращает:
            список подходящих элементов
        
        Пример:
            high_level = players.filter(lambda p: p.level >= 5)
        """
        return [item for item in self._items if predicate(item)]
    
    def map(self, transform: Callable[[T], R]) -> List[R]:
        """
        Применить функцию преобразования ко всем элементам.
        
        Аргументы:
            transform: функция, преобразующая T в R
        
        Возвращает:
            список результатов преобразования
        
        Примеры:
            names = players.map(lambda p: p.name)  # List[str]
            powers = players.map(lambda p: p.calculate_power())  # List[float]
        """
        return [transform(item) for item in self._items]
    
    # ========== 4. Методы для сортировки и фильтрации ==========
    
    def sort_by(self, key_func: Callable[[T], Any], reverse: bool = False) -> 'TypedCollection[T]':
        """
        Сортировка по переданной функции-ключу.
        
        Аргументы:
            key_func: функция, возвращающая значение для сравнения
            reverse: если True, сортировка по убыванию
        
        Возвращает:
            новую отсортированную коллекцию
        """
        sorted_collection = TypedCollection[T]()
        sorted_collection._items = self._items.copy()
        sorted_collection._items.sort(key=key_func, reverse=reverse)
        return sorted_collection
    
    # ========== 5. Магические методы ==========
    
    def __len__(self) -> int:
        """Возвращает количество элементов."""
        return len(self._items)
    
    def __iter__(self):
        """Позволяет перебирать элементы в цикле for."""
        return iter(self._items)
    
    def __getitem__(self, index: int) -> T:
        """
        Доступ по индексу. Поддерживает отрицательные индексы (-1 = последний).
        
        Аргументы:
            index: индекс элемента (может быть отрицательным)
        
        Возвращает:
            элемент по указанному индексу
        """
        # Преобразуем отрицательный индекс в положительный
        actual_index = index if index >= 0 else len(self._items) + index
        
        if actual_index < 0 or actual_index >= len(self._items):
            raise IndexError(f"Индекс {index} вне диапазона (0-{len(self._items)-1})")
        
        return self._items[actual_index]
    
    def __contains__(self, item: T) -> bool:
        """Проверка наличия элемента."""
        return item in self._items
    
    def __str__(self) -> str:
        """Строковое представление коллекции."""
        if len(self._items) == 0:
            return f"TypedCollection[{self._get_type_name()}] (пусто)"
        
        result = f"TypedCollection[{self._get_type_name()}] ({len(self._items)} элементов):\n"
        for i, item in enumerate(self._items):
            result += f"  [{i}] {self._get_display_str(item)}\n"
        return result
    
    def _get_type_name(self) -> str:
        """Возвращает имя типа элементов."""
        if self._items:
            return type(self._items[0]).__name__
        return "T"




class Displayable(Protocol):
    """
    Протокол "Отображаемый".
    Объект должен иметь метод display(), возвращающий строку.
    
    Классы не обязаны наследовать этот протокол!
    Достаточно, что у них есть метод с правильной сигнатурой.
    """
    def display(self) -> str:
        ...


class Scorable(Protocol):
    """
    Протокол "Оцениваемый".
    Объект должен иметь метод get_score(), возвращающий число (float).
    
    Классы не обязаны наследовать этот протокол!
    """
    def get_score(self) -> float:
        ...


class HealthProtocol(Protocol):
    """
    Протокол "Имеющий здоровье".
    Объект должен иметь атрибуты health и is_alive.
    """
    @property
    def health(self) -> float:
        ...
    
    @property
    def is_alive(self) -> bool:
        ...


# ========== 7. TypeVar с ограничениями (bound) для протоколов ==========

D = TypeVar('D', bound=Displayable)
"""
TypeVar для коллекций, которые могут содержать только Displayable объекты.
Используется с bound=Displayable.
"""

S = TypeVar('S', bound=Scorable)
"""
TypeVar для коллекций, которые могут содержать только Scorable объекты.
Используется с bound=Scorable.
"""

H = TypeVar('H', bound=HealthProtocol)
"""
TypeVar для коллекций, которые могут содержать только объекты со здоровьем.
"""


# ========== 8. Специализированные типы коллекций для протоколов ==========

class DisplayableCollection(TypedCollection[D]):
    """
    Специализированная коллекция для Displayable объектов.
    Может содержать только объекты, у которых есть метод display().
    
    Пример:
        # Классы Warrior, Mage, Archer имеют метод display()?
        # Если да - они подходят!
        collection: DisplayableCollection = DisplayableCollection()
    """
    
    def display_all(self) -> None:
        """Вывести все объекты через их метод display()."""
        print("Вывод всех объектов (через display()):")
        for item in self._items:
            print(f"  {item.display()}")


class ScorableCollection(TypedCollection[S]):
    """
    Специализированная коллекция для Scorable объектов.
    Может содержать только объекты, у которых есть метод get_score().
    """
    
    def get_total_score(self) -> float:
        """Получить сумму всех очков."""
        return sum(item.get_score() for item in self._items)
    
    def get_average_score(self) -> float:
        """Получить среднее арифметическое очков."""
        if len(self._items) == 0:
            return 0.0
        return self.get_total_score() / len(self._items)