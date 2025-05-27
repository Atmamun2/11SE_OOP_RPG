"""
Game module for the RPG game.

This module contains the Game class that manages the game flow, combat, and interactions.
"""
import sys
import os
import random
from typing import List, Tuple, Optional, Dict, Any, Type

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rpg_game.character import (
    Character, Player, Boss, 
    Goblin, Orc, 
    DefenderSidekick, HealerSidekick # for some reason these were not used
)
from rpg_game.weapon import Rock, Paper, Scissors, Lizard, Spock
from rpg_game.inventory import Inventory, Item, Armor, Weapon as WeaponItem, Consumable # same with inventory, item , armour and weapon item
from rpg_game.utils.logger import GameLogger
from rpg_game.utils.console import clear_screen, press_enter, print_border

# Game constants
MAX_LEVEL = 10
INITIAL_HEALTH = 100
INITIAL_DAMAGE = 10

# Enemy configurations
ENEMY_TYPES = [Goblin, Orc]
BOSS_TYPES = [
    ("Goblin King", 150, 15, "Summon Minions"),
    ("Dark Sorcerer", 200, 12, "Dark Magic"),
    ("Dragon Lord", 300, 20, "Fire Breath"),
    ("Elemental Titan", 400, 25, "Elemental Mastery")
]

# Item configurations
STARTING_ITEMS = [
    Rock(),
    Paper(),
    Scissors(),
    Lizard(),
    Spock(),
# Added Lizard and Spock as two of the new starting items
]

# Location configurations
LOCATIONS = [
    "Townsville (Starting Village)",
    "The Shattered Spire",
    "Whispering Catacombs",
    "Clockwork Forge",
    "Verdant Maw",
    "Drowned Cathedral"
]


