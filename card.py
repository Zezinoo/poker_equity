class Card():

    def __init__(self):
        self.__value = 0
        self.__face = ()

    def pick_card(self, possible_cards):
        from numpy.random import choice
        from utils import int_parse
        self.__face = (choice(possible_cards[0], 1),
                       choice(possible_cards[1], 1))
        self.__value = int_parse(choice(possible_cards[1], 1))
