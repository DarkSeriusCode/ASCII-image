from PIL import Image
import sys
import argparse
from typing import Tuple, List, Iterable

# ----------------------------------------------------
# Алиасы типов

Color = Tuple[int, int, int]

# ----------------------------------------------------
# Классы

class Canvas:
    def __init__(self, size: Tuple[int, int]):
        self.width, self.height = size
        self.canvas = [["" for _ in range(self.width)] for _ in range(self.height)]

    def set_char(self, x: int, y: int, symbol: str):
        """Устанавливает символ в canvas"""
        self.canvas[y][x] = symbol
    
    def show(self):
        """Выводит canvas"""
        for line in self.canvas:
            print("".join(line))

# ----------------------------------------------------
# Необходимые функции для работы с изображением

def get_colors(img: Image, x: int, y: int, size: int) -> List[Color]:
    """Возвращает цвета пикселей в квадрате со стороной size.
    Часть квадрата, находящаяся за пределами картинки, будет отброшена!

    x, y - координаты левого верхнего угла квадрата.
    size - размер стороны квадрата."""
    width, height = size, size
    rect = []

    # Изменяем размер квадрата, если тот выходит за
    # пределы картинки
    if x + width > img.width:
        width = img.width - x
    if y + height > img.height:
        height = img.height - y
    
    for Y in range(height):
        rect.extend([img.getpixel((x + X, y + Y)) for X in range(width)])
    return rect

def get_sum_color(rect: List[Color]) -> Color:
    """Возвращает среднее арифметическое всех цветов в квадрате"""
    common_color = [0, 0, 0]
    lenght = len(rect)

    for color in rect:
        common_color[0] += color[0]
        common_color[1] += color[1]
        common_color[2] += color[2]
    common_color[0] /= lenght
    common_color[1] /= lenght
    common_color[2] /= lenght

    return tuple(map(int, common_color))

def resize_img(img: Image, K: int, *, out_fname: str="result.jpg") -> Image:
    """Сжимает img в K раз и сохраняет как out_fname"""
    newimg_width = img.width // K
    newimg_height = img.height // K
    result = Image.new("RGB", (newimg_width, newimg_height))

    for y in range(0, img.height, K):
        for x in range(0, img.width, K):
            # Если вышли за пределы изображения
            if (y // K >= newimg_height) or (x // K >= newimg_width):
                break
            
            color = get_sum_color(get_colors(img, x, y, K))
            result.putpixel((x // K, y // K), color)
    
    result.save(out_fname)
    return result

# ----------------------------------------------------

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file")
    argparser.add_argument("-r", type=int, dest="resize", default=1,
                            help="How many times to compress the image")

    argparser.add_argument("--light-palette", type=str, 
                            dest="palette", default=" .,-+*&#@$",
                            help="Setup light palette. see README.md")

    argparser.add_argument("--no-print", 
                            dest="noprint", action="store_false",
                            help="Not print image")

    args = argparser.parse_args()

    PICTURE_NAME = args.file
    K = 1 if not args.resize else args.resize 
    # .,-~:;=!*#$@
    # .,-+*&#@$
    SYMBOLS = args.palette
    NOPRINT = not args.noprint

    STEP_SIZE = 255 // len(SYMBOLS)
    picture = Image.open(PICTURE_NAME)

    # Сжатие картинки
    if K > 1:
        print("Сжатие...")
        picture = resize_img(picture, K)
        print("Успех!\n")

    canvas = Canvas((picture.width, picture.height))

    if NOPRINT: return 

    # Построение canvas
    for Y in range(picture.height):
        for X in range(picture.width):
            color_code = sum(picture.getpixel((X, Y))) // 3

            # Определение символа в соответствии с color_code
            try:
                symbol = SYMBOLS[color_code // STEP_SIZE]
            except IndexError:
                symbol = SYMBOLS[-1]
            canvas.set_char(X, Y, symbol)
    canvas.show()

if __name__ == "__main__":
    main()
    