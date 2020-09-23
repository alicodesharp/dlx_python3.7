from functools import reduce
from .combfuncs import binom


def rank(B, K):
    """Return the rank of k-subset K in base set B."""
    """ Subset ranking yöntemlerinden birisi """
    v = (B if type(B) == int else len(B[0]))
    block = (K if type(B) == int else [B[1][i] for i in K])
    k = len(block)
    r = binom(v, k)
    for i in range(k):
        r -= binom(v - block[i] - 1, k - i)
    return r - 1


def unrank(B, k, rk):
    """Return the k-subset of rank rk in base set B."""

    v = (B if type(B) == int else len(B[0]))

    K = [0] * k
    vi = binom(v, k)
    j = v
    ki = k
    s = rk + 1
    for i in range(k - 1):
        while s > vi - binom(j, ki):
            j -= 1
        K[i] = v - j - 1
        s += binom(j + 1, ki) - vi
        ki -= 1
        vi = binom(j, ki)
    K[k - 1] = v + s - vi - 1

    return K if type(B) == int else [B[0][i] for i in K]


def succ(B, K):
    """Return the successor of the k-subset K in base set B.
    If there is no successor, we return None."""

    retcode = None
    v = (B if type(B) == int else len(B[0]))
    Kn = (K[:] if type(B) == int else [B[1][i] for i in K])

    k = len(K)
    for i in range(k - 1, -1, -1):
        Kn[i] += 1
        if Kn[i] < v and Kn[i] + (k - i) <= v:
            Kn[i + 1:] = [Kn[i] + j - i for j in range(i + 1, k)]
            retcode = Kn
            break

    if retcode is None:
        return retcode
    return Kn if type(B) == int else [B[0][i] for i in Kn]


def all(B, k):
    """A generator to create all k-subsets over the specified base set B."""
    # Check to make sure that we can return subsets, i.e. there are enough
    # elements to satisfy.
    lenB = (B if type(B) == int else len(B[0]))
    if lenB < k:
        return

    # Make the base set, creating a copy of B if B is a pair as described in
    # the module introduction; thus, if B changes, the iterator does not
    # become invalid.
    Bn = (B if type(B) == int else (B[0][:], dict(B[1])))
    K = list(range(k) if type(B) == int else Bn[0][:k])
    while K is not None:
        yield K
        K = succ(Bn, K)
