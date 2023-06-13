import numpy as np
h_ranks = h_suits = f_ranks = f_suits = flop = []


def window(seq, n=2):
    pass


def missing_elements(L):
    pass


def h_check_flush(h_suits, f_suits, binary):
    all_suits = h_suits + f_suits
    n_f_suits = len(set(f_suits))
    n_all_suits = len(set(all_suits))
    tmp = []
    tmp.append(1) if (n_f_suits != 1 and n_all_suits >= 3) else tmp.append(0)
    tmp.append(1) if (n_all_suits <= 2) else tmp.append(0)
    tmp.append(1) if (n_f_suits == 1 and set(f_suits)
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
    dups = {i: all_ranks.count(i) for i in all_ranks if all_ranks.count(i) > 1}
    v_d = list(dups.values())
    v_k = list(dups.keys())
    tmp = []

    # is4 or FH
    tmp.append(1) if (4 in v_d or (3 in v_d and 2 in v_d)) else tmp.append(0)
    # is3
    tmp.append(1) if (3 in v_d and v_k[v_d.index(3)]) else tmp.append(0)
    # isPair
    tmp.append(1) if (2 in v_d) else tmp.append(0)
    # isTwo
    tmp.append(1) if (v_d.count(2) == 2) else temp.append(0)
    # top/middle/bottom/pair something wrong, not checking all pairs
    if (2 in v_d):
        tmp.append(1) if (v_k[v_d.index(2)] <= 4) else tmp.append(0)
        tmp.append(1) if (v_k[v_d.index(2)] <=
                          8 and v_k[v_d.index(2)] > 4) else tmp.append(0)
        tmp.append(1) if (v_k[v_d.index(2)] > 8) else tmp.append(0)
        binary.extend(temp)
    else:
        binary.extend(temp)
        binary.extend([0, 0, 0])
    if (2 in v_d or 3 in v_d):
        if n_f_ranks == 3:
            binary.extend([1, 0])
        if n_f_ranks == 2:
            binary.extend([0, 1])


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

    if h_over == 1:
        temp += [1, 0]
    elif h_over == 2:
        temp += [0, 1]

    binary.extend(temp)


def h_check_straight(h_ranks, f_ranks, binary):
    all_ranks = h_ranks + f_ranks
    all_ranks = all_ranks.sort()
    diffs = np.diff(all_ranks)
    tmp = []
    tmp.append(1) if (np.sum(diffs) == 4) else tmp.append(0)
    binary.extend[tmp]

    if (diffs.count(1) == 3):
        binary.extend([1, 0]) if (min(all_ranks in h_ranks)
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
    # Not exactly according to article F64/F65
    if (diffs.count(1) + diffs.count(2) + diffs.count(3) == 2):
        binary.extend([1, 1, 0])
    else:
        binary.extend([0, 0, 0])


def h_check_draw_comb(h_ranks, f_ranks, h_suits, f_suits, binary):
    all_ranks = h_ranks + f_ranks
    all_ranks = all_ranks.sort()
    all_suits = h_suits + f_suits
    all_suits = all_suits.sort()
    s_diffs = np.diff(all_suits)
    diffs = np.diff(all_ranks)
    h_high = max(h_ranks)
    f_high = max(f_ranks)
    h_over = len([rank for rank in h_ranks if rank > f_high])
    f_over = len([rank for rank in f_ranks if rank > h_high])

    tmp = []
    # Inside Straights
    if (diffs.count(1) == 3 or diffs.count(2) == 2):
        tmp.append(1) if (h_over == 0) else tmp.append(0)
        tmp.append(1) if (h_over == 1) else tmp.append(0)
        tmp.append(1) if (h_over == 2) else tmp.append(0)
        tmp.append(1) if (s_diffs.count(1) + s_diffs.count(2) +
                          s_diffs.count(3) == 2 and len(set(f_suits)) >= 2) else tmp.append(0)
        tmp.append(1) if (len(set(all_suits)) <= 2) else tmp.append(0)
        tmp.append(1) if (len(set(all_suits)) <= 2 and h_over=1) else tmp.append(0)
        tmp.append(1) if (len(set(all_suits)) <= 2 and h_over=2) else tmp.append(0)

        binary.extend(tmp)
