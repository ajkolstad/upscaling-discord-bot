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
    get_default_bitmap_behavior,
    set_default_bitmap_behavior,
    create_output_zip_files,
    LitterBox,
    unzip_files,
    sort_input_images,
    convert_all_to_bitmap,
    clean_up,
    write_status_to_settings_file,
)
from upscale import Upscale

DISCORD_CHARACTER_LIMIT = 2000
FAIL_STATUS = "An error occurred during the upscale process"
IDLE_STATUS = "Idle"


def list_all_models() -> str:
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


def list_bw_models() -> str:
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


def list_c_models() -> str:
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


def set_default_bw_model(model_name) -> str:
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


def set_default_c_model(model_name) -> str:
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


def set_bitmap_mode(bitmap_mode: str) -> str:
    if bitmap_mode.lower() == "true" or bitmap_mode.lower() == "t":
        bitmap_mode_bool = True
    elif bitmap_mode.lower() == "false" or bitmap_mode.lower() == "f":
        bitmap_mode_bool = False
    else:
        return "# Error\nBitmap mode must be true or false [`true, false, t, f`]"

    if set_default_bitmap_behavior(bitmap_mode_bool):
        return "Bitmap mode has been set to `" + str(bitmap_mode_bool) + "`"


def list_settings() -> str:
    default_color_model = get_default_color_model()
    default_black_white_model = get_default_black_white_model()
    bitmap_behavior = get_default_bitmap_behavior()
    message = (
        "# Settings:\nDefault color upscaling model: `"
        + str(default_color_model)
        + "`\nDefault black and white upscaling model: `"
        + str(default_black_white_model)
        + "`\nConvert black and white images to bitmap: `"
        + str(bitmap_behavior)
        + "`"
    )
    return message


def list_commands() -> str:
    # TODO: make this list generated from the list of commands instead
    return (
        "# Commands"
        + "\n- `!upscaler help`: Shows this message"
        + "\n- `!upscaler set model blackwhite [modelname]`: Sets the black and white upscaling model to the provided model"
        + "\n- `!upscaler set model color [modelname]`: Sets the color upscaling model to the provided model"
        + "\n- `!upscaler set bitmap [true/false]`: Sets whether to convert black and white images to bitmaps or not"
        + "\n- `!upscaler show models all`: Displays all available upscaling models"
        + "\n- `!upscaler show models blackwhite`: Displays list of available black and white upscaling models"
        + "\n- `!upscaler show models color`: Displays list of available color upscaling models"
        + "\n- `!upscaler show settings`: Displays current settings"
        + "\n- `!upscaler upscale [link]`: Provided a catbox.moe link or an image file or zip containing images, will download the images and upscale them using the current settings"
    )


def upscale_process(
    link_to_zip: str,
    bw_model: str = None,
    c_model: str = None,
    bitmap_mode: bool = None,
    status_to_file: bool = False,
) -> str:
    try:
        current_status = "Initializing"
        if status_to_file:
            write_status_to_settings_file(current_status)
        print(current_status, flush=True)

        # Download files
        litterbox_client = LitterBox()

        output_folder = os.path.join(os.getcwd(), "output")
        bw_models_folder = os.path.join(os.getcwd(), "models/blackwhite")
        c_models_folder = os.path.join(os.getcwd(), "models/color")

        current_status = "Downloading files"
        if status_to_file:
            write_status_to_settings_file(current_status)
        print(current_status, flush=True)

        downloaded_file = litterbox_client.file_download(link_to_zip)

        if "error" in downloaded_file.lower():
            clean_up()
            return downloaded_file

        current_status = "Download complete"
        if status_to_file:
            write_status_to_settings_file(current_status)

        print(current_status, flush=True)

        if downloaded_file.lower().endswith(".zip"):
            current_status = "Unzipping images"
            if status_to_file:
                write_status_to_settings_file(current_status)
            print(current_status, flush=True)
            # Unzip files
            unzip_files(downloaded_file)
            # Sort images based on color/bw
        else:

            if (
                not downloaded_file.lower().endswith(".png")
                and not downloaded_file.lower().endswith(".jpg")
                and not downloaded_file.lower().endswith(".jpeg")
            ):
                clean_up()
                return "# Error:\nFile must be a PNG or a JPG format (`*.png, *.jpg, *.jpeg`)"

        current_status = "Sorting images"
        if status_to_file:
            write_status_to_settings_file(current_status)
        print(current_status, flush=True)
        sort_input_images()

        # Upscaling
        current_status = "Upscaling images"
        if status_to_file:
            write_status_to_settings_file(current_status)
        print(current_status, flush=True)
        # Upscale the bw images
        if bw_model is None:
            bw_model = os.path.join(bw_models_folder, get_default_black_white_model())

        if bitmap_mode is None:
            bitmap_mode = get_default_bitmap_behavior()

        if bitmap_mode:
            bw_output_path = Path("input/output_pre_bitmap")
        else:
            bw_output_path = Path("output")

        upscale = Upscale(
            model=bw_model,
            input=Path("input/input_blackwhite"),
            output=bw_output_path,
            reverse=False,
            skip_existing=False,
            delete_input=True,
            # seamless=False,
            cpu=True,
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
            skip_existing=False,
            delete_input=True,
            # seamless=False,
            cpu=True,
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

        if bitmap_mode:
            current_status = "Converting to bitmap"
            if status_to_file:
                write_status_to_settings_file(current_status)
            print(current_status, flush=True)
            convert_all_to_bitmap()

        current_status = "Creating zip files"
        if status_to_file:
            write_status_to_settings_file(current_status)
        print(current_status, flush=True)
        # Prepare the files for upload to Litterbox by zipping them in groups of 1 gigabyte
        zip_files = create_output_zip_files()

        current_status = "Uploading files"
        if status_to_file:
            write_status_to_settings_file(current_status)
        print(current_status, flush=True)
        links = []
        for zip_file in zip_files:
            link = litterbox_client.file_upload(
                os.path.join(output_folder, zip_file["filename"]), 72
            )
            print(link, flush=True)
            links.append({"link": link, "files": zip_file["files"]})

        message = "# Upscaling process complete\nThe following zip file(s) have been created with the shown contents"
        for link in links:
            filename = link["link"][link["link"].index(".moe/") + 5 :]
            message += "\n## [" + str(filename) + "](" + link["link"] + ")"
            for file in sorted(link["files"]):
                message += "\n - " + str(file)

        if len(message) >= DISCORD_CHARACTER_LIMIT:
            message = "# Upscaling process complete\nThe following zip file(s) have been created"
            for link in links:
                filename = link["link"][link["link"].index(".moe/") + 5 :]
                message += "\n## [" + str(filename) + "](" + link["link"] + ")"

        clean_up()
        print(message, flush=True)
        if status_to_file:
            write_status_to_settings_file("Idle")
        return message
    except Exception as e:
        print(e, flush=True)
        if status_to_file:
            write_status_to_settings_file(FAIL_STATUS)
        return FAIL_STATUS


upscale_process("https://files.catbox.moe/5ex5xv.zip", None, None, True, False)
