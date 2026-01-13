import math

def encode_rs(input: list[int]):
    generator_polynomial = [1, 127, 122, 154, 164, 11, 68, 117]
    blocks = []
    
    copied = input.copy()
    while len(copied) > 0:
        block = 0
        for _ in range(8):
            block *= 2
            block += copied.pop(0)
        blocks.append(block)
    blocks += [0] * 7
    print(blocks, len(blocks))

    for i in range(len(blocks) - 7):
        block = blocks[i]
        if block != 0:
            for j in range(len(generator_polynomial)):
                blocks[i + j] ^= gf_multiply(generator_polynomial[j], block)

    return blocks[-7:]

def gf_multiply(a, b):
    primitive_polynomial = 0x11D
    result = 0
    while b > 0:
        if b % 2 == 1:
            result ^= a
        a <<= 1
        if a >= 256:
            a ^= primitive_polynomial
        b >>= 1
    return result

if __name__ == "__main__":
    print(encode_rs(
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
         1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1,
         1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1,
         0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0,
         0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0,
         0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1,
         1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0,
         0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0,
         1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1,
         1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0,
         0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0,
         1, 0, 0, 0, 1, 0, 0, 1, 1]
        ))