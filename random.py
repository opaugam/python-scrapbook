
#
# - https://cdsmith.wordpress.com/2011/10/10/build-your-own-simple-random-numbers/
# - https://en.wikipedia.org/wiki/Pseudorandom_number_generator
# - https://en.wikipedia.org/wiki/Linear-feedback_shift_register
#

#
# - /dev/urandom to 4-bytes integer conversion
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
# - simple fibonacci LFSR with taps set at bits 16, 14, 13 and 11
# - we should have 2**16-1 distinct outputs before it cycles (maximum sequence over 16 bits)
#
def LFSR(seed, n):
    seed &= 0xFFFF
    state = seed
    while n:
        bit = 1 & ((state >> 0) ^ (state >> 2) ^ (state >> 3) ^ (state >> 5))
        state = (state >> 1) | (bit << 15)
        yield state % 100
        n -= 1
    
if __name__ == '__main__':

    print urandom()
    print [n for n in naive(urandom(), 100)]
    print [n for n in LFSR(urandom(), 100)]