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

# Precompute tables
EXP = [0] * 512
LOG = [0] * 256
x = 1
for i in range(255):
    EXP[i] = x
    LOG[x] = i
    x <<= 1
    if x & 0x100:
        x ^= 0x11D
# Duplicate EXP to avoid modulo 255 during addition
for i in range(255, 512):
    EXP[i] = EXP[i - 255]

def gf_multiply(a, b):
    if a * b == 0:
        return 0
    return EXP[LOG[a] + LOG[b]]

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