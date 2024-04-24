import glob
import os

from PIL import Image

BITMAP_CONVERSION_INPUT_PATH = os.path.join(os.getcwd(), "input", "output_pre_bitmap")
BITMAP_CONVERSION_OUTPUT_PATH = os.path.join(os.getcwd(), "output")


def remove_file_extension(filename: str) -> str:
    for index, char in enumerate(filename[::-1]):
        if char == ".":
            return filename[: len(filename) - (index + 1)]


def convert_to_bitmap(filename: str, source_path: str, destination_path: str) -> bool:
    img = Image.open(os.path.join(source_path, filename))
    img = img.convert("1", dither=Image.Dither.NONE)
    new_filename = remove_file_extension(filename) + ".bmp"
    img.save(os.path.join(destination_path, new_filename))
    if os.path.isfile(os.path.join(destination_path, new_filename)):
        os.remove(os.path.join(source_path, filename))
        return True


def convert_all_to_bitmap() -> bool:
    for picture in os.listdir(BITMAP_CONVERSION_INPUT_PATH):
        res = convert_to_bitmap(
            picture.replace(BITMAP_CONVERSION_INPUT_PATH, ""),
            BITMAP_CONVERSION_INPUT_PATH,
            BITMAP_CONVERSION_OUTPUT_PATH,
        )
        if res is False:
            return False
    return True

