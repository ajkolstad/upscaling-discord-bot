import os
from pathlib import Path

from lib import (
    get_all_models,
    get_black_white_models,
    get_color_models,
    get_default_black_white_model,
    get_default_color_model,
    set_default_black_white_model,
    set_default_color_model,
    get_settings,
    create_output_zip_files,
    LitterBox,
    unzip_files,
    sort_input_images,
)
from upscale import Upscale


def list_all_models():
    bw_models, c_models = get_all_models()
    default_bw_model = get_default_black_white_model()
    default_c_model = get_default_color_model()
    message = "# All Available Models"
    if len(bw_models) > 0:
        message += "\n## Black and White Models:"
        for bw_model in bw_models:
            if bw_model == default_bw_model:
                message += "\n- `" + bw_model + "`\t**default**"
            else:
                message += "\n- `" + bw_model + "`"
    message += "\n"
    if len(c_models) > 0:
        message += "\n## Color Models:"
        for c_model in c_models:
            if c_model == default_c_model:
                message += "\n- `" + c_model + "`\t**default**"
            else:
                message += "\n- `" + c_model + "`"
    return message


def list_bw_models():
    bw_models = get_black_white_models()
    default_bw_model = get_default_black_white_model()
    message = ""
    if len(bw_models) > 0:
        message += "# Available Black and White Models:"
        for bw_model in bw_models:
            if bw_model == default_bw_model:
                message += "\n- `" + bw_model + "`\t**default**"
            else:
                message += "\n- `" + bw_model + "`"
    else:
        message += "# No Black and White Models available"
    return message


def list_c_models():
    c_models = get_color_models()
    default_c_model = get_default_color_model()
    message = ""
    if len(c_models) > 0:
        message += "# Available Color Models:"
        for c_model in c_models:
            if c_model == default_c_model:
                message += "\n- `" + c_model + "`\t**default**"
            else:
                message += "\n- `" + c_model + "`"
    else:
        message += "# No Color Models available"
    return message


def set_default_bw_model(model_name):
    if set_default_black_white_model(model_name):
        return "Default Black and White Model has been set to `" + model_name + "`"
    bw_models = get_black_white_models()
    if len(bw_models) == 0:
        return "Could not set a default Black and White Model because there are no Black and White Models available"
    else:
        return (
            "Could not set default Black and White Model to `"
            + model_name
            + "`\n"
            + list_bw_models()
        )


def set_default_c_model(model_name):
    if set_default_color_model(model_name):
        return "Default Color Model has been set to `" + model_name + "`"
    c_models = get_color_models()
    if len(c_models) == 0:
        return "Could not set a default Color Model because there are no Color Models available"
    else:
        return (
            "Could not set default Color Model to `"
            + model_name
            + "`\n"
            + list_c_models()
        )


def list_settings():
    settings = get_settings()


def upscale_using_link(link_to_zip: str, bw_model: str = None, c_model: str = None):
    # Download files
    litterbox_client = LitterBox()
    downloaded_file = litterbox_client.file_download(link_to_zip)

    # Unzip files
    unzip_files(downloaded_file)

    # Sort images based on color/bw
    sort_input_images()

    # Upscaling
    output_folder = os.path.join(os.getcwd(), "output")
    bw_models_folder = os.path.join(os.getcwd(), "models/blackwhite")
    c_models_folder = os.path.join(os.getcwd(), "models/color")

    # Upscale the bw images
    if bw_model is None:
        bw_model = os.path.join(bw_models_folder, get_default_black_white_model())

    upscale = Upscale(
        model=bw_model,
        input=Path("input/input_blackwhite"),
        output=Path("output"),
        reverse=False,
        skip_existing=True,
        delete_input=False,
        # seamless=False,
        cpu=False,
        fp16=True,
        device_id=0,
        cache_max_split_depth=False,
        binary_alpha=False,
        ternary_alpha=False,
        alpha_threshold=0.5,
        alpha_boundary_offset=0.2,
        alpha_mode=None,
    )
    upscale.run()

    # Upscale the color images
    if c_model is None:
        c_model = os.path.join(c_models_folder, get_default_color_model())

    upscale = Upscale(
        model=c_model,
        input=Path("input/input_color"),
        output=Path("output"),
        reverse=False,
        skip_existing=True,
        delete_input=False,
        # seamless=False,
        cpu=False,
        fp16=True,
        device_id=0,
        cache_max_split_depth=False,
        binary_alpha=False,
        ternary_alpha=False,
        alpha_threshold=0.5,
        alpha_boundary_offset=0.2,
        alpha_mode=None,
    )
    upscale.run()

    # Prepare the files for upload to Litterbox by zipping them in groups of 1 gigabyte
    zip_files = create_output_zip_files()

    message = "# Upscaling process complete\nThe following zip files have been created with the shown contents"

    for zip_file in zip_files:
        link = litterbox_client.file_upload(
            os.path.join(output_folder, zip_file["filename"]), 1
        )
        print(link)
        filename = link[link.index(".moe/") + 5 :]
        message += "\n## [" + str(filename) + "](" + link + ")"
        for file in sorted(zip_file["files"]):
            message += "\n - " + str(file)

    return message


print(upscale_using_link("https://files.catbox.moe/wj3fu7.zip"))
