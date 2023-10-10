"""
    Contains the Player class and related objects
"""

from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod


class Player:
    """
        Contains data for number of 'sticks' on each 'hand'

        Logic for implementing attacking other player and splitting
        sticks between hands.
        All decision logic is handled by encapsulated PlayerEngine element.

        PlayerAction instances are received from the PlayerEngine and then
        converted here to actual game movement.
        e.g. adding to the other player's hand after a hit
    """

    @dataclass
    class State:
        """ Contains the data in a Player instance """
        hands: List[int]
        engine: "PlayerEngine"

    def __init__(self, engine):
        self.state = Player.State([1, 1], engine(self))

    def move(self, game_state):
        """
            High-level interface that causes the player to:
            1. Make a decision on which move to make with PlayerEngine
            2. Execute the move, changing the game state
        """
        next_move = self.state.engine.move(game_state)
        self.execute(next_move, game_state)

    def execute(self, action, game_state):
        """
            Uses the information from the PlayerAction to
            change the game state accordingly--'Plays' the action
        """
        if not action.is_valid(game_state):
            return ValueError(f"Invalid action: {action} based on game state {game_state}")
            
        action.callable(self, game_state, *list(action.__dict__.values())[:-1])

    def attack(self, game_state, self_pos, other_pos):
        """ Executes an 'attack' on the other player """
        other = game_state.other_player

        other.state.hands[other_pos] += self.state.hands[self_pos]

        if other.state.hands[other_pos] >= 5:
            other.state.hands[other_pos] = 0

    def split(self, _game_state, new_hands):
        """ Executes a split action, changing hand arrangement """

        self.state.hands = list(new_hands)

    def __str__(self):
        return f"Player: {'| ' * self.state.hands[0]}   " + \
                       f"{'| ' * self.state.hands[1]}"

@dataclass
class PlayerAction(ABC):
    """ Represents an action any player can take """
    
    @abstractmethod
    def is_valid(self, _game_state):
        pass


@dataclass
class PlayerAttackAction(PlayerAction):
    """ An action of attacking the other hands """
    self_pos: int
    other_pos: int

    callable = Player.attack
    
    def is_valid(self, game_state):
        """ Makes sure both hands involved in the attack aren't 'dead' """
        return all(
            hand > 0 for hand in
            [
                game_state.active_player.state.hands[self.self_pos], 
                game_state.other_player.state.hands[self.other_pos]
            ]
        )


@dataclass
class PlayerSplitAction(PlayerAction):
    """ Rearranges the player's hand """
    new_hands: List[int]

    callable = Player.split

    def is_valid(self, game_state):
        """
            Checks to make sure the new configuration is valid:
                - sums are the same, e.g. no splitting from 1/0 into 4/4
                - all new hands are valid numbers e.g. no splitting from 3/4
                    into 5/2
                - it's not the same, e.g. 2/3 to 2/3 OR 2/3 to 3/2
        """
        return sum(self.new_hands) == sum(game_state.active_player.state.hands) and \
            all(hand < 5 for hand in self.new_hands) and \
            sorted(self.new_hands) != sorted(game_state.active_player.state.hands)