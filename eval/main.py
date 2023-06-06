import eval7
from itertools import combinations
from pprint import pprint
from eval7 import Card


def write_output(hero, villain, comb):
    file_name = hero_cards[0]+"_" + hero_cards[1]

    f = open("./outputs/" + file_name + ".txt", "x")

    for flop in list(comb):
        f.write("Hand " + str(hero) + "\n")
        f.write("###########\n")
        f.write("Flop: \n")
        f.write(str(flop)+'\n')
        f.write("Equity: \n")
        f.write(str(eval7.py_hand_vs_range_exact(hero, r_villain, flop))+"\n")

    f.close()


# Sklanksy groups
S_1 = 'AA,KK,QQ,JJ,AKs'
S_2 = 'TT,AQs,AJs,AKo'
S_3 = '99 ,JTs ,QJs ,ATs,AQo'
S_4 = 'T9s,KQo,88,QTs,98s,J9s,AJo,KTs'

deck = eval7.Deck()

hero_cards = ('As', 'Ad')

hero = list(map(Card, hero_cards))


for card in hero:
    deck.cards.remove(card)


comb = list(combinations(deck.cards, 3))
r_villain = eval7.HandRange(S_2)

write_output(hero, r_villain, comb)
