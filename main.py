import cards

possible_figures = ["A", "K", "Q", "J", "T", "9",
                    "8", "7", "6", "5", "4", "3", "2", "1"]
possible_suits = ["D", "S", "H", "C"]

possible_cards = (possible_figures, possible_suits)


def main():
    hand = cards.Hand()
    hand.deal_hand(possible_cards)
    hand.show_hand()


if __name__ == "__main__":
    main()
