from utils import int_parse


class Card():

    def __init__(self, face=()):
        self.__value = 0 if face == () else int_parse(face[0])
        self.__face = face

    def pick_card(self, possible_cards):
        from numpy.random import choice
        from utils import int_parse
        self.__face = (choice(possible_cards[0], 1)[0],
                       choice(possible_cards[1], 1)[0])
        self.__value = int_parse(choice(possible_cards[1], 1))

    def get_value(self):
        return self.__value

    def get_face(self):
        return self.__face
