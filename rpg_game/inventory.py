"""
Inventory system for the RPG game.

This module contains the Item class hierarchy and Inventory class that manages
the inventory of a character with weight limits and item categories.
"""
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional, Union, Type, TypeVar, Any


class ItemType(Enum):
    """Types of items in the game."""
    ARMOR = auto()
    WEAPON = auto()
    CONSUMABLE = auto()
    MISC = auto()


class ArmorType(Enum):
    """Types of armor pieces."""
    HELMET = "Helmet"
    CHESTPLATE = "Chestplate"
    LEGGINGS = "Leggings"
    BOOTS = "Boots"
    CHARM = "Armor Charm"


class WeaponType(Enum):
    """Types of weapons."""
    BATTLE_AXE = "Battle Axe"
    SHORT_SWORD = "Short Sword"
    BOW_AND_ARROW = "Bow and Arrow"


@dataclass
class Item:
    """Base class for all items in the game."""
    name: str
    description: str
    weight: float  # in kg
    value: int  # in gold
    item_type: ItemType
    max_stack: int = 1
    quantity: int = 1

    def __str__(self) -> str:
        return f"{self.name} (x{self.quantity}): {self.description} - {self.weight}kg"


@dataclass
class Armor(Item):
    """Armor items that provide defense."""
    # Required fields (no default values)
    armor_type: ArmorType
    defense: int
    
    # Fields with default values
    durability: int = 100
    is_equipped: bool = False
    
    # Ensure these fields from Item come after required fields
    max_stack: int = 1
    quantity: int = 1

    def __post_init__(self):
        self.item_type = ItemType.ARMOR


@dataclass
class Weapon(Item):
    """Weapon items that deal damage."""
    # Required fields (no default values)
    weapon_type: WeaponType
    damage: int
    
    # Fields with default values
    durability: int = 100
    is_equipped: bool = False
    range: int = 1  # 1 for melee, >1 for ranged
    
    # Ensure these fields from Item come after required fields
    max_stack: int = 1
    quantity: int = 1

    def __post_init__(self):
        self.item_type = ItemType.WEAPON


@dataclass
class Consumable(Item):
    """Consumable items that can be used."""
    # Required fields (no default values)
    effect: str
    potency: int
    
    # Fields with default values
    duration: int = 0  # in turns, 0 for instant
    max_stack: int = 5  # Higher max stack for consumables
    
    # Ensure this field from Item comes after required fields
    quantity: int = 1

    def __post_init__(self):
        self.item_type = ItemType.CONSUMABLE


class Location(Enum):
    """Game locations where items can be found."""
    TOWNSVILLE = "Townsville"
    SHATTERED_SPIRE = "The Shattered Spire"
    WHISPERING_CATACOMBS = "The Whispering Catacombs"
    CLOCKWORK_FORGE = "The Clockwork Forge"
    VERDANT_MAW = "The Verdant Maw"
    DROWNED_CATHEDRAL = "The Drowned Cathedral"


