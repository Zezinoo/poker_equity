from progressbar import progressbar
import numpy as np
import eval7
import pandas as pd
import docplex.mp.model as cpx
from itertools import combinations, islice, chain
from pprint import pprint
from eval7 import Card


def do_all(cards: tuple, bound: float, rng: str):

    def window(seq, n=2):
        "Returns a sliding window (of width n) over data from the iterable"
        "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    def missing_elements(L):
        L.sort()
        missing = chain.from_iterable(range(x + 1, y)
                                      for x, y in window(L) if (y - x) > 1)
        return list(missing)

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

    def return_all_flops(deck):
        comb = list(combinations(deck.cards, 3))
        return comb

# Sklanksy groups
    group_name = ""

    S_1 = 'AA,KK,QQ,JJ,AKs'
    S_2 = 'TT,AQs,AJs,AKo'
    S_3 = '99 ,JTs ,QJs ,ATs,AQo'
    S_4 = 'T9s,KQo,88,QTs,98s,J9s,AJo,KTs'

    if rng == S_1:
        group_name = "S_1"
    elif rng == S_2:
        group_name = "S_2"
    elif rng == S_3:
        group_name = "S_3"
    elif rng == S_4:
        group_name = "S_4"

    deck = eval7.Deck()

    hero_cards = (cards[0], cards[1])

    hero = list(map(Card, hero_cards))

    for card in hero:
        deck.cards.remove(card)

    comb = return_all_flops(deck)

    r_villain = eval7.HandRange(rng)

# Defining features
# Initializing binary array
    binary = []
    all_binaries = []
    flop = []
    h_suits = [card.suit for card in hero]
    h_ranks = [card.rank for card in hero]
# Individual Broadway F1-15

    def check_i_broadway(f_ranks, binary, rank):
        acc = 0
        for rank in f_ranks:
            if card.rank == rank:
                acc += 1
        if acc == 0:
            binary.extend([0, 0, 1])
        elif acc == 1:
            binary.extend([1, 0, 0])
        elif acc >= 2:
            binary.extend([1, 1, 0])

    def check_suits(f_suits, f_rank, binary, flop):
        temp = set(f_suits)
        suits = len(temp)
        if suits == 1:
            binary.extend([1, 0, 0, 0])
        elif suits == 2:
            for card in flop:
                if card.rank == 12 and f_suits.count(card.suit) == 2:
                    binary.extend([0, 1, 0, 1])
                    return
            else:
                binary.extend([0, 1, 0, 0])

        elif suits == 3:
            binary.extend([0, 0, 1, 0])

# Ranks

    def check_ranks(f_ranks, binary):
        temp = set(f_ranks)
        ranks = len(temp)
        if ranks == 1:
            binary.extend([1, 0, 0])
        elif ranks == 2:
            binary.extend([0, 1, 0])
        elif ranks == 3:
            binary.extend([0, 0, 1])

# Paint

    def check_paint(f_ranks, binary):
        temp = [rank for rank in f_ranks if rank > 8]
        paints = len(temp)
        if paints == 1:
            binary.extend([1, 0, 0])
        elif paints == 2:
            binary.extend([0, 1, 0])
        elif paints == 3:
            binary.extend([0, 1, 1])
        else:
            binary.extend([0, 0, 0])

# Broadways

    def check_broadway(f_ranks, binary):
        temp = [rank for rank in f_ranks if rank > 7]
        broadways = len(temp)
        if broadways == 0:
            binary.extend([1, 0, 0, 0])
        elif broadways == 1:
            binary.extend([0, 1, 0, 0])
        elif broadways == 2:
            binary.extend([0, 1, 1, 0])
        elif broadways == 3:
            binary.extend([0, 1, 1, 1])

# Card Size

    def check_cards_size(f_ranks, binary):
        medium = [rank for rank in f_ranks if rank < 8 and rank > 4]
        small = [rank for rank in f_ranks if rank < 5]
        if len(medium) == 3:
            binary.extend([1, 0, 0, 0])
        elif len(small) == 3:
            temp = set(small)
            if len(temp) == 3:
                if '4' not in temp:
                    binary.extend([0, 1, 0, 1])
            else:
                binary.extend([0, 1, 0, 0])
        elif len(small) + len(medium) == 3:
            binary.extend([0, 0, 1, 0])
        else:
            binary.extend([0, 0, 0, 0])

