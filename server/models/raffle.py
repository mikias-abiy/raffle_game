#!/usr/bin/python3
"""
raffle.py: This module contains a defination of Raffle class.
"""

import raffle_config as config
from models.base_model import BaseModel

class Raffle(BaseModel):
    """
    Raffle: A model that that contains neccessary attributes
        and methods to manage multitple RaffleGames
    """
    
    def __init__ (self, *args, **kwargs):
        super().__init__()
        if self.__class__.__name__ == "Raffle":
            self.update(**kwargs)
            self.min_participant = config.MIN_PARTICIPANT # specified in percent of currently viewing users.
            self.required_gift = config.RAFFLE_GIFT_TYPE
            self.required_gift_amount = config.MINIMUM_GIFT_AMOUNT
            self.raffle_fee = 0
            self.states = ["WAITING", "ACTIVE", "ENDED"]
            self.state = self.states[0]
            self.raffle_games = []
            self.current_game = None
            self.winner = None
            self.last_winner = None
            self.viewers = 0
            self.tiktok_client = None
            self.delay = False
            self.websocket = None
            self.stop = False

    def set_game(self, game):
        if self.current_game:
            self.raffle_games.append(self.current_game)
        self.current_game = game
