from hand import Hand
from table import Table
from utils import int_parse

possible_figures = ["A", "K", "Q", "J", "T", "9",
                    "8", "7", "6", "5", "4", "3", "2", "1"]
possible_suits = ["D", "S", "H", "C"]
possible_cards = (possible_figures, possible_suits)


def main():

    hand = Hand()
    table = Table(hand)
    hand.deal_hand(possible_cards)
    hand.show_hand()
    table.flop(possible_cards)
    table.turn(possible_cards)
    table.river(possible_cards)
    print(int_parse("A"), int_parse("D"))


if __name__ == "__main__":
    main()
