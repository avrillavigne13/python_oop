import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from base import Player 


class Warrior(Player):
    """Воин - наследник Player."""
    
    def __init__(self, name: str, level: int = 1, health: float = 100.0,
                 experience: int = 0, armor: int = 5, weapon: str = "Меч"):
        
        super().__init__(name, level, health, experience)
        
        self._armor = armor
        self._weapon = weapon
    
    @property
    def armor(self) -> int:
        return self._armor
    
    @property
    def weapon(self) -> str:
        return self._weapon
    
    def take_damage(self, damage: float) -> str:
        """Броня уменьшает урон."""
        if not self._is_alive:
            return f"[ОШИБКА] {self._name} уже мертв"
        
        reduced_damage = damage * (1 - self._armor / 100)
        return super().take_damage(reduced_damage)
    
    def power_attack(self) -> str:
        """Сильная атака воина."""
        if not self._is_alive:
            return f"{self._name} мертв"
        
        damage = 20 + self._level * 2
        return f"[СИЛЬНАЯ АТАКА] {self._name} использует {self._weapon} и наносит {damage} урона!"
    
    def get_player_type(self) -> str:
        return "Воин"
    
    def calculate_power(self) -> float:
        return round(super().calculate_power() * (1 + self._armor / 100), 2)
    
    def __str__(self) -> str:
        return f"[Воин] {self._name} | Ур.{self._level} | Здоровье: {self._health:.0f} | Броня: {self._armor}% | Оружие: {self._weapon}"


class Mage(Player):
    """Маг - наследник Player."""
    
    def __init__(self, name: str, level: int = 1, health: float = 100.0,
                 experience: int = 0, mana: int = 100, spell: str = "Огненный шар"):
        
        super().__init__(name, level, health, experience)
        
        self._mana = mana
        self._spell = spell
        self._max_mana = 100
    
    @property
    def mana(self) -> int:
        return self._mana
    
    @property
    def spell(self) -> str:
        return self._spell
    
    def add_experience(self, amount: int) -> str:
        """Маг получает на 20% больше опыта."""
        bonus_amount = int(amount * 1.2)
        return super().add_experience(bonus_amount)
    
    def cast_spell(self) -> str:
        """Заклинание мага."""
        if not self._is_alive:
            return f"{self._name} мертв"
        
        if self._mana < 20:
            return f"{self._name} не хватает маны!"
        
        self._mana -= 20
        damage = 15 + self._level * 3
        return f"[ЗАКЛИНАНИЕ] {self._name} использует {self._spell} и наносит {damage} урона! (Мана: {self._mana})"
    
    def restore_mana(self, amount: int) -> str:
        """Восстановление маны."""
        if not self._is_alive:
            return f"{self._name} мертв"
        
        old_mana = self._mana
        self._mana = min(self._max_mana, self._mana + amount)
        return f"[МАНА] {self._name} восстановил {self._mana - old_mana} маны. Мана: {self._mana}/{self._max_mana}"
    
    def get_player_type(self) -> str:
        return "Маг"
    
    def calculate_power(self) -> float:
        return round(super().calculate_power() * (1 + self._mana / 100 * 0.3), 2)
    
    def __str__(self) -> str:
        return f"[Маг] {self._name} | Ур.{self._level} | Здоровье: {self._health:.0f} | Мана: {self._mana}/{self._max_mana} | Заклинание: {self._spell}"


class Archer(Player):
    """Лучник - наследник Player."""
    
    def __init__(self, name: str, level: int = 1, health: float = 100.0,
                 experience: int = 0, accuracy: int = 80, bow_type: str = "Длинный лук"):
        
        super().__init__(name, level, health, experience)
        
        self._accuracy = accuracy
        self._bow_type = bow_type
    
    @property
    def accuracy(self) -> int:
        return self._accuracy
    
    @property
    def bow_type(self) -> str:
        return self._bow_type
    
    def critical_shot(self) -> str:
        """Критический выстрел (зависит от меткости)."""
        if not self._is_alive:
            return f"{self._name} мертв"
        
        import random
        if random.randint(1, 100) <= self._accuracy:
            damage = 30 + self._level * 2
            return f"[КРИТИЧЕСКИЙ ВЫСТРЕЛ] {self._name} наносит {damage} урона!"
        else:
            return f"[ПРОМАХ] {self._name} промахивается!"
    
    def get_player_type(self) -> str:
        return "Лучник"
    
    def calculate_power(self) -> float:
        return round(super().calculate_power() * (1 + self._accuracy / 100 * 0.2), 2)
    
    def __str__(self) -> str:
        return f"[Лучник] {self._name} | Ур.{self._level} | Здоровье: {self._health:.0f} | Меткость: {self._accuracy}% | Лук: {self._bow_type}"