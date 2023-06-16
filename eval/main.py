from progressbar import progressbar
import eval7
import pandas as pd
import docplex.mp.model as cpx
from itertools import combinations, islice, chain
from pprint import pprint
from eval7 import Card
import numpy as np

from eqcalc import do_all


def main(tests):
    S_1 = 'AA,KK,QQ,JJ,AKs'
    S_2 = 'TT,AQs,AJs,AKo'
    S_3 = '99 ,JTs ,QJs ,ATs,AQo'
    S_4 = 'T9s,KQo,88,QTs,98s,J9s,AJo,KTs'

    for test in tests:
        cards = test[0]
        bound = test[1]
        rng = test[2]
        group = []
        if rng == "S_1":
            group = S_1
        elif rng == "S_2":
            group = S_2
        elif rng == "S_3":
            group = S_3
        elif rng == "S_4":
            group = S_4
        do_all(cards, bound, group)


if __name__ == "__main__":
    all_cards = [("Ks", "Kc"), ("Qs", "Qc"), ("Ks", "Kc"), ("As", "Ks")]
    all_rngs = ["S_1"]
    tests = [(card, i, rng) for i in [0.01, 0.05, 0.1, 0.15, 0.2]
             for card in all_cards for rng in all_rngs]
    print(tests)

    main(tests)
