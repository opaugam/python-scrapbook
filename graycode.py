from copy import copy

def generate(n):
    assert n, 'n must be strictly positive'
    if n == 1:
        return [0, 1]

    prv = generate(n - 1)
    tmp = copy(prv)
    return prv + [(1<<(n-1)) | code for code in tmp[::-1]]