class Inventory:
    """Manages a character's inventory with weight limits and item categories."""
    
    MAX_WEIGHT = 100.0  # 100kg weight limit
    MAX_CONSUMABLES = 3  # Max number of different consumable types
    
    def __init__(self):
        self.items: List[Item] = []
        self.equipped_armor: Dict[ArmorType, Optional[Armor]] = {at: None for at in ArmorType}
        self.equipped_weapon: Optional[Weapon] = None
        self.current_weight: float = 0.0
    
    def add_item(self, item: Item) -> bool:
        """
        Add an item to the inventory.
        
        Args:
            item: The item to add
            
        Returns:
            bool: True if the item was added successfully, False otherwise
        """
        # Check if adding this item would exceed weight limit
        if self.current_weight + (item.weight * item.quantity) > self.MAX_WEIGHT:
            return False
        
        # Check for stackable items
        if item.item_type == ItemType.CONSUMABLE:
            # Check if we already have this consumable and can stack it
            for existing in self.items:
                if (isinstance(existing, Consumable) and 
                    existing.name == item.name and 
                    existing.quantity < existing.max_stack):
                    existing.quantity += item.quantity
                    self.current_weight += item.weight * item.quantity
                    return True
            
            # If we can't stack, check if we can add a new consumable type
            if len([i for i in self.items if i.item_type == ItemType.CONSUMABLE]) >= self.MAX_CONSUMABLES:
                return False
        
        # Add the new item
        self.items.append(item)
        self.current_weight += item.weight * item.quantity
        return True
    
    def remove_item(self, item: Item, quantity: int = 1) -> bool:
        """
        Remove an item from the inventory.
        
        Args:
            item: The item to remove
            quantity: How many to remove
            
        Returns:
            bool: True if the item was removed, False otherwise
        """
        for i, inv_item in enumerate(self.items):
            if inv_item == item:
                if inv_item.quantity > quantity:
                    inv_item.quantity -= quantity
                    self.current_weight -= item.weight * quantity
                else:
                    self.items.pop(i)
                    self.current_weight -= item.weight * inv_item.quantity
                return True
        return False
    
    def equip_armor(self, armor: Armor) -> bool:
        """
        Equip a piece of armor.
        
        Args:
            armor: The armor to equip
            
        Returns:
            bool: True if equipped successfully, False otherwise
        """
        if armor not in self.items:
            return False
            
        # Unequip currently equipped armor of this type if any
        if self.equipped_armor[armor.armor_type]:
            self.unequip_armor(armor.armor_type)
            
        armor.is_equipped = True
        self.equipped_armor[armor.armor_type] = armor
        return True
    
    def unequip_armor(self, armor_type: ArmorType) -> bool:
        """
        Unequip a piece of armor.
        
        Args:
            armor_type: The type of armor to unequip
            
        Returns:
            bool: True if unequipped successfully, False otherwise
        """
        if not self.equipped_armor[armor_type]:
            return False
            
        self.equipped_armor[armor_type].is_equipped = False
        self.equipped_armor[armor_type] = None
        return True
    
    def equip_weapon(self, weapon: Weapon) -> bool:
        """
        Equip a weapon.
        
        Args:
            weapon: The weapon to equip
            
        Returns:
            bool: True if equipped successfully, False otherwise
        """
        if weapon not in self.items:
            return False
            
        # Unequip current weapon if any
        if self.equipped_weapon:
            self.unequip_weapon()
            
        weapon.is_equipped = True
        self.equipped_weapon = weapon
        return True
    
    def unequip_weapon(self) -> bool:
        """
        Unequip the currently equipped weapon.
        
        Returns:
            bool: True if unequipped successfully, False otherwise
        """
        if not self.equipped_weapon:
            return False
            
        self.equipped_weapon.is_equipped = False
        self.equipped_weapon = None
        return True
    
    def use_consumable(self, consumable: Consumable) -> bool:
        """
        Use a consumable item.
        
        Args:
            consumable: The consumable to use
            
        Returns:
            bool: True if used successfully, False otherwise
        """
        if consumable not in self.items:
            return False
            
        # Apply the consumable effect here
        # This would be handled by the game's effect system
        print(f"Using {consumable.name}: {consumable.effect}")
        
        # Remove one from the stack or remove the item if last one
        return self.remove_item(consumable, 1)
    
    def get_equipped_items(self) -> Dict[str, Union[Armor, Weapon, None]]:
        """
        Get all currently equipped items.
        
        Returns:
            Dict containing equipped items by slot
        """
        return {
            'weapon': self.equipped_weapon,
            **{at.value: armor for at, armor in self.equipped_armor.items() if armor}
        }
    
    def get_inventory_by_type(self, item_type: ItemType) -> List[Item]:
        """
        Get all items of a specific type.
        
        Args:
            item_type: The type of items to get
            
        Returns:
            List of items of the specified type
        """
        return [item for item in self.items if item.item_type == item_type]
    
    def get_total_weight(self) -> float:
        """
        Get the total weight of all items in the inventory.
        
        Returns:
            float: Total weight in kg
        """
        return sum(item.weight * item.quantity for item in self.items)
    
    def display(self) -> str:
        """
        Generate a string representation of the inventory.
        
        Returns:
            str: Formatted inventory display
        """
        output = ["=== INVENTORY ==="]
        output.append(f"Weight: {self.current_weight:.1f}/{self.MAX_WEIGHT}kg")
        
        # Show equipped items
        output.append("\n--- EQUIPPED ---")
        if self.equipped_weapon:
            output.append(f"Weapon: {self.equipped_weapon.name} (Dmg: {self.equipped_weapon.damage})")
        
        for armor_type, armor in self.equipped_armor.items():
            if armor:
                output.append(f"{armor_type.value}: {armor.name} (Def: {armor.defense})")
        
        # Show items by category
        categories = {
            "Weapons": self.get_inventory_by_type(ItemType.WEAPON),
            "Armor": self.get_inventory_by_type(ItemType.ARMOR),
            "Consumables": self.get_inventory_by_type(ItemType.CONSUMABLE),
            "Misc": self.get_inventory_by_type(ItemType.MISC)
        }
        
        for category, items in categories.items():
            if items:
                output.append(f"\n--- {category.upper()} ---")
                for item in items:
                    output.append(f"- {item}")
        
        return "\n".join(output)


# Example items that can be used in the game
class GameItems:
    """Predefined game items for easy access."""
    
    # Armor
    LEATHER_HELMET = Armor(
        name="Leather Helmet",
        description="Basic head protection made of tanned leather.",
        weight=0.5,
        value=15,
        armor_type=ArmorType.HELMET,
        defense=2
    )
    
    IRON_CHESTPLATE = Armor(
        name="Iron Chestplate",
        description="Sturdy chest protection made of iron plates.",
        weight=8.0,
        value=100,
        armor_type=ArmorType.CHESTPLATE,
        defense=8
    )
    
    # Weapons
    RUSTY_SWORD = Weapon(
        name="Rusty Sword",
        description="An old, worn-out sword that has seen better days.",
        weight=2.5,
        value=20,
        weapon_type=WeaponType.SHORT_SWORD,
        damage=5
    )
    
    HUNTERS_BOW = Weapon(
        name="Hunter's Bow",
        description="A well-crafted bow used by experienced hunters.",
        weight=1.5,
        value=75,
        weapon_type=WeaponType.BOW_AND_ARROW,
        damage=7,
        range=3
    )
    
    # Consumables
    HEALTH_POTION = Consumable(
        name="Health Potion",
        description="Restores 30 health points when consumed.",
        weight=0.3,
        value=25,
        effect="restore_health",
        potency=30
    )
    
    STAMINA_ELIXIR = Consumable(
        name="Stamina Elixir",
        description="Restores 50 stamina points over 3 turns.",
        weight=0.3,
        value=35,
        effect="restore_stamina",
        potency=50,
        duration=3
    )