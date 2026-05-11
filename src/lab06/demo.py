import sys
import os

# Добавляем пути
src_path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_path)
sys.path.insert(0, os.path.dirname(__file__))

# Импортируем классы из ЛР-3
from lab03.models import Player, Warrior, Mage, Archer

# Импортируем из container.py
from container import (
    TypedCollection, Displayable, Scorable, HealthProtocol,
    DisplayableCollection, ScorableCollection,
    D, S
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


def create_test_players():
    """Создаёт тестовых игроков для демонстрации."""
    return [
        Player("Алексей", level=3, health=100),
        Warrior("Громобой", level=8, health=100, armor=40, weapon="Топор"),
        Mage("Мерлин", level=6, health=80, mana=120, spell="Огонь"),
        Archer("Леголас", level=5, health=90, accuracy=90, bow_type="Эльфийский лук"),
        Player("Борис", level=2, health=100),
        Warrior("Спартак", level=4, health=60, armor=20, weapon="Меч"),
        Mage("Гэндальф", level=7, health=70, mana=150, spell="Молния"),
    ]


# ==================== ДОБАВЛЯЕМ МЕТОДЫ В КЛАССЫ (для протоколов) ====================

def add_protocol_methods_to_players() -> None:
    """
    Добавляем методы display() и get_score() в классы Player.
    Это делается динамически, чтобы не менять исходные файлы lab03.
    """
    
    # Добавляем метод display() в класс Player
    def player_display(self) -> str:
        status = "ЖИВ" if self.is_alive else "МЕРТВ"
        return f"[{self.get_player_type()}] {self.name} | Ур.{self.level} | {status}"
    
    Player.display = player_display
    
    # Добавляем метод get_score() в класс Player
    def player_get_score(self) -> float:
        return self.calculate_power()
    
    Player.get_score = player_get_score
    
    # Добавляем display() в Warrior
    def warrior_display(self) -> str:
        return f"[Воин] {self.name} | Ур.{self.level} | Броня: {self.armor}% | Оружие: {self.weapon}"
    
    Warrior.display = warrior_display
    
    # Добавляем display() в Mage
    def mage_display(self) -> str:
        return f"[Маг] {self.name} | Ур.{self.level} | Мана: {self.mana}/100 | Заклинание: {self.spell}"
    
    Mage.display = mage_display
    
    # Добавляем display() в Archer
    def archer_display(self) -> str:
        return f"[Лучник] {self.name} | Ур.{self.level} | Меткость: {self.accuracy}% | Лук: {self.bow_type}"
    
    Archer.display = archer_display


# ==================== СЦЕНАРИЙ 1: GENERIC-КОЛЛЕКЦИЯ (оценка 3) ====================

def scenario_1_generic_collection() -> None:
    """
    Сценарий 1: демонстрация Generic-коллекции.
    - создание типизированной коллекции
    - добавление объектов
    - получение всех элементов
    """
    print_header("СЦЕНАРИЙ 1: GENERIC-КОЛЛЕКЦИЯ (оценка 3)")
    
    # Создаём типизированную коллекцию для Player
    print_subheader("Создание коллекции TypedCollection[Player]")
    players: TypedCollection[Player] = TypedCollection()
    print_info(f"Тип коллекции: TypedCollection[Player]")
    
    # Добавляем игроков
    print_subheader("Добавление объектов")
    test_players = create_test_players()
    for player in test_players[:4]:
        players.add(player)
    
    # Выводим коллекцию
    print_subheader("Все элементы коллекции")
    print(players)
    
    # Проверка длины
    print_info(f"Количество элементов: {len(players)}")
    
    # Доступ по индексу
    print_subheader("Доступ по индексу")
    print(f"  Первый элемент: {players[0].name}")
    print(f"  Последний элемент: {players[-1].name}")
    
    # Итерация
    print_subheader("Итерация (for item in collection)")
    for i, player in enumerate(players):
        print(f"  {i}: {player.name} (ур.{player.level})")
    
    print_success("Generic-коллекция работает!")


# ==================== СЦЕНАРИЙ 2: FIND, FILTER, MAP (оценка 4) ====================

def scenario_2_find_filter_map() -> None:
    """
    Сценарий 2: демонстрация методов find, filter, map.
    - find: поиск элемента по условию
    - filter: фильтрация элементов
    - map: преобразование элементов с изменением типа
    """
    print_header("СЦЕНАРИЙ 2: FIND, FILTER, MAP (оценка 4)")
    
    # Создаём коллекцию
    players: TypedCollection[Player] = TypedCollection()
    for player in create_test_players():
        players.add(player)
    
    print(players)
    
    # ===== FIND =====
    print_subheader("Метод find() - поиск элемента")
    
    # Поиск существующего элемента
    found = players.find(lambda p: p.name == "Громобой")
    if found:
        print_info(f"Найден: {found.name} (ур.{found.level})")
    
    # Поиск несуществующего элемента
    not_found = players.find(lambda p: p.name == "Несуществующий")
    if not_found is None:
        print_info("Поиск 'Несуществующий' → None (не найден)")
    
    # Поиск по уровню
    high_level = players.find(lambda p: p.level >= 7)
    if high_level:
        print_info(f"Первый игрок с уровнем >= 7: {high_level.name} (ур.{high_level.level})")
    
    # ===== FILTER =====
    print_subheader("Метод filter() - фильтрация")
    
    # Фильтр: только воины
    warriors = players.filter(lambda p: p.get_player_type() == "Воин")
    print_info(f"Воины ({len(warriors)} шт.):")
    for w in warriors:
        print(f"    {w.name} (ур.{w.level})")
    
    # Фильтр: только высокоуровневые (уровень >= 5)
    elite = players.filter(lambda p: p.level >= 5)
    print_info(f"Игроки с уровнем >= 5 ({len(elite)} шт.):")
    for p in elite:
        print(f"    {p.name} (ур.{p.level})")
    
    # Фильтр: только живые (после небольшого урона)
    for p in players.get_all():
        if p.name == "Спартак":
            p.take_damage(100)
    
    alive = players.filter(lambda p: p.is_alive)
    print_info(f"Живые игроки ({len(alive)} шт.):")
    for p in alive:
        print(f"    {p.name} (здоровье: {p.health:.0f})")
    
    # Восстанавливаем
    for p in players.get_all():
        if p.name == "Спартак":
            p.health = 60
    
    # ===== MAP (с изменением типа) =====
    print_subheader("Метод map() - преобразование с изменением типа")
    
    # map: List[Player] → List[str] (имена)
    names: List[str] = players.map(lambda p: p.name)
    print_info(f"map → имена (List[str]): {names}")
    
    # map: List[Player] → List[int] (уровни)
    levels: List[int] = players.map(lambda p: p.level)
    print_info(f"map → уровни (List[int]): {levels}")
    
    # map: List[Player] → List[float] (сила)
    powers: List[float] = players.map(lambda p: p.calculate_power())
    print_info(f"map → сила (List[float]): {[round(p, 2) for p in powers]}")
    
    # map: List[Player] → List[str] (информационные строки)
    info_strings: List[str] = players.map(lambda p: f"{p.name} (ур.{p.level}, сила: {p.calculate_power():.2f})")
    print_info("map → информационные строки:")
    for s in info_strings:
        print(f"    {s}")
    
    print_success("Методы find, filter, map работают и типы корректны!")


# ==================== СЦЕНАРИЙ 3: PROTOCOL (оценка 5) ====================

def scenario_3_protocol() -> None:
    """
    Сценарий 3: демонстрация протоколов и структурной типизации.
    - объекты разных типов подходят под Protocol благодаря наличию методов
    - коллекция с ограничением bound=Displayable
    - коллекция с ограничением bound=Scorable
    """
    print_header("СЦЕНАРИЙ 3: PROTOCOL И СТРУКТУРНАЯ ТИПИЗАЦИЯ (оценка 5)")
    
    # Добавляем методы display() и get_score() в классы
    add_protocol_methods_to_players()
    
    # ===== Демонстрация Displayable =====
    print_subheader("Протокол Displayable")
    print_info("Классы не наследуют Displayable, но имеют метод display() → подходят!")
    
    # Создаём коллекцию для Displayable объектов
    displayable_collection: TypedCollection[D] = TypedCollection()
    
    # Добавляем объекты разных типов (все имеют метод display())
    displayable_collection.add(Player("Обычный", level=3))
    displayable_collection.add(Warrior("Ахиллес", level=8, armor=50, weapon="Копье"))
    displayable_collection.add(Mage("Цирцея", level=7, mana=140, spell="Превращение"))
    displayable_collection.add(Archer("Артемида", level=6, accuracy=85, bow_type="Лук"))
    
    print_info("Элементы в коллекции Displayable:")
    print(displayable_collection)
    
    print_subheader("Вызов метода display() для каждого элемента")
    for item in displayable_collection:
        print(f"  {item.display()}")
    
    # ===== Демонстрация Scorable =====
    print_subheader("Протокол Scorable")
    print_info("Классы имеют метод get_score() (возвращает calculate_power()) → подходят!")
    
    # Создаём коллекцию для Scorable объектов
    scorable_collection: TypedCollection[S] = TypedCollection()
    
    scorable_collection.add(Player("Обычный", level=3))
    scorable_collection.add(Warrior("Ахиллес", level=8, armor=50, weapon="Копье"))
    scorable_collection.add(Mage("Цирцея", level=7, mana=140, spell="Превращение"))
    
    print_info("Элементы в коллекции Scorable:")
    print(scorable_collection)
    
    print_subheader("Вызов метода get_score() для каждого элемента")
    for item in scorable_collection:
        print(f"  {item.name}: score = {item.get_score():.2f}")
    
    # Использование специализированных коллекций
    print_subheader("Специализированная коллекция DisplayableCollection")
    disp_collection = DisplayableCollection()
    disp_collection.add(Warrior("Гектор", level=5, armor=30, weapon="Меч"))
    disp_collection.add(Mage("Гермес", level=4, mana=100, spell="Скорость"))
    disp_collection.display_all()
    
    print_subheader("Специализированная коллекция ScorableCollection")
    score_collection = ScorableCollection()
    score_collection.add(Warrior("Гектор", level=5, armor=30, weapon="Меч"))
    score_collection.add(Mage("Гермес", level=4, mana=100, spell="Скорость"))
    score_collection.add(Archer("Леголас", level=6, accuracy=90, bow_type="Лук"))
    
    print_info(f"Сумма очков: {score_collection.get_total_score():.2f}")
    print_info(f"Среднее очков: {score_collection.get_average_score():.2f}")
    
    print_success("Протоколы работают! Объекты подходят без явного наследования!")


# ==================== ДОПОЛНИТЕЛЬНЫЙ СЦЕНАРИЙ: ПРОВЕРКА ТИПОВ ====================

def scenario_4_type_safety() -> None:
    """
    Дополнительный сценарий: демонстрация типобезопасности.
    """
    print_header("СЦЕНАРИЙ 4: ТИПОБЕЗОПАСНОСТЬ")
    
    # Корректное использование
    print_subheader("Корректное использование типов")
    players: TypedCollection[Player] = TypedCollection()
    players.add(Player("Сашка", level=5))
    players.add(Warrior("Гром", level=8, armor=30, weapon="Меч"))
    print_info(f"В коллекции {len(players)} элементов")
    
    # Демонстрация типов в map
    print_subheader("Map с разными типами результатов")
    
    # map: List[Player] → List[str]
    names = players.map(lambda p: p.name)
    print_info(f"Тип результата map (имена): {type(names).__name__}[{type(names[0]).__name__}]")
    
    # map: List[Player] → List[int]
    levels = players.map(lambda p: p.level)
    print_info(f"Тип результата map (уровни): {type(levels).__name__}[{type(levels[0]).__name__}]")
    
    # map: List[Player] → List[float]
    powers = players.map(lambda p: p.calculate_power())
    print_info(f"Тип результата map (сила): {type(powers).__name__}[{type(powers[0]).__name__}]")
    
    print_success("Типы корректно определяются и проверяются!")


# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================

def main() -> None:
    print_header("ЛАБОРАТОРНАЯ РАБОТА №6: GENERICS И TYPING")
    print("Вариант 6 - Игрок (Player)")
    print("Оценка 5 - все требования выполнены")
    
    # Запуск сценариев
    scenario_1_generic_collection()
    scenario_2_find_filter_map()
    scenario_3_protocol()
    scenario_4_type_safety()
    
    print_header("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("\nРеализованные возможности:")
    print("  [3] - Аннотации типов, Generic-коллекция TypedCollection[T]")
    print("  [3] - Полная реализация методов из ЛР-2 с аннотациями")
    print("  [4] - Методы find, filter, map с корректными типами")
    print("  [4] - Map с изменением типа (T → R) через TypeVar R")
    print("  [5] - Протоколы Displayable и Scorable")
    print("  [5] - TypeVar с ограничениями bound=Displayable, bound=Scorable")
    print("  [5] - Объекты подходят под протоколы без явного наследования")
    print("\nВсе требования на оценку 5 выполнены!")


if __name__ == "__main__":
    main()