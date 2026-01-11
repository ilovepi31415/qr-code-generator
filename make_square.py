from PIL import Image

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def make_square(coords: tuple, size: int, color: bool, img: Image, scale=1) -> None:
    pixels = img.load()
    x, y = coords
    x *= scale
    y *= scale

    for i in range(x, x + size * scale):
        for j in range(y, y + size * scale):
            pixels[i,j] = WHITE if color else BLACK

def make_corner(coords: tuple, img: Image, scale=1) -> None:
    x, y = coords
    make_square((x, y), 7, False, img, scale)
    make_square((x + 1, y + 1), 5, True, img, scale)
    make_square((x + 2, y + 2), 3, False, img, scale)