# Straight

    def check_straight(f_ranks, binary):
        temp = missing_elements(f_ranks)
        gaps = len(temp)
        if gaps == 0:
            binary.extend([1, 0, 0, 0, 0])
        elif gaps == 1:
            binary.extend([0, 1, 0, 0, 0])
        elif gaps == 2:
            binary.extend([0, 0, 1, 0, 0])
        elif gaps == 3:
            binary.extend([0, 0, 0, 1, 0])
        elif gaps > 3:
            binary.extend([0, 0, 0, 0, 1])

# Hand Dependent Features F39-73

    def h_check_flush(h_suits, f_suits, binary):
        all_suits = h_suits + f_suits
        n_f_suits = len(set(f_suits))
        n_all_suits = len(set(all_suits))
        tmp = []
        tmp.append(1) if (n_f_suits != 1 and n_all_suits >=
                          3) else tmp.append(0)
        tmp.append(1) if (n_all_suits <= 2) else tmp.append(0)
        tmp.append(1) if (n_f_suits == 1 and list(set(f_suits))
                          [0] not in h_suits) else tmp.append(0)
        tmp.append(1) if (n_f_suits == 2 and bool(
            set(h_suits) & set(f_suits))) else tmp.append(0)
        tmp.append(1) if (n_all_suits == 1) else tmp.append(0)
        binary.extend(tmp)

# I need duplicates in a dict of the form {rank : count}

    def h_check_made_hands(h_ranks, f_ranks, binary):
        n_f_ranks = len(set(f_ranks))
        all_ranks = h_ranks + f_ranks
        n_all_ranks = len(set(all_ranks))
        dups = {i: all_ranks.count(i)
                for i in all_ranks if all_ranks.count(i) > 1}
        v_d = list(dups.values())
        v_k = list(dups.keys())

        # is4 or FH
        binary.append(1) if (4 in v_d or (
            3 in v_d and 2 in v_d)) else binary.append(0)
        # is3
        binary.extend([1, 1]) if (3 in v_d and v_k[v_d.index(3)]
                                  ) else binary.extend([0, 0])
        # isPair
        binary.append(1) if (2 in v_d) else binary.append(0)
        # isTwo
        binary.append(1) if (v_d.count(2) == 2) else binary.append(0)
        # top/middle/bottom/pair something wrong, not checking all pairs
        if (2 in v_d):
            binary.append(1) if (v_k[v_d.index(2)] <= 4) else binary.append(0)
            binary.append(1) if (v_k[v_d.index(2)] <=
                                 8 and v_k[v_d.index(2)] > 4) else binary.append(0)
            binary.append(1) if (v_k[v_d.index(2)] > 8) else binary.append(0)
        else:
            binary.extend([0, 0, 0])
        if (2 in v_d or 3 in v_d):
            if n_f_ranks == 3:
                binary.extend([1, 0])
            elif n_f_ranks == 2:
                binary.extend([0, 1])
            else:
                binary.extend([0, 0])
        else:
            binary.extend([0, 0])

    def h_check_overcards(h_ranks, f_ranks, binary):
        h_high = max(h_ranks)
        f_high = max(f_ranks)
        h_over = len([rank for rank in h_ranks if rank > f_high])
        f_over = len([rank for rank in f_ranks if rank > h_high])
        temp = []

        if f_over == 0:
            temp = [0, 0, 0]
        elif f_over == 1:
            temp = [0, 1, 0]
        elif f_over >= 2:
            temp = [0, 0, 1]
        else:
            temp = [0, 0, 0]

        if h_over == 1:
            temp += [1, 0]
        elif h_over == 2:
            temp += [0, 1]
        else:
            temp += [0, 0]

        binary.extend(temp)

    def h_check_straight(h_ranks, f_ranks, binary):
        all_ranks = h_ranks + f_ranks
        all_ranks = sorted(all_ranks)
        diffs = list(np.diff(all_ranks))
        tmp = []
        binary.append(1) if (np.sum(diffs) == 4) else binary.append(0)

        if (diffs.count(1) == 3):
            binary.extend([1, 0]) if (min(all_ranks) in h_ranks
                                      ) else binary.extend([0, 1])
        else:
            binary.extend([0, 0])
        # Inside Straights
        if (diffs.count(1) == 3):
            if diffs.count(2) == 1:
                binary.extend([1, 0])
            elif diffs.count(2) == 2:
                binary.extend([0, 1])
            else:
                binary.extend([0, 0])
        else:
            binary.extend([0, 0])
        # Not exactly according to article F64/F65
        if (diffs.count(1) + diffs.count(2) + diffs.count(3) == 2):
            binary.extend([1, 1, 0])
        else:
            binary.extend([0, 0, 0])

    def h_check_draw_comb(h_ranks, f_ranks, h_suits, f_suits, binary):
        all_ranks = h_ranks + f_ranks
        all_ranks = sorted(all_ranks)
        all_suits = h_suits + f_suits
        all_suits = sorted(all_suits)
        s_diffs = list(np.diff(all_suits))
        diffs = list(np.diff(all_ranks))
        h_high = max(h_ranks)
        f_high = max(f_ranks)
        h_over = len([rank for rank in h_ranks if rank > f_high])
        f_over = len([rank for rank in f_ranks if rank > h_high])

        # Inside Straights
        if (diffs.count(1) == 3 or diffs.count(2) == 2):
            binary.append(1) if (h_over == 0) else binary.append(0)
            binary.append(1) if (h_over == 1) else binary.append(0)
            binary.append(1) if (h_over == 2) else binary.append(0)
            binary.append(1) if (s_diffs.count(1) + s_diffs.count(2) +
                                 s_diffs.count(3) == 2 and len(set(f_suits)) >= 2) else binary.append(0)
            binary.append(1) if (len(set(all_suits))
                                 <= 2) else binary.append(0)
        else:
            binary.extend([0, 0, 0, 0, 0])

        binary.append(1) if (len(set(all_suits)) <=
                             2 and h_over == 1) else binary.append(0)
        binary.append(1) if (len(set(all_suits)) <=
                             2 and h_over == 2) else binary.append(0)


