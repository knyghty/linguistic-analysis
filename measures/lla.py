from . import deps


def lla(target, prime):
    counter = 0
    for token in target:
        counter += prime.count(token)

    return counter / (len(prime) * len(target))


def lilla(target, prime):
    return lla(target, prime)


def silla(target, prime):
    return lla(deps.subtrees(target), deps.subtrees(prime))
