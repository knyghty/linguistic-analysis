from . import deps


def lla(target, prime):
    counter = 0
    for token in target:
        counter += prime.count(token)

    try:
        return counter / (len(prime) * len(target))
    except ZeroDivisionError:
        return 1.0


def lilla(target, prime):
    return lla(target, prime)


def silla(target, prime):
    return lla(deps.subtrees(target), deps.subtrees(prime))