# Testing
    for flop in comb:

        binary = []
        f_suits = [card.suit for card in flop]
        f_ranks = [card.rank for card in flop]

        # F1-15
        # Aces
        check_i_broadway(flop, binary, 12)
# Kings
        check_i_broadway(flop, binary, 11)
# Queens
        check_i_broadway(flop, binary, 10)
# Jacks
        check_i_broadway(flop, binary, 9)
# Tens
        check_i_broadway(flop, binary, 8)
# Suits
        check_suits(f_suits, f_ranks, binary, flop)
# Ranks
        check_ranks(f_ranks, binary)
# Paint
        check_paint(f_ranks, binary)
# Check Broadway
        check_broadway(f_ranks, binary)
# Cards Size
        check_cards_size(f_ranks, binary)
# Straight
        check_straight(f_ranks, binary)
# Flush
        h_check_flush(h_suits, f_suits, binary)
#
        h_check_made_hands(h_ranks, f_ranks, binary)
#
        h_check_overcards(h_ranks, f_ranks, binary)
#
        h_check_straight(h_ranks, f_ranks, binary)
#
        h_check_draw_comb(h_ranks, f_ranks, h_suits, f_suits, binary)
        if len(binary) != 73:
            pprint(flop)
            print(len(binary))
# Eval
        binary.append(eval7.py_hand_vs_range_exact(hero, r_villain, flop))
        all_binaries.append(binary)
        binary = []


# Modelo
    for i in progressbar(range(100)):
        #
        #    opt_model = cpx.Model(name="AVGERROR Model")
        opt_model = cpx.Model(name="MINFEATURES")
# Parameters
        N_FEATURES = 10
        ERROR_BOUND = bound
        m = 19600  # Number of Flops
        n = 73  # Number of Features
        b = all_binaries  # nxm Matrix
#
#
# Decision Variables
##
# epsilon_i for each flop i, the error estimating it
# x_j the weight of each feature in the estimation
# y_j binary variable that determines if some constraint j is utilized or not
# epsilon is real nonnegative
#
        eps_vars = {i: opt_model.continuous_var(
            lb=0, name="eps_{0}".format(i)) for i in range(m)}

# x_j is real , and a probability
#
        x_vars = {j: opt_model.continuous_var(
            lb=-1, ub=1, name="x_{0}".format(j)) for j in range(n)}
