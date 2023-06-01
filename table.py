from numpy.random import choice


class Table(object):
    def __init__(self, hand):
        self.__something = []
        self.__hand = hand

    def turn_card(self, possible_cards):
        card = (choice(possible_cards[0]), choice(possible_cards[1]))
        return card

    def flop(self, possible_cards):
        for i in range(3):
            card = self.turn_card(possible_cards)
            while card in self.__something or card in self.__hand.get_cards():
                card = self.turn_card(possible_cards)
            self.__something.append(card)
        print("Flop")
        self.show_table()

    def turn(self, possible_cards):
        card = self.turn_card(possible_cards)
        while card in self.__something or card in self.__hand.get_cards():
            card = self.turn_card(possible_cards)
        self.__something.append(card)
        print("Turn")
        self.show_table()

    def river(self, possible_cards):
        card = self.turn_card(possible_cards)
        while card in self.__something or card in self.__hand.get_cards():
            card = self.turn_card(possible_cards)
        self.__something.append(card)
        print("River")
        self.show_table()

    def show_table(self):
        print("Cartas na mesa")
        for card in self.__something:
            print(card, " | ")
