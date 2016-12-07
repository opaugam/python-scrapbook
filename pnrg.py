
#
# - https://cdsmith.wordpress.com/2011/10/10/build-your-own-simple-random-numbers/
# - https://en.wikipedia.org/wiki/Pseudorandom_number_generator
# - https://en.wikipedia.org/wiki/Linear-feedback_shift_register
# - https://en.wikipedia.org/wiki/Xorshift
#
import random

#
# - /dev/urandom to 4-bytes integer
#


def urandom():
    with open("/dev/urandom", 'rb') as f:
        raw = bytearray(f.read(4))
        return raw[0] | (raw[1] << 8) | (raw[2] << 16) | (raw[3] << 24)

#
# - trivial modular generator producing values in [0, 100]
#


def naive(seed, n):
    state = 1 + seed
    while n:
        state = (7 * state) % 109973007
        yield state % 100
        n -= 1

#
# - same as a fibonacci LFSR with taps set at bits 16, 14, 13 and 11
# - we should have 2**16-1 distinct outputs before it cycles (maximum sequence over 16 bits)
# - changing to polynomial will produce distinct values at first and then fall into a cycle
#


def LFSR(seed, n):
    seed &= 0xFFFF
    state = seed
    while n:
        bit = 1 & ((state >> 0) ^ (state >> 2) ^ (state >> 3) ^ (state >> 5))
        state = (state >> 1) | (bit << 15)
        yield state % 100
        n -= 1

#
# - simple xorshift implementation taken from wikipedia with a max. period of 2**128 -1
#


def xorshift(seed, n):
    x = seed
    y = 2
    z = 3
    w = 4

    while n:
        tmp = 0xFFFFFF & (x ^ (x << 11))
        tmp ^= (tmp >> 8)
        (x, y, z) = (y, z, w)
        w = tmp ^ (w >> 19) ^ w
        yield w % 100
        n -= 1

if __name__ == '__main__':

    def frequencies(seq):

        digits = {_: 0 for _ in range(10)}
        for n in seq:
            while n:
                digits[n % 10] += 1
                n /= 10
        return digits

    #
    # - use 65K samples
    #
    S = 2**16

    #
    # - run the default PNRG implemenation
    #
    random.seed()
    print frequencies([random.randrange(100) for _ in range(S)])

    #
    # - now let's compare with our implementations
    #
    print frequencies(list(naive(urandom(), S)))
    print frequencies(list(LFSR(urandom(), S)))
    print frequencies(list(xorshift(urandom(), S)))
