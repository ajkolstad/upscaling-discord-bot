import json
import os
import zipfile
from os import path, getcwd
from typing import List, Tuple, Optional

from PIL import Image

# from upscale import Upscale

MAX_SIZE = 1000000000


SETTINGS_FILENAME = "settings.json"
BASE_FORMAT = {
    "DefaultBlackWhiteModel": "",
    "DefaultColorModel": "",
    "DefaultBitmapBehavior": False,
    "CurrentUpscalerStatus": "Idle",
}


def create_folders():
    create_image_folders()
    create_model_folders()
    initialize_settings_file()


def clean_up():
    create_image_folders()
    input_folder = os.path.join(os.getcwd(), "input")
    black_white_folder_path = os.path.join(input_folder, "input_blackwhite")
    color_folder_path = os.path.join(input_folder, "input_color")
    pre_bitmap_folder_path = os.path.join(input_folder, "output_pre_bitmap")
    output_folder = os.path.join(os.getcwd(), "output")

    for file in os.listdir(input_folder):
        if os.path.isfile(os.path.join(input_folder, file)):
            os.remove(os.path.join(input_folder, file))

    for file in os.listdir(black_white_folder_path):
        if os.path.isfile(os.path.join(black_white_folder_path, file)):
            os.remove(os.path.join(black_white_folder_path, file))

    for file in os.listdir(color_folder_path):
        if os.path.isfile(os.path.join(color_folder_path, file)):
            os.remove(os.path.join(color_folder_path, file))

    for file in os.listdir(pre_bitmap_folder_path):
        if os.path.isfile(os.path.join(pre_bitmap_folder_path, file)):
            os.remove(os.path.join(pre_bitmap_folder_path, file))

    for file in os.listdir(output_folder):
        if os.path.isfile(os.path.join(output_folder, file)):
            os.remove(os.path.join(output_folder, file))


def create_image_folders():
    input_folder = os.path.join(os.getcwd(), "input")

    if not os.path.exists(input_folder):
        os.mkdir(input_folder)

    black_white_folder_path = os.path.join(input_folder, "input_blackwhite")
    color_folder_path = os.path.join(input_folder, "input_color")
    pre_bitmap_folder_path = os.path.join(input_folder, "output_pre_bitmap")

    if not os.path.exists(black_white_folder_path):
        os.mkdir(black_white_folder_path)

    if not os.path.exists(color_folder_path):
        os.mkdir(color_folder_path)

    if not os.path.exists(pre_bitmap_folder_path):
        os.mkdir(pre_bitmap_folder_path)

    output_folder = os.path.join(os.getcwd(), "output")

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)


def create_model_folders():
    models_folder = os.path.join(os.getcwd(), "models")

    if not os.path.exists(models_folder):
        os.mkdir(models_folder)

    black_white_folder_path = os.path.join(models_folder, "blackwhite")
    color_folder_path = os.path.join(models_folder, "color")

    if not os.path.exists(black_white_folder_path):
        os.mkdir(black_white_folder_path)

    if not os.path.exists(color_folder_path):
        os.mkdir(color_folder_path)


def get_black_white_models() -> List[str]:
    create_model_folders()

    models_folder = os.path.join(os.getcwd(), "models")

    black_white_folder_path = os.path.join(models_folder, "blackwhite")

    black_white_models = []

    for file in os.listdir(black_white_folder_path):
        if file.endswith(".pth"):
            black_white_models.append(str(file))

    return black_white_models


def get_color_models() -> List[str]:
    create_model_folders()

    models_folder = os.path.join(os.getcwd(), "models")

    color_folder_path = os.path.join(models_folder, "color")

    color_models = []

    for file in os.listdir(color_folder_path):
        if file.endswith(".pth"):
            color_models.append(str(file))

    return color_models


def get_all_models() -> Tuple[List[str], List[str]]:

    create_model_folders()

    return get_black_white_models(), get_color_models()


def initialize_settings_file():
    if not os.path.isfile(SETTINGS_FILENAME):
        with open(SETTINGS_FILENAME, "w") as outfile:
            json.dump(BASE_FORMAT, outfile)

        bw_models, c_models = get_all_models()

        with open(SETTINGS_FILENAME, "r+") as file:
            file_data = json.load(file)

            if len(bw_models) == 1:
                file_data["DefaultBlackWhiteModel"] = bw_models[0]
            if len(c_models) == 1:
                file_data["DefaultColorModel"] = c_models[0]

        with open(SETTINGS_FILENAME, "w") as file:
            json.dump(file_data, file, indent=4)


def get_default_black_white_model() -> Optional[str]:
    initialize_settings_file()

    with open(SETTINGS_FILENAME, "r+") as file:
        file_data = json.load(file)

    model = file_data["DefaultBlackWhiteModel"]
    if model == "":
        return None

    return model


def get_default_color_model() -> Optional[str]:
    initialize_settings_file()

    with open(SETTINGS_FILENAME, "r+") as file:
        file_data = json.load(file)

    model = file_data["DefaultColorModel"]
    if model == "":
        return None

    return model


def set_default_black_white_model(model_name: str) -> bool:
    bw_models = get_black_white_models()
    initialize_settings_file()

    with open(SETTINGS_FILENAME, "r+") as file:
        file_data = json.load(file)

    if model_name not in bw_models:
        return False

    file_data["DefaultBlackWhiteModel"] = model_name

    with open(SETTINGS_FILENAME, "w") as file:
        json.dump(file_data, file, indent=4)

    return True


