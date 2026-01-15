import sys
from PIL import Image
from enum import Enum
from make_square import make_square, make_corner
from bch import encode_bch
from reed_solomon import encode_rs

TYPE1_SIZE = 21
TYPE1_LENGTH = 17
LOW_QUALITY = int('11', 2)
MASKPATTERN = int('011', 2)
PADDING_1 = '11101100'
PADDING_2 = '00010001'

SCALE = 20
SIZE = TYPE1_SIZE
QUALITY = LOW_QUALITY
MAXLENGTH = TYPE1_LENGTH

BORDER = 2

class Direction(Enum):
    UP = 1
    DOWN = 2

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <url/text>")
        return
    
    # Find and parse the data argument
    url = sys.argv[1]
    if len(url) > MAXLENGTH:
        print("ERROR: Message too long")
        sys.exit(1)
    url_bytes = url.encode()
    length = f'{len(url_bytes):08b}'

    bits = []

    # Add encoding bits
    encoding_method = [0, 1, 0, 0]
    for bit in encoding_method:
        bits.append(bit)
    for bit in length:
        bits.append(int(bit))
    
    for byte in url_bytes:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    # Add ending character to bytestream
    for bit in '0000':
        bits.append(int(bit))

    # Pad bytestream to max length
    while len(bits) < (MAXLENGTH + 2) * 8:
        for bit in PADDING_1:
            bits.append(int(bit))
        if len(bits) < (MAXLENGTH + 1) * 8:
            for bit in PADDING_2:
                bits.append(int(bit))
    
    print(bits)
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    img = Image.new( 'RGB', ((SIZE + (BORDER * 2)) * SCALE, (SIZE + (BORDER * 2)) * SCALE), (255, 0, 0)) # create a new black image
    pixels = img.load() # create the pixel map

    add_functional_info(img)

    # Get error correction data
    error_correction_value = encode_rs(bits)
    error_correction_string = ''
    for block in error_correction_value:
        error_correction_string += f'{block:08b}'
    print(error_correction_string)

    for bit in error_correction_string:
        bits.append(int(bit))

    img.show("QR Code")

    # Add data into image
    stream_data(bits, img)

    # mask_data(img)

    # Fix this after the mask
    add_functional_info(img)
    add_border(img)

    img.show("QR Code")

def stream_data(bits: list[int], img) -> None:
    # Set up a moving cursor and start in the bottom right
    cursor_x = SIZE - 1 + BORDER
    cursor_y = SIZE - 1 + BORDER

    # Used for restricting cursor movement
    edge = SIZE - 1 + BORDER
    dir = Direction.UP

    pixels = img.load()
    for bit in bits:
        # Loop until finding a blank pixelt to fill
        while is_used((cursor_x, cursor_y), pixels):
            # Follow a zigzag pattern up or down the edge
            if (cursor_x >= edge):
                cursor_x -= 1
            else:
                if dir == Direction.UP:
                    cursor_x += 1
                    cursor_y -= 1
                elif dir == Direction.DOWN:
                    cursor_x += 1
                    cursor_y += 1
            # switch direction if you hit the top or bottom
            if cursor_y < BORDER:
                dir = Direction.DOWN
                cursor_y += 1
                if edge == 8 + BORDER:
                    edge -= 3
                else:
                    edge -= 2 
                print("down")
            if cursor_y == SIZE + BORDER:
                dir = Direction.UP
                cursor_y -= 1
                edge -= 2
                print("up")
        make_square((cursor_x, cursor_y), 1, bit == 1, img, SCALE)

def is_used(coords, pixels) -> bool:
    x, y = coords
    return pixels[x * SCALE, y * SCALE] != (255, 0, 0)

def mask_data(img: Image):
    pixels = img.load()
    for y in range(BORDER, SIZE+BORDER):
        for x in range(BORDER, SIZE+BORDER):
            if y % 2 == 0:
                make_square((x, y), 1, pixels[x * SCALE, y * SCALE] != (0, 0, 0), img, SCALE)

def add_border(img):
    for x in range(SIZE+(2*BORDER)):
        for y in range(BORDER):
            make_square((x, y), 1, False, img, SCALE)
    for y in range(SIZE+(2*BORDER)):
        for x in range(BORDER):
            make_square((x, y), 1, False, img, SCALE)
    for x in range(SIZE+(2*BORDER)):
        for y in range(SIZE+BORDER, SIZE+(2*BORDER)):
            make_square((x, y), 1, False, img, SCALE)
    for y in range(SIZE+(2*BORDER)):
       for x in range(SIZE+BORDER, SIZE+(2*BORDER)):
            make_square((x, y), 1, False, img, SCALE)

def add_functional_info(img):
    # Basic Formatting on all QR Codes
    make_square((BORDER, BORDER), 8, False, img, SCALE)
    make_square((BORDER, SIZE-8+BORDER), 8, False, img, SCALE)
    make_square((SIZE-8+BORDER, BORDER), 8, False, img, SCALE)

    make_square((8+BORDER, SIZE-8+BORDER), 1, True, img, SCALE)

    make_corner((BORDER, BORDER), img, SCALE)
    make_corner((BORDER, SIZE - 7 + BORDER), img, SCALE)
    make_corner((SIZE - 7 + BORDER, BORDER), img, SCALE)

    for y in range(7+BORDER, SIZE-7+BORDER):
        make_square((6 + BORDER, y), 1, y % 2 == 0, img, SCALE)

    for x in range(7+BORDER, SIZE-7+BORDER):
        make_square((x, 6 + BORDER), 1, x % 2 == 0, img, SCALE)

    # Add format data into image
    format = (QUALITY << 2) + MASKPATTERN
    encoded_format = encode_bch(format)
    print(encoded_format)
    format_coords_1 = [
        (0, 8), (1, 8), (2, 8), (3, 8), (4, 8),
        (5, 8), (7, 8), (8, 8), (8, 7), (8, 5),
        (8, 4), (8, 3), (8, 2), (8, 1), (8, 0)
        ]
    format_coords_2 = [
        (8, SIZE-1), (8, SIZE-2), (8, SIZE-3), (8, SIZE-4), (8, SIZE-5),
        (8, SIZE-6), (8, SIZE-7), (SIZE-8, 8), (SIZE-7, 8), (SIZE-6, 8),
        (SIZE-5, 8), (SIZE-4, 8), (SIZE-3, 8), (SIZE-2, 8), (SIZE-1, 8) 
    ]
    for i in range(len(format_coords_1)):
        make_square((format_coords_1[i][0]+BORDER, format_coords_1[i][1]+BORDER), 1, (encoded_format >> (15 - i - 1)) & 1 == 1, img, SCALE)
        make_square((format_coords_2[i][0]+BORDER, format_coords_2[i][1]+BORDER), 1, (encoded_format >> (15 - i - 1)) & 1 == 1, img, SCALE)

if __name__ == "__main__":
    main()