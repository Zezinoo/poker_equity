import eval7
from eval7 import Card
from itertools import combinations
from numpy import random


S_1 = 'AA,KK,QQ,JJ,AKs'
S_2 = 'TT,AQs,AJs,AKo'
S_3 = '99 ,JTs ,QJs ,ATs,AQo'
S_4 = 'T9s,KQo,88,QTs,98s,J9s,AJo,KTs'

deck = eval7.Deck()
comb = list(combinations(deck, 3))

hero_cards = ('Qs', 'Qd')

hero = list(map(Card, hero_cards))

for card in hero:
    deck.cards.remove(card)


r_villain = eval7.HandRange(S_2)
acc = 0
for flop in comb:
    acc += eval7.py_hand_vs_range_exact(hero, r_villain, flop)
base = acc*(1/19600)
print(base)
