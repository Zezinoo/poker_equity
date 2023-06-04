from table import Table
from hand import Hand
from card import Card
import combinations as comb

possible_figures = ["A", "K", "Q", "J", "10", "9",
                    "8", "7", "6", "5", "4", "3", "2", "1"]
possible_suits = ["D", "S", "H", "C"]
possible_cards = (possible_figures, possible_suits)


def main():
    # PairTest
    ini_hand = [Card(face=("10", "C")), Card(face=("9", "H"))]
    initial = [("A", "D"), ("A", "S"), ("A", "H"), ("A", "C"), ("10", "D")]
    ini_table = []
    for card in initial:
        ini_table.append(Card(face=card))
    ########################

    hand = Hand(initial_cards=ini_hand)
    table = Table(hand, initial_cards=ini_table)
    hand.show_hand()
    table.show_table()
    for card in hand.get_cards():
        print(card.get_value())
        print(comb.pair(table, card))
#    table.flop(possible_cards)
#    table.turn(possible_cards)
#    table.river(possible_cards)


if __name__ == "__main__":
    main()
