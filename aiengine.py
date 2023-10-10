""" The engine that will learn automatically """

from itertools import product
import random

from game import Game
from engine import PlayerEngine
from player import (
    Player,
    PlayerAttackAction,
    PlayerSplitAction,
)


class AIEngine(PlayerEngine):
    @staticmethod
    def random_move():
        move_type = random.choice([
            PlayerAttackAction,
            PlayerSplitAction,
        ])
    
    @staticmethod
    def random_attack():
        return PlayerAttackAction(
            random.randint(0, 1),
            random.randint(0, 1),
        )
    
    @staticmethod
    def random_split():
        return PlayerSplitAction([random.randint(0, 1), random.randint(0, 1)])
        
    
    def __init__(self):
        # Construct all 5^4 = 625 possible game states of a Sticks game
        # (assuming this engine is always the active players, which it will be when making a move)
        moves = {}
        for four_hands in product(*[[0, 1, 2, 3, 4]]*4):
            # Players do not need engines; they're just for hashing
            players = [Player(None), Player(None)]
            players[0].state.hands = four_hands[:2]
            players[1].state.hands = four_hands[2:]
            all_game_states[Game(players)]
        
        
        