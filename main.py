import sys
from PIL import Image
from make_square import make_square, make_corner

TYPE1_SIZE = 21
SCALE = 50

SIZE = TYPE1_SIZE

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <url/text>")
        return
    
    url = sys.argv[1]
    url_bytes = url.encode()
    print(len(url_bytes))

    bits = []
    for byte in url_bytes:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    
    print(bits)
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    img = Image.new( 'RGB', (SIZE * SCALE, SIZE * SCALE), "red") # create a new black image
    pixels = img.load() # create the pixel map

    # for i in range(img.size[0]):    # for every col:
    #     for j in range(img.size[1]):    # For every row
    #         pixels[i, j] = (i//4, j//4, 100) # set the colour accordingly

    make_corner((0, 0), img, SCALE)
    make_corner((0, SIZE - 7), img, SCALE)
    make_corner((SIZE - 7, 0), img, SCALE)

    for y in range(7, SIZE-7):
        make_square((6, y), 1, y % 2 == 1, img, SCALE)

    for x in range(7, SIZE-7):
        make_square((x, 6), 1, x % 2 == 1, img, SCALE)

    img.show("QR Code")

if __name__ == "__main__":
    main()

