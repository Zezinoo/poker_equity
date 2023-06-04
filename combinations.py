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
                fofak(table, card)
                print("Is tofak")
                print(card.get_face(), matched_card.get_face(),
                      t_card.get_face(), card.get_value())
                return True
        return False
    except ValueError:
        return False


def fofak(table, card, *args):
    pass
# HighCard, Pair, TwoPair , TOFAK , Straight , Flush , FullHouse , FOFAK , StraightFlush , RoyalFlush


def foo():
    bar()
    print("In foo")
    return


def bar():
    print("In bar")
    return
