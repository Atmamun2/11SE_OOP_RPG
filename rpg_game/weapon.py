"""
Weapon module for the RPG game.

This module contains the Weapon base class and its subclasses that demonstrate
polymorphism through method overriding.
"""
import sys
import os
from typing import Optional, TypeVar, Any
from abc import ABC, abstractmethod

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Weapon(ABC):
    """
    Abstract base class for all weapons in the game.
    
    This class defines the interface that all weapons must implement.
    """
    def __init__(self, name: str, damage_bonus: int) -> None:
        """
        Initialize a new Weapon.
        
        Args:
            name: The name of the weapon
            damage_bonus: The additional damage this weapon provides
        """
        self.name = name
        self.damage_bonus = damage_bonus
    
    @abstractmethod
    def use(self, target: Any) -> str:
        """
        Use the weapon on a target.
        
        Args:
            target: The target to use the weapon on
            
        Returns:
            A message describing the action
        """
        pass
    
    def __str__(self) -> str:
        return f"{self.name} (+{self.damage_bonus} damage)"


class Rock(Weapon):
    """A heavy rock that can be thrown at enemies."""
    
    def __init__(self) -> None:
        super().__init__("Rock", damage_bonus=5)
    
    def use(self, target: Any) -> str:
        """
        Throw the rock at the target.
        
        Rock is strong against Scissors but weak against Paper.
        """
        if hasattr(target, 'weapon') and isinstance(target.weapon, Scissors):
            # Critical hit against Scissors
            return f"{self.name} crushes {target.weapon.name}! Critical hit!"
        elif hasattr(target, 'weapon') and isinstance(target.weapon, Paper):
            # Weak against Paper
            return f"{self.name} is wrapped by {target.weapon.name}! Not very effective..."
        return f"Threw {self.name} at {getattr(target, 'name', 'the target')}!"


class Paper(Weapon):
    """A sheet of paper that can be used to wrap or cover."""
    
    def __init__(self) -> None:
        super().__init__("Paper", damage_bonus=3)
    
    def use(self, target: Any) -> str:
        """
        Use the paper on the target.
        
        Paper is strong against Rock but weak against Scissors.
        """
        if hasattr(target, 'weapon') and isinstance(target.weapon, Rock):
            # Critical hit against Rock
            return f"{self.name} wraps around {target.weapon.name}! Critical hit!"
        elif hasattr(target, 'weapon') and isinstance(target.weapon, Scissors):
            # Weak against Scissors
            return f"{self.name} is cut by {target.weapon.name}! Not very effective..."
        return f"Used {self.name} on {getattr(target, 'name', 'the target')}!"


class Scissors(Weapon):
    """A sharp pair of scissors that can cut through things."""
    
    def __init__(self) -> None:
        super().__init__("Scissors", damage_bonus=4)
    
    def use(self, target: Any) -> str:
        """
        Use the scissors on the target.
        
        Scissors are strong against Paper and Lizard but weak against Rock and Spock.
        """
        if hasattr(target, 'weapon') and (isinstance(target.weapon, Paper) or isinstance(target.weapon, Lizard)):
            # Critical hit against Paper and Lizard
            return f"{self.name} cut through {target.weapon.name}! Critical hit!"
        elif hasattr(target, 'weapon') and (isinstance(target.weapon, Rock) or isinstance(target.weapon, Spock)):
            # Weak against Rock and Spock
            return f"{self.name} are crushed by {target.weapon.name}! Not very effective..."
        return f"Used {self.name} on {getattr(target, 'name', 'the target')}!"


class Lizard(Weapon):
    """A small lizard that can poison enemies."""
    
    def __init__(self) -> None:
        super().__init__("Lizard", damage_bonus=3)
    
    def use(self, target: Any) -> str:
        """
        Use the lizard on the target.
        
        Lizard is strong against Spock and Paper but weak against Rock and Scissors.
        """
        if hasattr(target, 'weapon') and (isinstance(target.weapon, Spock) or isinstance(target.weapon, Paper)):
            # Critical hit against Spock and Paper
            return f"{self.name} poisons {target.weapon.name}! Critical hit!"
        elif hasattr(target, 'weapon') and (isinstance(target.weapon, Rock) or isinstance(target.weapon, Scissors)):
            # Weak against Rock and Scissors
            return f"{self.name} is defeated by {target.weapon.name}! Not very effective..."
        return f"Used {self.name} on {getattr(target, 'name', 'the target')}!"


class Spock(Weapon):
    """A powerful alien with advanced technology."""
    
    def __init__(self) -> None:
        super().__init__("Spock", damage_bonus=5)
    
    def use(self, target: Any) -> str:
        """
        Use Spock on the target.
        
        Spock is strong against Rock and Scissors but weak against Lizard and Paper.
        """
        if hasattr(target, 'weapon') and (isinstance(target.weapon, Rock) or isinstance(target.weapon, Scissors)):
            # Critical hit against Rock and Scissors
            return f"{self.name} vaporizes {target.weapon.name}! Critical hit!"
        elif hasattr(target, 'weapon') and (isinstance(target.weapon, Lizard) or isinstance(target.weapon, Paper)):
            # Weak against Lizard and Paper
            return f"{self.name} is defeated by {target.weapon.name}! Not very effective..."
        return f"Used {self.name} on {getattr(target, 'name', 'the target')}!"
