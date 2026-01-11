def encode_bch(input: int) -> int:
    generator_polynomial = int('10100110111', 2)
    mask = int('101010000010010', 2)

    dividend = (input << 10)

    # Polynomial division in binary
    while dividend >= 2 ** 10:
        divisor = generator_polynomial
        while (divisor << 1) < dividend:
            divisor <<= 1
        dividend ^= divisor
    
    return ((input << 10) + dividend) ^ mask

if __name__ == "__main__":
    print(bin(encode_bch(int('10101', 2))))