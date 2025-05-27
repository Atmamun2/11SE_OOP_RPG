"""
Character module for the RPG game.

This module contains the Character base class and various character types.
"""
import sys
import os
from typing import Optional, Union, Type, List, Dict, Any
from abc import ABC, abstractmethod

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpg_game.weapon import Weapon, Rock, Paper, Scissors
from rpg_game.utils.logger import GameLogger
from rpg_game.inventory import Inventory, Item, Armor, Weapon as WeaponItem, Consumable

class Character(ABC):
    """
    Represents a game character with health, damage, and weapon attributes.
    
    This is an abstract base class that defines the common interface for all characters.
    """
    
    def __init__(
        self, 
        name: str, 
        health: int, 
        damage: int, 
        weapon: Optional[Weapon] = None,
        inventory_capacity: int = 20
    ) -> None:
        """
        Initialize a new Character.
        
        Args:
            name: The character's name
            health: The character's initial health
            damage: The character's base damage
            weapon: The character's weapon (optional)
            inventory_capacity: Maximum number of items the character can carry
        """
        self.name = name
        self._health = health
        self.damage = damage
        self.weapon = weapon
        self.inventory = Inventory(capacity=inventory_capacity)
        self.level = 1
        self.experience = 0
    
    @abstractmethod
    def special_ability(self) -> str:
        """
        Perform the character's special ability.
        
        Returns:
            A message describing the ability's effect
        """
        pass
    
    def attack(self, target: 'Character', logger: Optional[GameLogger] = None) -> int:
        """
        Attack another character.
        
        Args:
            target: The character to attack
            logger: Optional logger to log the attack
            
        Returns:
            The damage dealt
        """
        if self.weapon:
            damage = self.damage + self.weapon.damage_bonus
            weapon_msg = f" using {self.weapon.name}"
        else:
            damage = self.damage
            weapon_msg = ""
            
        if logger:
            logger.log_combat(self, target, damage)
            
        target.take_damage(damage)
        return damage
    
    def take_damage(self, amount: int) -> None:
        """
        Reduce the character's health by the given amount.
        
        Args:
            amount: The amount of damage to take
        """
        self._health = max(0, self._health - amount)
    
    def is_alive(self) -> bool:
        """Check if the character is still alive."""
        return self._health > 0
    
    def add_experience(self, amount: int) -> None:
        """
        Add experience points to the character.
        
        Args:
            amount: The amount of experience to add
        """
        self.experience += amount
        # Simple level up: every 100 XP levels up the character
        levels_gained = self.experience // 100
        if levels_gained > 0:
            self.level_up(levels_gained)
    
    def level_up(self, levels: int = 1) -> None:
        """
        Level up the character.
        
        Args:
            levels: Number of levels to gain
        """
        self.level += levels
        self._health += 10 * levels
        self.damage += 2 * levels
    
    def get_health(self) -> int:
        """Get the character's current health."""
        return self._health
    
    def set_health(self, health: int) -> None:
        """
        Set the character's health.
        
        Args:
            health: The new health value
        """
        self._health = max(0, health)
    
    def __str__(self) -> str:
        return f"{self.name} (Lv. {self.level}): {self._health} HP, {self.damage} ATK"

    # Getter for health - provides controlled access to the private attribute
    def get_health(self) -> int:
        """
        Get the character's current health.
        
        Returns:
            The character's current health
        """
        return self._health
    
    # Setter for health with validation - ensures health is never negative
    def set_health(self, new_health: int) -> None:
        """
        Set the character's health with validation.
        
        Args:
            new_health: The new health value
        """
        if new_health < 0:
            self._health = 0
        else:
            self._health = new_health

    # Method for the character to attack an enemy
    def attack(self, enemy: 'Character', logger: Optional[GameLogger] = None) -> int:
        """
        Attack another character.
        
        Args:
            enemy: The character to attack
            logger: Optional logger to log the combat
            
        Returns:
            The total damage dealt
        """
        total_damage = self.damage + (self.weapon.damage_bonus if self.weapon else 0)
        # Use getter and setter instead of direct attribute access
        current_health = enemy.get_health()
        enemy.set_health(current_health - total_damage)
        # Use the logger if provided (dependency), otherwise fall back to static method
        if logger:
            logger.log_combat(self, enemy, total_damage)
        return total_damage

    # Method to display character information
    def display(self) -> None:
        """Display the character's information."""
        weapon_name = self.weapon.name if self.weapon else 'No Weapon'
        weapon_damage = self.weapon.damage_bonus if self.weapon else 0
        # Use getter instead of direct attribute access
        print(f"Name: {self.name}\nHealth: {self.get_health()}\nDamage: {self.damage}\nWeapon: {weapon_name} (+{weapon_damage} Damage)")

    def get_inventory(self) -> Inventory:
        """Get the character's inventory."""
        return self.inventory

    def set_inventory(self, inventory: Inventory) -> None:
        """Set the character's inventory."""
        self.inventory = inventory


