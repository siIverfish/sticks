""" Ties together modules & runs program with user-controlled players """

from player import Player
from engine import UserControlled
from game import Game


game = Game([
    Player(UserControlled),
    Player(UserControlled),
])

game.play()
