from card import Card


class Hand:

    def __init__(self, initial_cards=[]):
        self.__cards = initial_cards
        self.__equity = 0

    def show_hand(self):
        print("Cartas na mão")
        for card in self.__cards:
            print(
                f"{card.get_face()[0]},{card.get_face()[1]}", end=" | ")
        print("")

    def deal_hand(self, possible_cards):
        for i in range(len(possible_cards)):
            card = Card()
            card.pick_card(possible_cards)
            self.__cards.append(card)
        while self.__cards[0] == self.__cards[1]:
            self.deal_hand(self, possible_cards)
            return

    def calculate_equity(self):
        pass

    def get_cards(self):
        return self.__cards