# y_j is binary
        y_vars = {j: opt_model.binary_var(
            name="y_{0}".format(j)) for j in range(n)}
#
# Constraint 2
        xy_leq_constraints = {j:
                              opt_model.add_constraint(
                                  ct=x_vars[j] <= y_vars[j],
                                  ctname="xy_cstr{0}".format(j))
                              for j in range(n)
                              }

        xy_geq_constraints = {j:
                              opt_model.add_constraint(
                                  ct=x_vars[j] >= - y_vars[j],
                                  ctname="xy_cstr{0}".format(j))
                              for j in range(n)
                              }
# Constraint 3
#    y_leq_constraints = {j :
#                         opt_model.add_constraint(
#                             ct=y_vars[j] <= N_FEATURES,
#                             ctname="y_cstr{0}".format(j))
#                         for j in range(n)}
# Constraint 6

        eps_leq_constraints = {i:
                               opt_model.add_constraint(
                                   ct=opt_model.sum(b[i][j] * x_vars[j]
                                                    for j in range(n))
                                   <= b[i][-1] + eps_vars[i],
                                   ctname="eps_cstr{0}".format(i))
                               for i in range(m)}
        eps_geq_constraints = {i:
                               opt_model.add_constraint(
                                   ct=opt_model.sum(b[i][j] * x_vars[j]
                                                    for j in range(n))
                                   >= b[i][-1] - eps_vars[i],
                                   ctname="eps_cstr{0}".format(i))
                               for i in range(m)}

# Constraint 7
        opt_model.add_constraint(ct=(
            1/m)*opt_model.sum(eps_vars[i] for i in range(m)) <= ERROR_BOUND, ctname="csrt7")

# Objective function for AVGERROR

#    objective = (1/m)*opt_model.sum(eps_vars[i] for i in range(m))

# Objective function for FEAT_AVGERROR
        objective = opt_model.sum(y_vars[j] for j in range(n))

        opt_model.minimize(objective)

# Solving
        solution = opt_model.solve()
        details = opt_model.solve_details
        print(details.problem_type)
        print(details.status)
        if details.status == "integer infeasible":
            return

#    with open("{0}_E_{1}_{2}.txt".format(str(cards), str(bound), group_name), "w") as sys.stdout:
#        solution.print_mst()
#        sys.stdout.close()
    solution.print_mst()
    obj_value = solution.get_objective_value()
    with open("{0}_E_{1}_{2}.txt".format(str(cards), str(bound), group_name), "w") as f:
        f.write(str(obj_value))
        f.close()
#

#
#
#
#
#
#


# Catching output

# x_output

    x_df = pd.DataFrame.from_dict(x_vars, orient="index",
                                  columns=["variable_object"])
    x_df.index = pd.Index(x_df.index)
    x_df.reset_index(inplace=True)
    x_df["solution_value"] = x_df["variable_object"].apply(
        lambda item: item.solution_value)

    x_df.drop(columns=["variable_object"], inplace=True)
    x_df.to_csv(
        "./73_outs/2{0}_E_{1}_{2}ximization_solution.csv".format(str(cards), str(bound), group_name))

# y output

    y_df = pd.DataFrame.from_dict(y_vars, orient="index",
                                  columns=["variable_object"])
    y_df.index = pd.Index(y_df.index)
    y_df.reset_index(inplace=True)
    y_df["solution_value"] = y_df["variable_object"].apply(
        lambda item: item.solution_value)

    y_df.drop(columns=["variable_object"], inplace=True)
    y_df.to_csv(
        "./73_outs/2{0}_E_{1}_{2}yimization_solution.csv".format(str(cards), str(bound), group_name))

# eps_output

    eps_df = pd.DataFrame.from_dict(eps_vars, orient="index",
                                    columns=["variable_object"])
    eps_df.index = pd.Index(eps_df.index)
    eps_df.reset_index(inplace=True)
    eps_df["solution_value"] = eps_df["variable_object"].apply(
        lambda item: item.solution_value)

    eps_df.drop(columns=["variable_object"], inplace=True)
    eps_df.to_csv(
        "./73_outs/2{0}_E_{1}_{2}epsimization_solution.csv".format(str(cards), str(bound), group_name))
#
