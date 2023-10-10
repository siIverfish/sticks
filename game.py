"""
    Contains the 'Game' class
    Overall logic for deciding winners, switching turns, etc
"""

from dataclasses import dataclass
from typing import List

from player import Player


class Game:
    """ Overall logic for things like deciding winners & switching turns """

    @dataclass
    class State:
        """ Contains all of the data in a single Game instance """

        players: List[Player]
        active_player: Player
        other_player: Player
        
        def __hash__(self):
            return hash((
                self.players[0].state.hands[0],
                self.players[0].state.hands[1],
                self.players[1].state.hands[0],
                self.players[1].state.hands[1],
            ))

    def __init__(self, players):
        self.state = Game.State(players, players[0], players[1])

    def swap_active_player(self):
        """
            Switches whose turn it is so that the other player can attack/split
            Called once per game loop, at the end
        """
        self.state.active_player, self.state.other_player = \
            self.state.other_player,  self.state.active_player

    def game_is_over(self) -> bool:
        """ Returns 'True' if either player has boths hands equal to zero """
        return any(
            not any(player.state.hands)
            for player in self.state.players
        )

    def winner(self) -> Player:
        """
            Returns the first player that has not lost
            (at least one 'stick' on at least one hand)
            or player one if the game is not over.
        """
        return next(
            player for player in self.state.players
            if player.state.hands != [0, 0]
        )

    def play(self, *, print_state=True) -> Player:
        """
            Main game loop.
            Continues swapping active player and prompting movements
            until the game ends.

            Returns the player who won the game (self.winner).
        """
        while not self.game_is_over():
            if print_state:
                print(self)
            self.state.active_player.move(self.state)
            self.swap_active_player()

        return self.winner()

    @property
    def active_player_num(self):
        """
            Used for UI purposes.

            Returns the index of the active player, plus one.
        """
        return self.state.players.index(self.state.active_player) + 1

    def __str__(self):
        return f"Game:\n1: {self.state.players[0]}\n2: {self.state.players[1]}"