class Player(Character):
    """The player character with special abilities and progression."""
    
    def __init__(self, name: str, health: int = 100, damage: int = 10) -> None:
        """
        Initialize a new Player.
        
        Args:
            name: The player's name
            health: The player's initial health (default: 100)
            damage: The player's base damage (default: 10)
        """
        super().__init__(name, health, damage)
        self.sidekick = None
    
    def special_ability(self) -> str:
        """Use the player's special ability."""
        # Heal for 20% of max health
        heal_amount = int(self.get_health() * 0.2)
        self._health = min(100, self._health + heal_amount)
        return f"{self.name} uses Second Wind and heals for {heal_amount} HP!"
    
    def add_sidekick(self, sidekick: 'Sidekick') -> None:
        """
        Add a sidekick to assist the player.
        
        Args:
            sidekick: The sidekick to add
        """
        self.sidekick = sidekick
        return f"{sidekick.name} has joined {self.name}'s party!"


class Sidekick(Character, ABC):
    """Base class for all sidekick types."""
    
    def __init__(self, name: str, health: int, damage: int, ability: str) -> None:
        """
        Initialize a new Sidekick.
        
        Args:
            name: The sidekick's name
            health: The sidekick's initial health
            damage: The sidekick's base damage
            ability: Description of the sidekick's special ability
        """
        super().__init__(name, health, damage)
        self.ability = ability
    
    @abstractmethod
    def special_ability(self) -> str:
        """Perform the sidekick's special ability."""
        pass


class DefenderSidekick(Sidekick):
    """A defensive sidekick that can protect the player."""
    
    def __init__(self, name: str, health: int, damage: int) -> None:
        """
        Initialize a new DefenderSidekick.
        
        Args:
            name: The sidekick's name
            health: The sidekick's initial health
            damage: The sidekick's base damage
        """
        super().__init__(name, health, damage, "Shield Ally")
    
    def special_ability(self) -> str:
        """Use the defender's special ability to protect the player."""
        # Reduces damage taken by 50% for one turn
        return f"{self.name} raises their shield, ready to defend!"


class HealerSidekick(Sidekick):
    """A supportive sidekick that can heal the player."""
    
    def __init__(self, name: str, health: int, damage: int) -> None:
        """
        Initialize a new HealerSidekick.
        
        Args:
            name: The sidekick's name
            health: The sidekick's initial health
            damage: The sidekick's base damage
        """
        super().__init__(name, health, damage, "Healing Touch")
    
    def special_ability(self, target: Character) -> str:
        """
        Use the healer's special ability on a target.
        
        Args:
            target: The character to heal
        """
        heal_amount = 15
        target.set_health(target.get_health() + heal_amount)
        return f"{self.name} heals {target.name} for {heal_amount} HP!"


class Villain(Character, ABC):
    """Base class for all villain characters."""
    
    def __init__(self, name: str, health: int, damage: int, ability: str) -> None:
        """
        Initialize a new Villain.
        
        Args:
            name: The villain's name
            health: The villain's initial health
            damage: The villain's base damage
            ability: Description of the villain's special ability
        """
        super().__init__(name, health, damage)
        self.ability = ability
    
    @abstractmethod
    def special_ability(self) -> str:
        """Perform the villain's special ability."""
        pass


class Goblin(Villain):
    """A small but numerous enemy type."""
    
    def __init__(self) -> None:
        """Initialize a new Goblin."""
        super().__init__("Goblin", 30, 5, "Sneak Attack")
    
    def special_ability(self) -> str:
        """Use the goblin's special ability."""
        # 30% chance to deal double damage
        return f"{self.name} attempts a Sneak Attack!"


class Orc(Villain):
    """A strong and durable enemy type."""
    
    def __init__(self) -> None:
        """Initialize a new Orc."""
        super().__init__("Orc", 60, 8, "Brute Force")
    
    def special_ability(self) -> str:
        """Use the orc's special ability."""
        # Deal 50% more damage on next attack
        return f"{self.name} channels Brute Force for their next attack!"


class Boss(Villain):
    """
    Represents a boss enemy that inherits from Villain.
    
    This class demonstrates inheritance and method overriding.
    """
    
    def __init__(self, name: str, health: int, damage: int) -> None:
        """
        Initialize a new Boss.
        
        Args:
            name: The boss's name
            health: The boss's initial health
            damage: The boss's base damage
        """
        super().__init__(name, health, damage, "Boss Special")
    
    def attack(self, enemy: Character, logger: Optional[GameLogger] = None) -> int:
        """
        Attack another character with the boss's special attack.
        
        Overrides the Character.attack method to add additional damage.
        
        Args:
            enemy: The character to attack
            logger: Optional logger to log the combat
            
        Returns:
            The total damage dealt
        """
        # Call the parent class's attack method first
        damage_dealt = super().attack(enemy, logger)
        
        # Boss's special ability: 20% chance to deal double damage
        import random
        if random.random() < 0.2:  # 20% chance
            extra_damage = damage_dealt  # Deal the same amount again
            enemy.take_damage(extra_damage)
            
            if logger:
                logger.log_combat(self, enemy, extra_damage, "(critical hit!)")
            
            damage_dealt += extra_damage
        
        return damage_dealt
    
    def special_ability(self) -> str:
        """Use the boss's special ability."""
        # Bosses have powerful special abilities
        return f"{self.name} unleashes their ultimate power!"
