from copy import copy

#
# - https://en.wikipedia.org/wiki/Gray_code
#


def reflected(n):
    if n == 0:
        return [0]

    if n == 1:
        return [0, 1]

    prv = reflected(n - 1)
    tmp = copy(prv)
    return prv + [(1 << (n - 1)) | code for code in tmp[::-1]]


def shifted(n):

    return [i ^ (i >> 1) for i in range(2 ** n)]


def n_ary(base, token):
    digits = []
    while token:
        digits.append(token % base)
        token /= base
   
    if not digits:
        digits = [0]
   
    gray = []
    shift = 0
    for digit in digits[::-1]:
        tmp = (digit + shift) % base
        shift += base - tmp
        gray.append(tmp)

    return gray

def n_ary_words(n):

   return [''.join([chr(65 + digit) for digit in n_ary(26, i)]) for i in range(2 ** n)]


if __name__ == '__main__':

    print reflected(5)
    print shifted(5)
    
    #
    # - fun: generate tokens in base-26 (A-Z) using n-ary gray codes
    #
    print(n_ary_words(10))

   