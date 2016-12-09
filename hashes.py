
#
# - http://www.eternallyconfuzzled.com/tuts/algorithms/jsw_tut_hashing.aspx
# - https://en.wikipedia.org/wiki/List_of_hash_functions
# - http://burtleburtle.net/bob/hash/doobs.html
#
import random


def simple_xor(key):
    out = 0
    for byte in bytearray(key):
        out ^= byte
    return out


def rotating_xor(key):
    out = 0
    for byte in bytearray(key):
        out = (out << 4) ^ (out >> 28) ^ byte
    return out


def bernstein(key):
    out = 0
    for byte in bytearray(key):
        out = 33 * out + byte
    return out


def shift_add_xor(key):
    out = 0
    for byte in bytearray(key):
        out ^= byte + (out << 5) + (out >> 2)
    return out


def fnv(key):
    out = 0
    for byte in bytearray(key):
        out = (out * 16777619) ^ byte
    return out


def one_at_a_time(key):
    out = 0
    for byte in bytearray(key):
        out += byte
        out += (out << 10)
        out += (out >> 6)

    out += (out << 3)
    out ^= (out >> 11)
    out += (out << 15)
    return out


Z = [[random.randint(0, 0xFFFFFFFF) for _ in xrange(256)] for _ in xrange(4)]


def zobrist(key):
    out = 0
    for i, byte in enumerate(bytearray(key)):
        out ^= Z[i][byte]
    return out


def to_bytes(value):
    value &= 0xFFFFFF
    return ''.join(map(chr, [value >> i & 0xFF for i in (24, 16, 8, 0)]))


def bitrot32(value, n):
    assert n < 32
    return (value << n & 0xFFFFFFFF) ^ (value >> (32 - n) & 0xFFFFFFFF)


def bitcnt(value):
    n = 0
    while value:
        value &= value - 1
        n += 1
    return n


def check_collisions(method):

    K = 2**16
    S = 2**16

    hits = 0
    slots = [0 for n in xrange(S)]
    for n in xrange(K):
        index = method(to_bytes(n)) % S
        slots[index] += 1
        if slots[index] > 1:
            hits += 1

    expected = float(K) / S
    avg = float(sum(slots)) / S
    variance = sum((avg - n) ** 2 for n in slots) / len(slots)
    print '%s : %d hits [exp %d, mean %d, var %.1f]' % (method.__name__, hits, expected, avg, variance)


def check_bit_flips(method):

    K = 2**16
    S = 2**32

    msk = 0
    bits = 0
    for i in xrange(K):
        for j in xrange(32):

            #
            # - rotate our pair of 32bit integer
            # - their differ by definition in exactly 1 bit
            # - compute their respective hash
            # - check how many bits are different
            #
            A = bitrot32(2 * i,     j)
            B = bitrot32(2 * i + 1, j)
            xor = (method(to_bytes(A)) % S) ^ (method(to_bytes(B)) % S)
            bits += bitcnt(xor)
            msk |= xor

    avg = bits / (K * 32)
    print '%s : %d bits differ on avg, %d bits flipped' % (method.__name__, avg, bitcnt(msk))

if __name__ == '__main__':

    for method in [simple_xor, rotating_xor, bernstein, shift_add_xor, fnv, one_at_a_time, zobrist]:
        check_collisions(method)
        check_bit_flips(method)
