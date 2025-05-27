"""
Constants for the RPG game.

This module contains all the constant values used throughout the game.
"""

# Player constants
PLAYER_INITIAL_HEALTH = 110
PLAYER_INITIAL_DAMAGE = 10

# Boss constants
GOBLIN_KING_NAME = "Goblin King"
GOBLIN_KING_HEALTH = 50
GOBLIN_KING_DAMAGE = 8

DARK_SORCERER_NAME = "Dark Sorcerer"
DARK_SORCERER_HEALTH = 60
DARK_SORCERER_DAMAGE = 9

DRAGON_LORD_NAME = "Dragon Lord"
DRAGON_LORD_HEALTH = 70
DRAGON_LORD_DAMAGE = 10

# Weapon constants
WEAPON_ROCK_NAME = "Rock"
WEAPON_ROCK_DAMAGE = 2

WEAPON_PAPER_NAME = "Paper"
WEAPON_PAPER_DAMAGE = 3

WEAPON_SCISSORS_NAME = "Scissors"
WEAPON_SCISSORS_DAMAGE = 4

WEAPON_LIZARD_NAME = "Lizard"
WEAPON_LIZARD_DAMAGE = 5

WEAPON_SPOCK_NAME = "Spock"
WEAPON_SPOCK_DAMAGE = 6

# UI constants
SEPARATOR_LENGTH = 30
BORDER_LENGTH = 80

# Game messages
WELCOME_MESSAGE = (
    "🌟 Welcome, brave adventurer, to the RPG Adventure! 🌟\n"
    "Legends tell of heroes who rise against impossible odds—will you become one?"
)
INTRO_MESSAGE = (
    "In a realm shrouded in darkness and peril, you, {player_name}, have been chosen by fate.\n"
    "Two formidable bosses threaten the land: the ferocious Goblin King and the enigmatic Dark Sorcerer.\n"
    "Your journey will test your courage, wit, and strength. Gather your resolve—the fate of this world rests in your hands."
)

# Level messages
GOBLIN_KING_INTRO = (
    "🗡️ Level 1: The Goblin King's Lair 🗡️\n"
    "You step into a dank, torch-lit cavern echoing with guttural laughter.\n"
    "The Goblin King, infamous for his brute strength and savage cunning, awaits.\n"
    "Steel yourself, {player_name}, for this battle will be fierce and unforgiving!"
)
DARK_SORCERER_INTRO = (
    "🔮 Level 2: The Dark Sorcerer's Tower 🔮\n"
    "With the Goblin King fallen, you ascend a spiraling staircase into a chamber pulsing with arcane energy.\n"
    "The Dark Sorcerer, master of forbidden spells and illusions, greets you with a sinister grin.\n"
    "Only true heroes survive his magic. Face your fears, {player_name}, and let your legend grow!"
)

DRAGON_LORD_INTRO = (
    "🐉 Level 3: The Dragon Lord's Aerie 🐉\n"
    "The very air itself seems to tremble as you enter the volcanic lair high in the Obsidian Peaks.\n"
    "Before you towers the ancient Dragon Lord, his scales glistening like molten gold in the firelight.\n"
    "His voice rumbles like distant thunder: 'Foolish mortal! None have withstood my flame!\n"
    "Prove your worth, {player_name}, or be reduced to ashes like all who came before!"
)

# Combat messages
VICTORY_MESSAGE = (
    "🏆 Triumph! 🏆\n"
    "With a final, decisive blow, you have vanquished {enemy_name}.\n"
    "The air crackles with your newfound power as the path ahead becomes clear."
)
DEFEAT_MESSAGE = (
    "💀 Defeat... 💀\n"
    "You fought valiantly, but {enemy_name} has bested you in battle.\n"
    "Every setback is a lesson—rise again, stronger than before!"
)
GAME_WIN_MESSAGE = (
    "🎉 Heroic Victory! 🎉\n"
    "All evil has been banished thanks to your bravery, {player_name}.\n"
    "The people rejoice, and songs will be sung of your deeds for generations to come!\n"
    "You are a true legend of the realm!"
)
GAME_OVER_MESSAGE = (
    "☠️ Game Over ☠️\n"
    "Though darkness prevails this day, the spirit of a true hero never fades.\n"
    "Rest and return, {player_name}—the world still needs you. Your next adventure awaits!"
)