class Game:
    """
    Manages the game flow, including character creation, combat, and game state.
    
    This class demonstrates orchestration of other classes and game logic.
    """
    
    def __init__(self) -> None:
        """Initialize a new Game instance."""
        self.player: Optional[Player] = None
        self.current_enemy: Optional[Character] = None
        self.bosses: List[Boss] = []
        self.quests: List[Dict[str, Any]] = []
        self.current_location: str = LOCATIONS[0]  # Start in Townsville
        self.game_active: bool = True # the while loop condition on whether the game is active or not.
        self.logger = GameLogger()
        self.setup_game()
    
    def setup_game(self) -> None:
        """Set up the initial game state."""
        # Initialize player
        self.player = Player("Hero", INITIAL_HEALTH, INITIAL_DAMAGE)
        
        # Add starting items
        for item in STARTING_ITEMS:
            self.player.inventory.add_item(item)
        
        # Create bosses
        for boss_data in BOSS_TYPES:
            name, health, damage, ability = boss_data # unpacks the tuple boss data from Line ~30-35
            boss = Boss(name, health, damage) 
            boss.ability = ability 
            self.bosses.append(boss)
        
        # Initial quests
        self.quests = [
            {
                "name": "Defeat the Goblin King",
                "description": "The Goblin King has been terrorizing the countryside. Defeat him!",
                "completed": False,
                "objective": {"type": "defeat", "target": "Goblin King"},
                "reward": {"xp": 100, "gold": 50, "item": None}
            },
            {
                "name": "Defeat the Dark Sorcerer",
                "description": "The Dark Sorcerer is gathering dark forces. Stop him before it's too late!",
                "completed": False,
                "objective": {"type": "defeat", "target": "Dark Sorcerer"},
                "reward": {"xp": 200, "gold": 100, "item": "Amulet of Power"}
            },
            {
                "name": "Defeat the Dragon Lord",
                "description": "The Dragon Lord is terrorizing the countryside. Defeat him!",
                "completed": False,
                "objective": {"type": "defeat", "target": "Dragon Lord"},
                "reward": {"xp": 300, "gold": 150, "item": "Dragon Scales"}
            }
        ]
    
    def start_game(self) -> None:
        """Start the main game loop."""
        self.show_welcome()
        self.create_character()
        
        while self.game_active and self.player.is_alive() and self.bosses: # while the game is active and the player is alive and there are bosses left
            self.game_loop() # the game loop continues
        
        # when it exits out of the while loop the game ends immediately

        self.end_game()
    
    def game_loop(self) -> None:
        """Main game loop."""
        self.show_game_state()
        self.handle_player_action()
        
        # Check for quest completion
        self.update_quests()
        
        # Check for level up
        if self.player.experience >= (self.player.level * 100):
            self.player.level_up()
            print(f"Level up! You are now level {self.player.level}.")
    
    def handle_player_action(self) -> None:
        """Handle player's action in the game world."""
        print("\nWhat would you like to do?")
        print("1. Explore")
        print("2. Check inventory")
        print("3. View quests")
        print("4. Use item")
        print("5. Rest (heal to full health)")
        print("6. Quit game")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            self.explore()
        elif choice == "2":
            self.show_inventory()
        elif choice == "3":
            self.show_quests()
        elif choice == "4":
            self.use_item()
        elif choice == "5":
            self.rest()
        elif choice == "6":
            self.quit_game()
        else:
            print("Invalid choice. Please try again.")
    
    def explore(self) -> None:
        """Handle the explore action."""
        print(f"\nYou explore the area around {self.current_location}...")
        
        # Random encounter chance (30%)
        if random.random() < 0.3:
            self.random_encounter()
        else:
            print("You find nothing of interest.")
    
    def random_encounter(self) -> None:
        """Handle a random encounter with an enemy."""
        enemy_class = random.choice(ENEMY_TYPES)
        enemy = enemy_class()
        print(f"A wild {enemy.name} appears!")
        
        self.combat_loop(enemy)
    
    def combat_loop(self, enemy: Character) -> None:
        """Handle combat between player and enemy."""
        print(f"\n=== Combat Started ===")
        print(f"{self.player.name} vs {enemy.name}")
        

        # while the enemy and player is still alive
        while self.player.is_alive() and enemy.is_alive():
            # Player's turn
            print(f"\nYour turn!")
            print(f"Your health: {self.player.get_health()}")
            print(f"{enemy.name}'s health: {enemy.get_health()}")
            # health status concurrent update

            print("\n1. Attack")
            print("2. Use special ability")
            print("3. Use item")
            print("4. Try to flee")
            
            choice = input("Choose an action: ")
            
            if choice == "1":
                # Player attacks
                damage = self.player.attack(enemy, self.logger)
                print(f"You deal {damage} damage to {enemy.name}!")
            elif choice == "2":
                # Player uses special ability
                ability_msg = self.player.special_ability()
                print(ability_msg)
            elif choice == "3":
                # Player uses item
                self.use_item_in_combat()
                continue  # Don't end turn if item was used
            elif choice == "4":
                # Try to flee
                if random.random() < 0.5:  # 50% chance to flee
                    print("You successfully fled from battle!")
                    return
                else:
                    print("You failed to flee!")
            else:
                print("Invalid choice. You hesitate and waste your turn.")
            
            # Check if enemy is defeated
            if not enemy.is_alive():
                print(f"You defeated {enemy.name}!")
                self.handle_victory(enemy)
                return
            
            # Enemy's turn
            print(f"\n{enemy.name}'s turn!")
            damage = enemy.attack(self.player, self.logger)
            print(f"{enemy.name} deals {damage} damage to you!")
            
            # Check if player is defeated
            if not self.player.is_alive():
                print("You have been defeated!")
                return
    
    def handle_victory(self, enemy: Character) -> None:
        """Handle victory over an enemy."""
        # Grant experience
        xp_reward = 20 if not isinstance(enemy, Boss) else 100
        self.player.add_experience(xp_reward)
        print(f"You gained {xp_reward} experience points!")
        
        # Check for level up
        if self.player.experience >= (self.player.level * 100):
            self.player.level_up()
            print(f"Level up! You are now level {self.player.level}.")
        
        # Check if defeated a boss
        if isinstance(enemy, Boss):
            self.bosses.remove(enemy)
            print(f"You have defeated {enemy.name}!")
    
    def show_inventory(self) -> None:
        """Display the player's inventory."""
        print("\n=== Inventory ===")
        print(f"Gold: {self.player.inventory.gold}")
        print("\nItems:")
        for i, item in enumerate(self.player.inventory.items, 1):
            print(f"{i}. {item.name} - {item.description}")
        
        input("\nPress Enter to continue...")
    
    def show_quests(self) -> None:
        """Display active quests."""
        print("\n=== Quests ===")
        for i, quest in enumerate(self.quests, 1):
            status = "[COMPLETED]" if quest["completed"] else ""
            print(f"{i}. {quest['name']} {status}")
            print(f"   {quest['description']}")
        
        input("\nPress Enter to continue...")
    
    def update_quests(self) -> None:
        """Update quest status based on game state."""
        for quest in self.quests:
            if quest["completed"]:
                continue
                
            if quest["objective"]["type"] == "defeat":
                target = quest["objective"]["target"]
                if not any(boss.name == target for boss in self.bosses):
                    quest["completed"] = True
                    print(f"\nQuest completed: {quest['name']}!")
                    
                    # Grant rewards
                    reward = quest["reward"]
                    self.player.inventory.gold += reward["gold"]
                    self.player.add_experience(reward["xp"])
                    
                    if reward["item"]:
                        print(f"You received {reward['item']} as a reward!")
                        # Add item to inventory
                        # (Implementation depends on your item system)
    
    def use_item(self) -> None:
        """Use an item from inventory."""
        if not self.player.inventory.items:
            print("Your inventory is empty!")
            return
            
        print("\nSelect an item to use:")
        for i, item in enumerate(self.player.inventory.items, 1):
            print(f"{i}. {item.name} - {item.description}")
        
        try:
            choice = int(input("Enter item number (or 0 to cancel): "))
            if choice == 0:
                return
                
            item = self.player.inventory.items[choice - 1]
            # Handle item usage based on item type
            if isinstance(item, Consumable):
                self.player.inventory.use_item(item)
                print(f"You used {item.name}!")
            else:
                print("You can't use that item right now.")
                
        except (ValueError, IndexError):
            print("Invalid choice.")
    
    def use_item_in_combat(self) -> None:
        """Use an item during combat."""
        consumables = [i for i in self.player.inventory.items if isinstance(i, Consumable)]
        
        if not consumables:
            print("You don't have any usable items!")
            return
            
        print("\nSelect an item to use:")
        for i, item in enumerate(consumables, 1):
            print(f"{i}. {item.name} - {item.description}")
        
        try:
            choice = int(input("Enter item number (or 0 to cancel): "))
            if choice == 0:
                return
                
            item = consumables[choice - 1]
            self.player.inventory.use_item(item)
            print(f"You used {item.name}!")
            
        except (ValueError, IndexError):
            print("Invalid choice.")
    
    def rest(self) -> None:
        """Rest to restore health."""
        self.player.set_health(INITIAL_HEALTH)
        print("You rest and recover your health.")
    
    def quit_game(self) -> None:
        """Quit the game."""
        print("\nThanks for playing!")
        self.game_active = False
    
    def show_welcome(self) -> None:
        """Display the welcome message."""
        print("=== Welcome to the RPG Adventure! ===")
        print("A text-based adventure where you battle monsters and complete quests!")
        print("Type 'help' at any time for a list of commands.\n")
    
    def create_character(self) -> None:
        """Create a new character."""
        print("=== Character Creation ===")
        name = input("Enter your character's name: ")
        self.player = Player(name, INITIAL_HEALTH, INITIAL_DAMAGE) # taking in the initial health and damage from the constants.py file
        print(f"\nWelcome, {name}! Your adventure begins now!")
    
    def show_game_state(self) -> None:
        """Display the current game state."""
        clear_screen()
        print(f"=== {self.current_location} ===")
        print(f"Player: {self.player.name} (Lv. {self.player.level})")
        print(f"Health: {self.player.get_health()}/{INITIAL_HEALTH}")
        print(f"XP: {self.player.experience}/{(self.player.level + 1) * 100}")
        print(f"Gold: {self.player.inventory.gold}")
        print("-" * 20)
    
    def end_game(self) -> None:
        """Handle game over conditions."""
        if not self.player.is_alive():
            print("\n=== Game Over ===")
            print("You have been defeated. Better luck next time!")
        elif not self.bosses:
            print("\n=== Victory! ===")
            print("Congratulations! You have defeated all the bosses and saved the land!")
        else:
            print("\nThanks for playing!")
        
        print("\nGame over.")
        self.game_active = False

    # Show the introductory message and set up the game
    def show_intro(self) -> None:
        """Display the game introduction and set up the player character."""
        clear_screen()
        print(WELCOME_MESSAGE)
        player_name = input("Enter your character's name: ").capitalize()
        print(INTRO_MESSAGE.format(player_name=player_name))
        self.setup_game(player_name)

    # Set up the game by creating the player character and bosses
    def setup_game(self, name: str) -> None:
        """
        Set up the game with player character and bosses.
        
        Args:
            name: The player character's name
        """
        # Get weapon details instead of a Weapon object
        weapon_name, weapon_damage = self.choose_weapon()
        self.player = Character(name, PLAYER_INITIAL_HEALTH, PLAYER_INITIAL_DAMAGE, 
                               weapon_name, weapon_damage)
        self.player.display()
        press_enter()
        self.bosses = [
            Boss(GOBLIN_KING_NAME, GOBLIN_KING_HEALTH, GOBLIN_KING_DAMAGE), 
            Boss(DARK_SORCERER_NAME, DARK_SORCERER_HEALTH, DARK_SORCERER_DAMAGE),
            Boss(DRAGON_LORD_NAME, DRAGON_LORD_HEALTH, DRAGON_LORD_DAMAGE)
        ]

    # Allow the player to choose a weapon
    def choose_weapon(self) -> Tuple[str, int]:
        """
        Let the player choose a weapon.
        
        Returns:
            A tuple containing the weapon name and damage bonus
        """
        weapons = [
            {"name": WEAPON_ROCK_NAME, "damage_bonus": WEAPON_ROCK_DAMAGE},
            {"name": WEAPON_PAPER_NAME, "damage_bonus": WEAPON_PAPER_DAMAGE},
            {"name": WEAPON_SCISSORS_NAME, "damage_bonus": WEAPON_SCISSORS_DAMAGE},
            {"name": WEAPON_LIZARD_NAME, "damage_bonus": WEAPON_LIZARD_DAMAGE},
            {"name": WEAPON_SPOCK_NAME, "damage_bonus": WEAPON_SPOCK_DAMAGE}
        ]
        options = [weapon["name"] for weapon in weapons]
        prompt = "\nChoose your weapon (Rock, Paper, Scissors, Lizard, Spock): "
        choice_index = self.get_valid_input(prompt, options)
        weapon_data = weapons[choice_index]
        # Return weapon name and damage instead of creating a Weapon object
        return weapon_data["name"], weapon_data["damage_bonus"]

    # Get valid user input for weapon choice
    def get_valid_input(self, prompt: str, options: List[str]) -> int:
        """
        Get valid user input from a list of options.
        
        Args:
            prompt: The prompt to display to the user
            options: List of valid options
            
        Returns:
            The index of the chosen option
        """
        while True:
            user_input = input(prompt).capitalize()
            if user_input in options:
                return options.index(user_input)
            print("Invalid input, please try again.")

    # Handle the combat between player and enemy
    def combat(self, player: Character, enemy: Boss) -> bool:
        """
        Handle combat between player and enemy.
        
        Args:
            player: The player character
            enemy: The enemy character
            
        Returns:
            True if the player won, False otherwise
        """
        while player.get_health() > 0 and enemy.get_health() > 0:
            self.display_combat_status(player, enemy)
            # Pass the logger to the attack methods
            damage_dealt = player.attack(enemy, self.logger)
            print(f"You dealt {damage_dealt} damage to {enemy.name}.")
            if enemy.get_health() <= 0:
                self.print_victory_message(enemy)
                return True

            # Pass the logger to the attack methods
            damage_received = enemy.attack(player, self.logger)
            print(f"{enemy.name} dealt {damage_received} damage to you.")
            if player.get_health() <= 0:
                self.print_defeat_message(enemy)
                return False
            press_enter()

    # Display the current status of the combat
    def display_combat_status(self, player: Character, enemy: Boss) -> None:
        """
        Display the current combat status.
        
        Args:
            player: The player character
            enemy: The enemy character
        """
        clear_screen()
        level = "LEVEL 1" if enemy.name == "Goblin King" else "LEVEL 2"
        print(f"\n=============> {level}: {enemy.name} <=============")
        player.display()
        print("-" * SEPARATOR_LENGTH)
        enemy.display()
        print("-" * SEPARATOR_LENGTH)

    # Handle battles with bosses
    def handle_boss_battles(self) -> None:
        """Handle battles with all bosses in sequence."""
        for boss in self.bosses:
            self.introduce_boss(boss)
            if not self.combat(self.player, boss):
                self.end_game(False)
                return
        self.end_game(True)

    # Introduce each boss before the battle
    def introduce_boss(self, boss: Boss) -> None:
        """
        Introduce a boss before battle.
        
        Args:
            boss: The boss to introduce
        """
        clear_screen()
        intro_messages = {
            GOBLIN_KING_NAME: GOBLIN_KING_INTRO.format(player_name=self.player.name),
            DARK_SORCERER_NAME: DARK_SORCERER_INTRO.format(player_name=self.player.name)
        }
        print(intro_messages.get(boss.name, "A new boss appears!"))
        press_enter()

    # Print victory message after defeating an enemy
    def print_victory_message(self, enemy: Boss) -> None:
        """
        Print a victory message.
        
        Args:
            enemy: The defeated enemy
        """
        print_border()
        print(VICTORY_MESSAGE.format(enemy_name=enemy.name))
        press_enter()

    # Print defeat message after being defeated by an enemy
    def print_defeat_message(self, enemy: Boss) -> None:
        """
        Print a defeat message.
        
        Args:
            enemy: The enemy that defeated the player
        """
        print_border()
        print(DEFEAT_MESSAGE.format(enemy_name=enemy.name))
        press_enter()

    # End the game and show final message
    def end_game(self, player_won: bool) -> None:
        """
        End the game and show the final message.
        
        Args:
            player_won: Whether the player won the game
        """
        print_border()
        if player_won:
            print(GAME_WIN_MESSAGE.format(player_name=self.player.name))
        else:
            print(GAME_OVER_MESSAGE.format(player_name=self.player.name))
        print_border()

    # Run the game
    def run(self) -> None:
        """Run the game from start to finish."""
        self.show_intro()
        self.handle_boss_battles()
