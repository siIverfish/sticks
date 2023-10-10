""" The decision-making engines behind the Player instances. """

from abc import ABC, abstractmethod
from dataclasses import dataclass

from player import (
    PlayerAttackAction,
    PlayerSplitAction,
    PlayerAction,
)

class PlayerEngine(ABC):
    """ Interface for all engines """

    @abstractmethod
    def move(self, game_state) -> "PlayerAction":
        """ Returns a PlayerAction based on the current board state. """


class UserControlled(PlayerEngine):
    """
        A player engine whose decision-making uses a
        human typing things in the terminal
    """

    def __init__(self, player):
        self.player = player

    def attack_ui(self, game_state) -> "PlayerAttackAction":
        """
            Prompts the player to fill in the details of the attack move.
            Packages & returns the data as a PlayerAttackAction object.
        """
        self_pos = input("Which hand attacks? (l/r)") == "r"
        other_pos = input("Which hand is attacked? (l/r)") == "r"
        other_player = next(
            p for p in game_state.players if p is not self.player
            )

        return PlayerAttackAction(
            self_pos,
            other_player,
            other_pos,
        )

    def split_ui(self, _) -> "PlayerSplitAction":
        """
            Prompts the player to fill in the details of the split move.
            Does not use the game state (2nd argument).
            Packages & returns the data as a PlayerSplitAction object.
        """
        new_hands = [
            int(input("New left hand: ")),
            int(input("New right hand: ")),
        ]

        return PlayerSplitAction(new_hands)

    def player_number(self, game_state):
        """ Finds the attached player's number in the game for UI purposes. """
        return game_state.players.index(self.player) + 1

    def move(self, game_state) -> PlayerAction:
        print(f"Player #{self.player_number(game_state)}'s turn:")

        if input("Attack or split? (a/s)").strip().lower() == "a":
            return self.attack_ui(game_state)
        else:
            return self.split_ui(game_state)
