#!/usr/bin/python3
"""
raffle_game.py: This module contains a defination of RaffleGame class.
"""

import random
from models.raffle import Raffle


class RaffleGame(Raffle):
    """
    Raffle: A model that that contains neccessary attributes
        and methods to manage multitple RaffleGames
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.update(**kwargs)
        self.state = self.raffle.states[0]
        self.participants = {}
        self.new_participants = []
        self.total_amount = 0
        self.go = False

    

    def add_participant(self, user_unique_id, gift_count):
        """
        add_participant: Adds a participand in a RaffleGame
            instance.

        Args:
            user_unique_id (:str:): The user's unique ID.
            gift_count (:int:): The gift the user
        """
        if self.state == self.raffle.states[1] or self.state == self.raffle.states[2]:
            print("Raffle has already started.\nCan't add user")
            return
        if user_unique_id not in self.participants.keys():
            print("New Participant Added: ", user_unique_id)
            self.new_participants.append(user_unique_id)
        self.participants[user_unique_id] = \
            self.participants.get(user_unique_id, 0) + gift_count
        self.total_amount += gift_count
        
        print(f"Total gifts: {self.total_amount}\nTotal Participant: {len(self.participants)}")
        
        self.save()

    def if_ready_start(self):
        """
        if_ready_start: checks if the raffle game is ready to
            start and if it's ready it will start the game.

        Return:
            True if ready else False is returned.
        """
        if len(self.participants) < self.raffle.viewers / 100 * self.raffle.min_participant:
            print("Not enough participants for the raffle!.")
            return
        elif (self.state != self.raffle.states[0]):
            print(self.state)
            print("Raffle has already started!.")
            return

        self.go = True

    def start(self):
        """
        starts: starts the raffle game.
        """
        self.raffle.delay = True
        self.state = self.raffle.states[1]
        
        print("Participants and their total gifts:")
        
        for participant, gifts in self.participants.items():
            print(f"\t@{participant} ------------ {gifts} Gifts")
        
        self.winner = self.raffle.winner = \
            random.choice(list(self.participants.keys()))
        self.raffle.last_winner = self.raffle.winner
        
        print(f"\nCongratulations! @{self.winner} has won with a total of {self.total_amount} gifts!\n")
        
        self.state = self.raffle.states[2]
    
    def is_gift_eligible(self, gift_event):
        """
        is_gift_elegible: Checks if a sent gift is eligible for Raffle entry

        Args:
            gift_event (:obj:): The gift event that was sent.

        Return:
            True if eligible else False is returned.
        """
        cond = (gift_event.gift.info.name == self.raffle.required_gift and
                gift_event.gift.count >= self.raffle.required_gift_amount)
        
        print (f"Checking if gift is eligible: {cond}")
        
        return (cond)

    def get_new_participants(self):
        new_participants = self.new_participants.copy()
        self.new_participants = []
        return (new_participants)
