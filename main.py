import sys
from PIL import Image
from make_square import make_square

SIZE = 1000

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
    img = Image.new( 'RGB', (SIZE, SIZE), "black") # create a new black image
    pixels = img.load() # create the pixel map

    # for i in range(img.size[0]):    # for every col:
    #     for j in range(img.size[1]):    # For every row
    #         pixels[i, j] = (i//4, j//4, 100) # set the colour accordingly

    make_square((0, 0), 5, True, img)
    make_square((100, 200), 25, True, img)
    make_square((105, 205), 10, False, img)

    img.show("QR Code")

if __name__ == "__main__":
    main()