def set_default_color_model(model_name: str) -> bool:
    c_models = get_color_models()
    initialize_settings_file()

    with open(SETTINGS_FILENAME, "r+") as file:
        file_data = json.load(file)

    if model_name not in c_models:
        return False

    file_data["DefaultColorModel"] = model_name

    with open(SETTINGS_FILENAME, "w") as file:
        json.dump(file_data, file, indent=4)

    return True


def get_default_bitmap_behavior() -> Optional[bool]:
    initialize_settings_file()

    with open(SETTINGS_FILENAME, "r+") as file:
        file_data = json.load(file)

    mode = file_data["DefaultBitmapBehavior"]
    return mode


def set_default_bitmap_behavior(bitmap: bool) -> bool:
    initialize_settings_file()

    with open(SETTINGS_FILENAME, "r+") as file:
        file_data = json.load(file)

    file_data["DefaultBitmapBehavior"] = bitmap

    with open(SETTINGS_FILENAME, "w") as file:
        json.dump(file_data, file, indent=4)

    return True


def get_settings() -> dict:
    initialize_settings_file()

    with open(SETTINGS_FILENAME, "r+") as file:
        file_data = json.load(file)

    return file_data


def write_status_to_settings_file(status: str):
    initialize_settings_file()

    with open(SETTINGS_FILENAME, "r+") as file:
        file_data = json.load(file)

    file_data["CurrentUpscalerStatus"] = status

    with open(SETTINGS_FILENAME, "w") as file:
        json.dump(file_data, file, indent=4)

    return True


def read_status_from_settings_file() -> str:
    initialize_settings_file()

    with open(SETTINGS_FILENAME, "r+") as file:
        file_data = json.load(file)

    status = file_data["CurrentUpscalerStatus"]
    return status


def is_grey_scale(img_path) -> bool:
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            if r != g != b:
                if abs(r - g) > 5 or abs(g - b) > 5 or abs(b - r) > 5:
                    return False
    return True


def sort_input_images() -> None:
    create_image_folders()

    input_folder = os.path.join(os.getcwd(), "input")

    black_white_folder_path = os.path.join(input_folder, "input_blackwhite")
    color_folder_path = os.path.join(input_folder, "input_color")

    for file in os.listdir(input_folder):
        if os.path.isfile(os.path.join(input_folder, file)):
            if (
                file.lower().endswith("png")
                or file.lower().endswith("jpg")
                or file.lower().endswith("jpeg")
            ):
                if is_grey_scale(os.path.join(input_folder, file)):
                    os.replace(
                        os.path.join(os.path.join(input_folder, file)),
                        os.path.join(os.path.join(black_white_folder_path, file)),
                    )
                else:
                    os.replace(
                        os.path.join(os.path.join(input_folder, file)),
                        os.path.join(os.path.join(color_folder_path, file)),
                    )


def unzip_files(zip_file_path: str) -> None:
    # Unzip the file
    input_folder = path.join(getcwd(), "input")
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(input_folder)

    directories = os.listdir(input_folder)

    for item in directories:
        folder = os.path.join(input_folder, item)
        for root, dirs, files in os.walk(folder):
            for file in files:
                if (
                    file.lower().endswith("png")
                    or file.lower().endswith("jpg")
                    or file.lower().endswith("jpeg")
                ):

                    target = os.path.join(root, file)
                    os.replace(target, os.path.join(os.path.join(input_folder, file)))
                else:
                    os.remove(os.path.join(root, file))

            if (
                not str(root).endswith("input_color")
                and not str(root).endswith("input_blackwhite")
                and not str(root).endswith("output_pre_bitmap")
            ):
                os.rmdir(root)

        if os.path.isfile(zip_file_path):
            os.remove(zip_file_path)


def get_file_size(file_path: str) -> int:
    file_stats = os.stat(file_path)
    return file_stats.st_size


def zip_files(file_paths: List[str], zip_file_name: str):
    output_folder = os.path.join(os.getcwd(), "output")
    with zipfile.ZipFile(zip_file_name, "w") as zip_file:
        for file in file_paths:
            zip_file.write(
                os.path.join(output_folder, file),
                os.path.basename(os.path.join(output_folder, file)),
                compress_type=zipfile.ZIP_DEFLATED,
            )


def create_output_zip_files() -> List:
    output_folder = os.path.join(os.getcwd(), "output")
    created_zip_files = []

    current_zip_file_size = 0
    current_zip_file_contained_files = []
    for file in os.listdir(output_folder):
        if not file.lower().endswith(".png") and not file.lower().endswith(".bmp"):
            continue
        file_size = get_file_size(os.path.join(output_folder, file))
        if current_zip_file_size + file_size > MAX_SIZE:
            print(current_zip_file_size)
            created_zip_files.append(
                {
                    "filename": "output_" + str(len(created_zip_files) + 1) + ".zip",
                    "files": current_zip_file_contained_files,
                    "size": current_zip_file_size,
                }
            )
            zip_files(
                current_zip_file_contained_files,
                os.path.join(
                    output_folder, "output_" + str(len(created_zip_files)) + ".zip"
                ),
            )
            current_zip_file_size = file_size
            current_zip_file_contained_files = [file]

        else:
            current_zip_file_size += file_size
            current_zip_file_contained_files.append(file)

    created_zip_files.append(
        {
            "filename": "output_" + str(len(created_zip_files) + 1) + ".zip",
            "files": current_zip_file_contained_files,
            "size": current_zip_file_size,
        }
    )
    zip_files(
        current_zip_file_contained_files,
        os.path.join(output_folder, "output_" + str(len(created_zip_files)) + ".zip"),
    )

    return created_zip_files


clean_up()
