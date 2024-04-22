import glob
import os

from PIL import Image

BITMAP_CONVERSION_INPUT_PATH = "./input/input_bw/"
BITMAP_CONVERSION_OUTPUT_PATH = "./output/"


def remove_file_extension(filename: str) -> str:
    for index, char in enumerate(filename[::-1]):
        if char == ".":
            return filename[: len(filename) - (index + 1)]


def convert_to_bitmap(filename: str, source_path: str, destination_path: str) -> bool:
    img = Image.open(source_path + filename)
    img = img.convert("1", dither=Image.Dither.NONE)
    new_filename = remove_file_extension(filename) + ".bmp"
    img.save(destination_path + new_filename)
    return os.path.isfile(destination_path + new_filename)


def convert_all_to_bitmap() -> bool:
    pictures = glob.glob(BITMAP_CONVERSION_INPUT_PATH + "*")

    for picture in pictures:
        res = convert_to_bitmap(
            picture.replace(BITMAP_CONVERSION_INPUT_PATH, ""),
            BITMAP_CONVERSION_INPUT_PATH,
            BITMAP_CONVERSION_OUTPUT_PATH,
        )
        if res is False:
            return False
    return True
