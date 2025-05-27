#!/usr/bin/env python3
"""
Main entry point for the RPG game.

This module initializes and starts the game.
"""

from rpg_game.game import Game

def main() -> None:
    """Initialize and start the game."""
    game = Game()
    game.start_game()

if __name__ == "__main__":
    main()
