from table import Table


def pair(table: Table, card, *args):
    table_cards = table.get_table_cards()
    for t_card in table_cards:
        if t_card.get_value() == card.get_value():
            is_tofak = tofak(table, card, table_cards, t_card)
            if is_tofak:
                return
            else:
                print("Is pair")
                print(card.get_face(), t_card.get_face(), t_card.get_value())
    print("No pair")
    return


def tofak(table, card, *args):
    table_cards = args[0]
    matched_card = args[1]
    try:
        table_cards.remove(matched_card)
        for t_card in table_cards:
            if t_card.get_value() == card.get_value():
                is_fofak = fofak(table, card, table_cards,
                                 t_card, matched_card)
                if is_fofak:
                    return
                else:
                    print("Is tofak")
                    print(card.get_face(), matched_card.get_face(),
                          t_card.get_face(), card.get_value())
                    return True
        return False
    except ValueError:
        return False


def fofak(table, card, *args):
    table_cards = args[0]
    second_match = args[1]
    first_match = args[2]
    try:
        table_cards.remove(second_match)
        for t_card in table_cards:
            if t_card.get_value() == card.get_value():
                fofak(table, card)
                print("Is tofak")
                print(card.get_face(), second_match.get_face(),
                      t_card.get_face(), first_match.get_face(), card.get_value())
                return True
        return False
    except ValueError:
        return False


def flush(table, card, *args):
    table_suit = []
    for card in table.get_table_cards():
        table_suit.append(card.get_face[1])
    dup_rank = {i: table_suit.count(i) for i in table_suit}
    if 4 in list(dup_rank.values()):
        cur_suit = list(dup_rank.keys())[list(dup_rank.values()).index(4)]
        print("Is flush")
        print(cur_suit)

# HighCard, Pair, TwoPair , TOFAK , Straight , Flush , FullHouse , FOFAK , StraightFlush , RoyalFlush
