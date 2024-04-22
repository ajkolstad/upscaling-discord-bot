import json
import os
import zipfile
from os import path, getcwd
from typing import List, Tuple, Optional

from PIL import Image

# from upscale import Upscale

SETTINGS_FILENAME = "settings.json"
BASE_FORMAT = {
    "DefaultBlackWhiteModel": "",
    "DefaultColorModel": "",
    "DefaultBitmapBehavior": False,
}


def get_input_files():
    return False


def get_output_files():
    return False


def download_file(file_id, file_name):
    return False


def upload_file(file_path, file_name):
    return False


def get_new_files():
    return False


def download_new_files(new_files):
    return False


def create_folders():
    create_image_folders()
    create_model_folders()


def create_image_folders():
    input_folder = os.path.join(os.getcwd(), "input")

    if not os.path.exists(input_folder):
        os.mkdir(input_folder)

    black_white_folder_path = os.path.join(input_folder, "input_blackwhite")
    color_folder_path = os.path.join(input_folder, "input_color")

    if not os.path.exists(black_white_folder_path):
        os.mkdir(black_white_folder_path)

    if not os.path.exists(color_folder_path):
        os.mkdir(color_folder_path)


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
        print(file)
        print(os.path.isfile(os.path.join(input_folder, file)))
        if os.path.isfile(os.path.join(input_folder, file)):
            print(file)
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


def unzip(zip_file_path: str) -> None:
    # Unzip the file
    print(zip_file_path)
    input_folder = path.join(getcwd(), "input")
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(input_folder)

    directories = os.listdir(input_folder)

    for item in directories:
        # Go to subfolder
        folder = os.path.join(input_folder, item)
        # print("Folder: " + str(folder))
        # Find the file
        for root, dirs, files in os.walk(folder):
            for file in files:
                if (
                    file.lower().endswith("png")
                    or file.lower().endswith("jpg")
                    or file.lower().endswith("jpeg")
                ):

                    target = os.path.join(root, file)
                    print("Image: " + str(target))
                    os.replace(target, os.path.join(os.path.join(input_folder, file)))
                else:
                    target = os.path.join(root, file)
                    print("Delete: " + str(target))
                    os.remove(os.path.join(root, file))

            if not str(root).endswith("input_color") and not str(root).endswith(
                "input_blackwhite"
            ):
                print("Root: " + str(root))
                os.rmdir(root)

        if os.path.isfile(zip_file_path):
            os.remove(zip_file_path)


"""def upscaling_process(channel, upscaler):
    print("Looking for new files...")

    new_files = get_new_files()

    if len(new_files) == 0:
        print(
            "I looked for new files to upscale, but I didn't find any. If you want me to upscale images again, delete all of the images in the Output folder, then run `!upscale` again."
        )
        return

    download_new_files(new_files)

    upscale = Upscale(
        model=upscaler,
        input=Path("input"),
        output=Path("output"),
        reverse=False,
        skip_existing=True,
        delete_input=False,
        seamless=False,
        cpu=False,
        fp16=(upscaler != V2_PATH),
        device_id=0,
        cache_max_split_depth=False,
        binary_alpha=False,
        ternary_alpha=False,
        alpha_threshold=0.5,
        alpha_boundary_offset=0.2,
        alpha_mode=None,
    )

    upscale.run()

    print("Process complete")
    num_new_files = 0"""

initialize_settings_file()
