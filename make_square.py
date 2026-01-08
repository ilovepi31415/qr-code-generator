from PIL import Image

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def make_square(coords: tuple, size: int, color: bool, img: Image) -> None:
    pixels = img.load()
    x, y = coords
    for i in range(x, x + size):
        for j in range(y, y + size):
            pixels[i,j] = WHITE if color else BLACK