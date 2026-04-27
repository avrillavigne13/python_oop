# lab04/models.py
import sys
import os

src_path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, src_path)

from lab04.interfaces import Printable, Comparable, Damageable
from lab03.base import Player as BasePlayer
from lab03.models import Warrior as BaseWarrior
from lab03.models import Mage as BaseMage
from lab03.models import Archer as BaseArcher


class Player(BasePlayer, Printable, Comparable, Damageable):
    def to_string(self) -> str:
        status = "ЖИВ" if self._is_alive else "МЕРТВ"
        return f"[{self.get_player_type()}] {self._name} | Ур.{self._level} | {status}"
    
    def compare_to(self, other) -> int:
        if not isinstance(other, Player):
            return 1
        
        # Умножаем на 100 и преобразуем в int для точного сравнения
        my_power = int(self.calculate_power() * 100)
        other_power = int(other.calculate_power() * 100)
        
        if my_power < other_power:
            return -1
        elif my_power > other_power:
            return 1
        else:
            return 0


class Warrior(BaseWarrior, Printable, Comparable, Damageable):
    def to_string(self) -> str:
        return f"[Воин] {self._name} | Ур.{self._level} | Броня: {self._armor}% | Оружие: {self._weapon}"
    
    def compare_to(self, other) -> int:
        if not isinstance(other, Player):
            return 1
        
        my_power = int(self.calculate_power() * 100)
        other_power = int(other.calculate_power() * 100)
        
        if my_power < other_power:
            return -1
        elif my_power > other_power:
            return 1
        else:
            return 0


class Mage(BaseMage, Printable, Comparable, Damageable):
    def to_string(self) -> str:
        return f"[Маг] {self._name} | Ур.{self._level} | Мана: {self._mana}/100 | Заклинание: {self._spell}"
    
    def compare_to(self, other) -> int:
        if not isinstance(other, Player):
            return 1
        
        my_power = int(self.calculate_power() * 100)
        other_power = int(other.calculate_power() * 100)
        
        if my_power < other_power:
            return -1
        elif my_power > other_power:
            return 1
        else:
            return 0


class Archer(BaseArcher, Printable, Comparable, Damageable):
    def to_string(self) -> str:
        return f"[Лучник] {self._name} | Ур.{self._level} | Меткость: {self._accuracy}% | Лук: {self._bow_type}"
    
    def compare_to(self, other) -> int:
        if not isinstance(other, Player):
            return 1
        
        my_power = int(self.calculate_power() * 100)
        other_power = int(other.calculate_power() * 100)
        
        if my_power < other_power:
            return -1
        elif my_power > other_power:
            return 1
        else:
            return 0