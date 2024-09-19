import argparse
import pathlib
import tomllib
import typing as t
from dataclasses import dataclass

from PIL import Image


ROOT_DIR: t.Final = pathlib.Path(__file__).parent.parent
PALLETES_TOML: t.Final = ROOT_DIR / "palletes.toml"


type Color = tuple[int, int, int]
type Pixel = tuple[int, int]


def hex_to_rgb(hex_value) -> Color:
    hex_value = hex_value if isinstance(hex_value, int) else int(hex_value, 16)
    
    r = (hex_value >> 16) & 0xFF  # Красный канал
    g = (hex_value >> 8) & 0xFF   # Зелёный канал
    b = hex_value & 0xFF          # Синий канал
    
    return r, g, b


@dataclass(frozen=True, slots=True)
class Pallete:
    black: Color
    white: Color
    white_d: Color
    red: Color
    red_d: Color
    green: Color
    green_d: Color
    blue: Color
    blue_d: Color
    cyan: Color
    cyan_d: Color
    magenta: Color
    magenta_d: Color
    yellow: Color
    yellow_d: Color

    def __iter__(self) -> t.Iterator[Color]:
        yield from [
            self.black,
            self.white,
            self.white_d,
            self.red,
            self.red_d,
            self.blue,
            self.blue_d,
            self.green,
            self.green_d,
            self.cyan,
            self.cyan_d,
            self.magenta,
            self.magenta_d,
            self.yellow,
            self.yellow_d,
        ]


REQUIRED_COLORS: t.Final = {
    "black",
    "white",
    "white_d",
    "red",
    "red_d",
    "green",
    "green_d",
    "blue",
    "blue_d",
    "cyan",
    "cyan_d",
    "magenta",
    "magenta_d",
    "yellow",
    "yellow_d",
}

def loaded_pallete(name: str) -> Pallete:
    data = tomllib.loads(PALLETES_TOML.read_text())
    pallete = data.get(name)
    if not pallete:
        raise ValueError(f"Pallete `{name}` is not defined. Please, define it in {PALLETES_TOML}")
    if not all(color_name in pallete for color_name in REQUIRED_COLORS):
        raise ValueError(f"Pallete `{name}` is defined incorrectly. Please, check it in {PALLETES_TOML}")
    black = hex_to_rgb(pallete.get("black"))
    white = hex_to_rgb(pallete.get("white"))
    white_d = hex_to_rgb(pallete.get("white_d"))
    red = hex_to_rgb(pallete.get("red"))
    red_d = hex_to_rgb(pallete.get("red_d"))
    green = hex_to_rgb(pallete.get("green"))
    green_d = hex_to_rgb(pallete.get("green_d"))
    blue = hex_to_rgb(pallete.get("blue"))
    blue_d = hex_to_rgb(pallete.get("blue_d"))
    cyan = hex_to_rgb(pallete.get("cyan"))
    cyan_d = hex_to_rgb(pallete.get("cyan_d"))
    magenta = hex_to_rgb(pallete.get("magenta"))
    magenta_d = hex_to_rgb(pallete.get("magenta_d"))
    yellow = hex_to_rgb(pallete.get("yellow"))
    yellow_d = hex_to_rgb(pallete.get("yellow_d"))
    return Pallete(
        black, 
        white, 
        white_d, 
        red, 
        red_d, 
        green, 
        green_d, 
        blue, 
        blue_d, 
        cyan, 
        cyan_d, 
        magenta, 
        magenta_d, 
        yellow,
        yellow_d,
    )


DEFAULT_PALLETE: t.Final = loaded_pallete("zx-spectrum")
DEFAULT_TARGET_PALLETE: t.Final = "gruvbox"


def iter_pixels(img: Image.Image) -> t.Iterator[Pixel]:
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            yield i, j


def map_color_to_pallete(c: Color, p: Pallete) -> Color:
    if c == DEFAULT_PALLETE.black:
        return p.black
    elif c == DEFAULT_PALLETE.white:
        return p.white
    elif c == DEFAULT_PALLETE.white_d:
        return p.white_d
    elif c == DEFAULT_PALLETE.red:
        return p.red
    elif c == DEFAULT_PALLETE.red_d:
        return p.red_d
    elif c == DEFAULT_PALLETE.green:
        return p.green
    elif c == DEFAULT_PALLETE.green_d:
        return p.green_d
    elif c == DEFAULT_PALLETE.blue:
        return p.blue
    elif c == DEFAULT_PALLETE.blue_d:
        return p.blue_d
    elif c == DEFAULT_PALLETE.cyan:
        return p.cyan
    elif c == DEFAULT_PALLETE.cyan_d:
        return p.cyan_d
    elif c == DEFAULT_PALLETE.magenta:
        return p.magenta
    elif c == DEFAULT_PALLETE.magenta_d:
        return p.magenta
    elif c == DEFAULT_PALLETE.yellow:
        return p.yellow
    elif c == DEFAULT_PALLETE.yellow_d:
        return p.yellow_d
    raise ValueError(f"Unapplicable color `{c}`")
    # return c



def colorized_image(i: Image.Image, pallete: Pallete) -> Image.Image:
    res = i.copy().convert("RGB")
    _colors = []
    for xy in iter_pixels(i):
        current_color: Color = res.getpixel(xy)  # type: ignore
        _colors.append(current_color)
        new_color = map_color_to_pallete(current_color, pallete)
        res.putpixel(xy, new_color)
    return res


def parsed_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tool to colorize ZX Spectrum arts to various palletes"
    )
    parser.add_argument("--input", "-i", type=pathlib.Path)
    parser.add_argument("--output", "-o", type=pathlib.Path)
    parser.add_argument("--pallete", "-p", type=str, default=DEFAULT_TARGET_PALLETE)
    return parser.parse_args()


def main() -> None:
    args = parsed_args()
    input_file = args.input
    output_file = args.output
    target_pallete = loaded_pallete(args.pallete)
    with Image.open(input_file) as img:
        colorized_image(img, target_pallete).save(output_file)


if __name__ == "__main__":
    main()

