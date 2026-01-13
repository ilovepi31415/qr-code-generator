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
    print(blocks, len(blocks))

    dividend = 0
    for term in input:
        dividend *= 2
        dividend += term
    print(dividend)

    generator_total = 0
    for term in generator_polynomial:
        generator_total *= 128
        generator_total += term

    while dividend >= 2 ** (7 * 8):
        divisor = generator_total
        while math.floor(math.log(divisor, 2)) < math.floor(math.log(dividend, 2)):
            divisor <<= 1
        dividend ^= divisor

    return dividend

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