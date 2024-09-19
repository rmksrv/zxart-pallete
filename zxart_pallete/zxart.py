import argparse
import pathlib
import tomllib
import typing as t
from dataclasses import dataclass

from PIL import Image


ROOT_DIR: t.Final = pathlib.Path(__file__).parent.parent
PALLETES_TOML: t.Final = ROOT_DIR / "palletes.toml"

type Color = tuple[int, int, int]
type Pos = tuple[int, int]
type SupportsInt = str | bytes | bytearray


@dataclass(frozen=True, slots=True)
class Pixel:
    pos: Pos
    color: Color


def hex_to_rgb(hex_value: int | SupportsInt) -> Color:
    hex_value = (
        hex_value if isinstance(hex_value, int) 
        else int(hex_value, 16)
    )
    
    r = (hex_value >> 16) & 0xFF
    g = (hex_value >> 8) & 0xFF
    b = hex_value & 0xFF
    
    return r, g, b


def find_key[K, V](val: V, dct: dict[K, V | t.Any]) -> K | None:
    if not dct:
        return None
    maybe_key = [k for k, v in dct.items() if v == val]
    if not maybe_key:
        return None
    return maybe_key[0]


Pallete = t.TypedDict("Pallete", {
    "black": Color,
    "white": Color,
    "white_d": Color,
    "red": Color,
    "red_d": Color,
    "green": Color,
    "green_d": Color,
    "blue": Color,
    "blue_d": Color,
    "cyan": Color,
    "cyan_d": Color,
    "magenta": Color,
    "magenta_d": Color,
    "yellow": Color,
    "yellow_d": Color,
})
REQUIRED_COLORS: t.Final = Pallete.__annotations__.keys()


def iter_pallete(p: Pallete) -> t.Iterator[Color]:
    yield from t.cast(list[Color], (p.values()))


def is_valid_pallete(p: Pallete) -> bool:
    return all(color in p for color in REQUIRED_COLORS)


def loaded_pallete(name: str) -> Pallete:
    data = tomllib.loads(PALLETES_TOML.read_text())
    pallete = data.get(name)
    if not pallete:
        raise ValueError(f"Pallete `{name}` is not defined. Please, define it in {PALLETES_TOML}")
    if not is_valid_pallete(pallete):
        raise ValueError(f"Pallete `{name}` is defined incorrectly. Please, check it in {PALLETES_TOML}")
    return t.cast(Pallete, {
        name: hex_to_rgb(hexcode) 
        for name, hexcode in pallete.items()
    })


DEFAULT_PALLETE: t.Final = loaded_pallete("zx-spectrum")
DEFAULT_TARGET_PALLETE: t.Final = "gruvbox"


def iter_pixels(img: Image.Image) -> t.Iterator[Pixel]:
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            color: Color = img.getpixel((i, j))  # type: ignore
            yield Pixel((i, j), color)


def match_pallete_color(c: Color, source_pallete: Pallete, target_pallete: Pallete) -> Color:
    matched_color_name = find_key(c, dict(source_pallete))
    if not matched_color_name:
        raise ValueError(f"Unapplicable color `{c}`")
    return target_pallete[matched_color_name]


def colorized_image(i: Image.Image, pallete: Pallete) -> Image.Image:
    res = i.copy().convert("RGB")
    for p in iter_pixels(res):
        new_color = match_pallete_color(p.color, DEFAULT_PALLETE, pallete)
        res.putpixel(p.pos, new_color)
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

