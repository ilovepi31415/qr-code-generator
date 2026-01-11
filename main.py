import sys
from PIL import Image
from enum import Enum
from make_square import make_square, make_corner

TYPE1_SIZE = 21
LOW_QUALITY = int('11', 2)
SCALE = 8

SIZE = TYPE1_SIZE
QUALITY = LOW_QUALITY

class Direction(Enum):
    UP = 1
    DOWN = 2

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <url/text>")
        return
    
    url = sys.argv[1]
    url_bytes = url.encode()
    length = f'{len(url_bytes):08b}'

    bits = []

    encoding_method = [0, 1, 0, 0]
    for bit in encoding_method:
        bits.append(bit)
    for bit in length:
        bits.append(int(bit))
    
    for byte in url_bytes:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    
    print(bits)
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    img = Image.new( 'RGB', (SIZE * SCALE, SIZE * SCALE), (255, 0, 0)) # create a new black image
    pixels = img.load() # create the pixel map

    # for i in range(img.size[0]):    # for every col:
    #     for j in range(img.size[1]):    # For every row
    #         pixels[i, j] = (i//4, j//4, 100) # set the colour accordingly

    # Basic Formatting on all QR Codes
    make_square((0, 0), 8, False, img, SCALE)
    make_square((0, SIZE-8), 8, False, img, SCALE)
    make_square((SIZE-8, 0), 8, False, img, SCALE)

    make_square((8, SIZE-8), 1, True, img, SCALE)

    make_corner((0, 0), img, SCALE)
    make_corner((0, SIZE - 7), img, SCALE)
    make_corner((SIZE - 7, 0), img, SCALE)

    for y in range(7, SIZE-7):
        make_square((6, y), 1, y % 2 == 0, img, SCALE)

    for x in range(7, SIZE-7):
        make_square((x, 6), 1, x % 2 == 0, img, SCALE)



    # Add data into image
    stream_data(bits, img)

    img.show("QR Code")

def stream_data(bits: list[int], img) -> None:
    # Set up a moving cursor and start in the bottom right
    cursor_x = SIZE - 1
    cursor_y = SIZE - 1

    # Used for restricting cursor movement
    edge = SIZE - 1
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
            if cursor_y < 0:
                dir = Direction.DOWN
                cursor_y += 1
                edge -= 2
                print("down")
            if cursor_y == SIZE:
                dir = Direction.UP
                cursor_y -= 1
                edge -= 2
                print("up")
        make_square((cursor_x, cursor_y), 1, bit == 1, img, SCALE)

def is_used(coords, pixels) -> bool:
    x, y = coords
    return pixels[x * SCALE, y * SCALE] != (255, 0, 0)

if __name__ == "__main__":
    main()

