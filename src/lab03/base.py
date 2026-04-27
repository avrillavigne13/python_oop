import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))

import validate

class Player:

    MAX_LEVEL = 10
    MIN_LEVEL = 1
    MAX_HEALTH = 100.0
    EXPERIENCE_PER_LEVEL = 1000
    
    TITLES = {
        (1, 2): "Новичок",
        (3, 4): "Воин",
        (5, 7): "Ветеран",
        (8, 10): "Легенда"
    }
    
    def __init__(self, name: str, level: int = 1, health: float = 100.0, experience: int = 0):
        self._validate_initialization(name, level, health, experience)
        
        self._name = name.strip()
        self._level = level
        self._health = float(health)
        self._experience = experience
        
        self._update_alive_status()
    
    def _validate_initialization(self, name, level, health, experience):
        validate.validate_string(name, "Имя", min_length=2, max_length=20)
        validate.validate_int(level, "Уровень", self.MIN_LEVEL, self.MAX_LEVEL)
        validate.validate_float(health, "Здоровье", 0.0, self.MAX_HEALTH)
        validate.validate_experience(experience, level)
    
    def _update_alive_status(self):
        self._is_alive = self._health > 0
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def level(self) -> int:
        return self._level
    
    @property
    def health(self) -> float:
        return self._health
    
    @health.setter
    def health(self, value: float):
        validate.validate_float(value, "Здоровье", 0.0, self.MAX_HEALTH)
        self._health = value
        self._update_alive_status()
    
    @property
    def experience(self) -> int:
        return self._experience
    
    @experience.setter
    def experience(self, value: int):
        if not self._is_alive:
            raise ValueError(f"Нельзя изменить опыт мертвому игроку '{self._name}'")
        
        if value < 0:
            raise ValueError(f"Опыт не может быть отрицательным: {value}")
        
        self._experience = value
        self._check_level_up()
    
    def _check_level_up(self):
        while self._experience >= self._level * self.EXPERIENCE_PER_LEVEL and self._level < self.MAX_LEVEL:
            self._level_up()
    
    def _level_up(self):
        if self._level < self.MAX_LEVEL:
            needed = self._level * self.EXPERIENCE_PER_LEVEL
            self._experience -= needed
            self._level += 1
            self._health = self.MAX_HEALTH
            self._update_alive_status()
            print(f"[ПОВЫШЕНИЕ УРОВНЯ] {self._name} достиг уровня {self._level}!")
    
    @property
    def is_alive(self) -> bool:
        return self._is_alive
    
    @property
    def title(self) -> str:
        for (min_lvl, max_lvl), title in self.TITLES.items():
            if min_lvl <= self._level <= max_lvl:
                return title
        return "Загадочный странник"
    
    @property
    def health_percent(self) -> float:
        return (self._health / self.MAX_HEALTH) * 100
    
    def take_damage(self, damage: float) -> str:
        if not self._is_alive:
            return f"[ОШИБКА] {self._name} уже мертв"
        
        validate.validate_float(damage, "Урон", 0.0, 1000.0)
        
        old_health = self._health
        self._health = max(0.0, self._health - damage)
        self._update_alive_status()
        
        damage_taken = old_health - self._health
        
        if not self._is_alive:
            return f"[СМЕРТЬ] {self._name} получил {damage_taken:.1f} урона и ПОГИБ!"
        else:
            return f"[УРОН] {self._name} получил {damage_taken:.1f} урона. Здоровье: {self._health:.1f}"
    
    def heal(self, amount: float) -> str:
        if not self._is_alive:
            return f"[ОШИБКА] Нельзя лечить мертвого игрока '{self._name}'"
        
        validate.validate_float(amount, "Лечение", 0.0, self.MAX_HEALTH)
        
        old_health = self._health
        self._health = min(self.MAX_HEALTH, self._health + amount)
        self._update_alive_status()
        
        healed = self._health - old_health
        return f"[ЛЕЧЕНИЕ] {self._name} вылечил {healed:.1f} здоровья"
    
    def add_experience(self, amount: int) -> str:
        validate.validate_int(amount, "Количество опыта", 0, 10000)
        
        if not self._is_alive:
            return f"[ОШИБКА] Мертвый игрок '{self._name}' не может получать опыт"
        
        old_level = self._level
        self._experience += amount
        self._check_level_up()
        
        if self._level > old_level:
            return f"[ОПЫТ] {self._name} получил {amount} опыта и ПОВЫСИЛ УРОВЕНЬ до {self._level}!"
        else:
            needed = self._level * self.EXPERIENCE_PER_LEVEL - self._experience
            return f"[ОПЫТ] {self._name} получил {amount} опыта. До уровня: {needed}"
    
    def revive(self) -> str:
        if self._is_alive:
            return f"[ОШИБКА] {self._name} уже жив"
        
        self._health = self.MAX_HEALTH / 2
        self._update_alive_status()
        return f"[ВОСКРЕШЕНИЕ] {self._name} воскрешен! Здоровье: {self._health:.1f}"
    
    # ПОЛИМОРФИЗМ
    
    def get_player_type(self) -> str:
        """Возвращает тип игрока. Будет переопределён в дочерних классах."""
        return "Обычный игрок"
    
    def calculate_power(self) -> float:
        return round(self._level * (self._health / self.MAX_HEALTH), 2)
    
    # МАГИЧЕСКИЕ МЕТОДЫ
    
    def __str__(self) -> str:
        status = "ЖИВ" if self._is_alive else "МЕРТВ"
        return f"[{self.get_player_type()}] {self._name} | Ур.{self._level} | Здоровье: {self._health:.0f} | {status}"
    
    def __repr__(self) -> str:
        return (f"Player(name='{self._name}', level={self._level}, "
                f"health={self._health:.1f}, exp={self._experience})")
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return self._name == other._name
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        if self._level != other._level:
            return self._level < other._level
        return self._name < other._name