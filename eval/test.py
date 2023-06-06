from itertools import islice, chain


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


L = [5, 6, 3]
print(missing_elements(L))
