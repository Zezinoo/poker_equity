from progressbar import progressbar
import pandas as pd
import docplex.mp.model as cpx
import eval7
from itertools import combinations, islice, chain
from pprint import pprint
from eval7 import Card


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
S_1 = 'AA,KK,QQ,JJ,AKs'
S_2 = 'TT,AQs,AJs,AKo'
S_3 = '99 ,JTs ,QJs ,ATs,AQo'
S_4 = 'T9s,KQo,88,QTs,98s,J9s,AJo,KTs'

deck = eval7.Deck()
test = list(map(Card, ('As', 'Ks', 'Qs', 'Js', 'Ts', '9s',
            '8s', '7s', '6s', '5s', '4s', '3s', '3s', '2s')))

hero_cards = ('Qs', 'Qd')

hero = list(map(Card, hero_cards))


for card in hero:
    deck.cards.remove(card)

comb = return_all_flops(deck)

r_villain = eval7.HandRange(S_2)

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
    if (len(binary) != 38):
        print(len(binary))
        pprint(flop)
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
    ERROR_BOUND = 0.2
    m = 19600  # Number of Flops
    n = 38  # Number of Features
    b = all_binaries  # nxm Matrix
#
#
# Decision Variables
##
# epsilon_i for each flop i, the error estimating it
# x_j the weight of each feature in the estimation
# y_j binary variable that determines if some constraint j is utilized or not
#
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
    print(solution.get_value_dict(x_vars))

details = opt_model.solve_details
print(details.problem_type)
print(details.status)
solution.print_mst()
#
#
#
#
#
#
#


# Catching output
# x_df = pd.DataFrame.from_dict(x_vars, orient="index",
#                              columns=["variable_object"])
# y_df = pd.DataFrame.from_dict(y_vars, orient="index",
#                              columns=["variable_object"])
# eps_df = pd.DataFrame.from_dict(eps_vars, orient="index",
#                                columns=["variable_object"])
#
# x_df["solution_value"] = x_df["variable_object"].apply(
#    lambda item: item.solution_value)
# y_df["solution_value"] = y_df["variable_object"].apply(
#    lambda item: item.solution_value)
# eps_df["solution_value"] = y_df["variable_object"].apply(
#    lambda item: item.solution_value)
#
#
# Outputs go into csv
# x_df.drop(columns=["variable_object"], inplace=True)
# x_df.to_csv("./x_optimization_solution.csv")
# y_df.drop(columns=["variable_object"], inplace=True)
# y_df.to_csv("./y_optimization_solution.csv")
# eps_df.drop(columns=["variable_object"], inplace=True)
# eps_df.to_csv("./eps_optimization_solution.csv")
