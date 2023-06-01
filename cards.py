import numpy as np
from numpy import random


class Hand:

    def __init__(self):
        self.__cards = []
        self.__equity = 0

    def show_hand(self):
        for card in self.__cards:
            print(f"{card[0][0]},{card[1][0]}", end=" | ")

    def deal_hand(self, possible_cards):
        for i in range(len(possible_cards)):
            self.__cards.append(
                (random.choice(possible_cards[0], 1), random.choice(possible_cards[1], 1)))
        while self.__cards[0] == self.__cards[1]:
            self.deal_hand(self, possible_cards[0], possible_cards[1])
            return

    def calculate_equity(self):
        pass
