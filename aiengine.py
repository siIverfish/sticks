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
    def random_valid_move(game_state):
        move = AIEngine.random_move()
        while not move.is_valid(game_state):
            move = AIEngine.random_move()
        return move
    
    
    @staticmethod
    def random_move():
        return random.choice([
            AIEngine.random_attack,
            AIEngine.random_split,
        ])()
        
    
    @staticmethod
    def random_attack():
        return PlayerAttackAction(
            random.randint(0, 1),
            random.randint(0, 1),
        )
    
    @staticmethod
    def random_split():
        return PlayerSplitAction([random.randint(0, 4), random.randint(0, 4)])
        
    
    def __init__(self):
        # Construct all 5^4 = 625 possible game states of a Sticks game
        # (assuming this engine is always the active players, which it will be when making a move)
        self.moves = {}
        for four_hands in product(*[[0, 1, 2, 3, 4]]*4):
            # These players do not need engines; they're just for hashing
            print(four_hands)
            players = [Player(lambda _: None), Player(lambda _: None)]
            players[0].state.hands = four_hands[:2]
            players[1].state.hands = four_hands[2:]
            game = Game(players)
            if game.game_is_over():
                continue
            self.moves[game.state] = AIEngine.random_valid_move(game.state)
    
    def move(self, game_state):
        return self.moves[game_state]