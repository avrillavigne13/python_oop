import validate


class Player:
    """
    Класс Игрок (Player) для игровой логики.
    
    Атрибуты класса:
        MAX_LEVEL (int): максимальный уровень
        MIN_LEVEL (int): минимальный уровень
        MAX_HEALTH (float): максимальное здоровье
        EXPERIENCE_PER_LEVEL (int): опыта для повышения уровня
        TITLES (dict): титулы для разных уровней
    
    Атрибуты экземпляра (приватные):
        _name: имя игрока
        _level: уровень (1-10)
        _health: здоровье (0-100)
        _experience: опыт (0 до level * 1000)
        _is_alive: жив ли игрок (вычисляется на основе здоровья)
    """
    
    # Атрибуты класса (для оценки 4+)
    MAX_LEVEL = 10
    MIN_LEVEL = 1
    MAX_HEALTH = 100.0
    EXPERIENCE_PER_LEVEL = 1000  # опыта для повышения уровня
    
    # Титулы в зависимости от уровня (на русском)
    TITLES = {
        (1, 2): "Новичок",
        (3, 4): "Воин",
        (5, 7): "Ветеран",
        (8, 10): "Легенда"
    }
    
    def __init__(self, name: str, level: int = 1, health: float = 100.0, experience: int = 0):
        """
        Конструктор класса Player с валидацией всех параметров.
        
        Аргументы:
            name: имя игрока
            level: начальный уровень (по умолчанию 1)
            health: начальное здоровье (по умолчанию 100)
            experience: начальный опыт (по умолчанию 0)
        """
        # Валидация через вынесенные методы
        self._validate_initialization(name, level, health, experience)
        
        # Присвоение значений приватным атрибутам
        self._name = name.strip()
        self._level = level
        self._health = float(health)
        self._experience = experience
        
        # Вычисляемое состояние - жив ли игрок
        self._update_alive_status()
    
    def _validate_initialization(self, name, level, health, experience):
        """Отдельный метод валидации для конструктора (требование на 5)."""
        validate.validate_string(name, "Имя", min_length=2, max_length=20)
        validate.validate_int(level, "Уровень", self.MIN_LEVEL, self.MAX_LEVEL)
        validate.validate_float(health, "Здоровье", 0.0, self.MAX_HEALTH)
        validate.validate_int(experience, "Опыт", 0, level * self.EXPERIENCE_PER_LEVEL)
    
    def _update_alive_status(self):
        """Обновляет состояние 'жив' на основе здоровья."""
        self._is_alive = self._health > 0
    
    # === Свойства (геттеры) ===
    
    @property
    def name(self) -> str:
        """Имя игрока (только чтение)."""
        return self._name
    
    @property
    def level(self) -> int:
        """Уровень игрока (только чтение)."""
        return self._level
    
    @property
    def health(self) -> float:
        """Текущее здоровье."""
        return self._health
    
    @health.setter
    def health(self, value: float):
        """
        Сеттер для здоровья с валидацией.
        Автоматически обновляет статус alive.
        """
        validate.validate_float(value, "Здоровье", 0.0, self.MAX_HEALTH)
        self._health = value
        self._update_alive_status()
    
    @property
    def experience(self) -> int:
        """Текущий опыт."""
        return self._experience
    
    @experience.setter
    def experience(self, value: int):
        """
        Сеттер для опыта со специальной валидацией.
        При достижении порога может повысить уровень.
        """
        # Проверка, что игрок жив (нельзя получать опыт мертвым)
        if not self._is_alive:
            raise ValueError(f"Нельзя добавить опыт мертвому игроку '{self._name}'")
        
        # Специальная валидация для опыта
        validate.validate_experience(value, self._level)
        self._experience = value
        
        # Логика повышения уровня (поведение, зависящее от состояния)
        while self._experience >= self._level * self.EXPERIENCE_PER_LEVEL and self._level < self.MAX_LEVEL:
            self._level_up()
    
    @property
    def is_alive(self) -> bool:
        """Жив ли игрок (вычисляемое свойство, только чтение)."""
        return self._is_alive
    
    @property
    def title(self) -> str:
        """Титул игрока на основе уровня (вычисляемое свойство)."""
        for (min_lvl, max_lvl), title in self.TITLES.items():
            if min_lvl <= self._level <= max_lvl:
                return title
        return "Загадочный странник"
    
    @property
    def health_percent(self) -> float:
        """Процент здоровья (вычисляемое свойство)."""
        return (self._health / self.MAX_HEALTH) * 100
    
    # === Бизнес-методы ===
    
    def _level_up(self):
        """Внутренний метод повышения уровня."""
        if self._level < self.MAX_LEVEL:
            self._level += 1
            # Восстанавливаем здоровье при повышении уровня
            self._health = self.MAX_HEALTH
            self._update_alive_status()
            print(f"[ПОВЫШЕНИЕ УРОВНЯ] {self._name} достиг уровня {self._level}!")
            print(f"                    Новый титул: {self.title}")
    
    def take_damage(self, damage: float) -> str:
        """
        Метод получения урона.
        
        Аргументы:
            damage: получаемый урон
            
        Returns:
            str: сообщение о результате
        """
        # Проверка на допустимость операции (игрок должен быть жив)
        if not self._is_alive:
            return f"[ОШИБКА] {self._name} уже мертв и не может получить урон"
        
        # Валидация входных данных
        validate.validate_float(damage, "Урон", 0.0, 1000.0)
        
        old_health = self._health
        self._health = max(0.0, self._health - damage)
        self._update_alive_status()
        
        damage_taken = old_health - self._health
        
        if not self._is_alive:
            return f"[СМЕРТЬ] {self._name} получил {damage_taken:.1f} урона и ПОГИБ!"
        else:
            return f"[УРОН] {self._name} получил {damage_taken:.1f} урона. Здоровье: {self._health:.1f} ({self.health_percent:.0f}%)"
    
    def heal(self, amount: float) -> str:
        """
        Метод лечения.
        
        Аргументы:
            amount: количество лечения
            
        Returns:
            str: сообщение о результате
        """
        # Проверка на допустимость операции (игрок должен быть жив)
        if not self._is_alive:
            return f"[ОШИБКА] Нельзя лечить мертвого игрока '{self._name}'"
        
        validate.validate_float(amount, "Лечение", 0.0, self.MAX_HEALTH)
        
        old_health = self._health
        self._health = min(self.MAX_HEALTH, self._health + amount)
        self._update_alive_status()
        
        healed = self._health - old_health
        return f"[ЛЕЧЕНИЕ] {self._name} вылечил {healed:.1f} здоровья. Текущее здоровье: {self._health:.1f} ({self.health_percent:.0f}%)"
    
    def add_experience(self, amount: int) -> str:
        """
        Добавление опыта (может вызвать повышение уровня).
        
        Аргументы:
            amount: получаемый опыт
        """
        validate.validate_int(amount, "Количество опыта", 0, 10000)
        
        # Проверка на состояние
        if not self._is_alive:
            return f"[ОШИБКА] Мертвый игрок '{self._name}' не может получать опыт"
        
        old_exp = self._experience
        old_level = self._level
        
        try:
            self.experience = self._experience + amount  # Используем сеттер для логики повышения уровня
        except ValueError as e:
            return f"[ОШИБКА] {e}"
        
        if self._level > old_level:
            return f"[ОПЫТ] {self._name} получил {amount} опыта и ПОВЫСИЛ УРОВЕНЬ! Текущий опыт: {self._experience}"
        else:
            return f"[ОПЫТ] {self._name} получил {amount} опыта. Текущий опыт: {self._experience}"
    
    def revive(self) -> str:
        """
        Воскрешение игрока (изменение состояния).
        """
        if self._is_alive:
            return f"[ОШИБКА] {self._name} уже жив"
        
        self._health = self.MAX_HEALTH / 2  # Воскрешаем с половинным здоровьем
        self._update_alive_status()
        return f"[ВОСКРЕШЕНИЕ] {self._name} воскрешен! Здоровье: {self._health:.1f} ({self.health_percent:.0f}%)"
    
    # === Магические методы ===
    
    def __str__(self) -> str:
        """
        Красивое строковое представление для пользователей.
        Требование для оценки 3.
        """
        status = "ЖИВ" if self._is_alive else "МЕРТВ"
        health_bar = self._get_health_bar()
        
        return (f"Игрок: {self._name} [{self.title}] (Ур. {self._level})\n"
                f"  {health_bar} {self._health:.1f}/{self.MAX_HEALTH}\n"
                f"  Опыт: {self._experience}/{self._level * self.EXPERIENCE_PER_LEVEL}\n"
                f"  Статус: {status}")
    
    def _get_health_bar(self, length: int = 20) -> str:
        """Вспомогательный метод для создания полоски здоровья."""
        filled = int((self._health / self.MAX_HEALTH) * length)
        bar = "█" * filled + "░" * (length - filled)
        
        if self._health > 60:
            marker = "+"  # Высокое здоровье
        elif self._health > 30:
            marker = "~"  # Среднее здоровье
        elif self._health > 0:
            marker = "-"  # Низкое здоровье
        else:
            marker = "x"  # Мертв
        
        return f"[{marker}] [{bar}]"
    
    def __repr__(self) -> str:
        """
        Официальное представление для разработчиков.
        Требование для оценки 4.
        """
        return (f"Player(name='{self._name}', level={self._level}, "
                f"health={self._health:.1f}, exp={self._experience})")
    
    def __eq__(self, other) -> bool:
        """
        Сравнение игроков по имени.
        Требование для оценки 3.
        """
        if not isinstance(other, Player):
            return False
        return self._name == other._name
    
    def __lt__(self, other) -> bool:
        """
        Сравнение для сортировки (по уровню, затем по имени).
        """
        if not isinstance(other, Player):
            return NotImplemented
        
        if self._level != other._level:
            return self._level < other._level
        return self._name < other._name