"""import bot

if __name__ == "__main__":
    bot.run_discord_bot()
"""

import datetime
import json
import os

from lib import (
    CatBox,
    add_content,
    remove_content,
    LitterBox,
    unzip_files,
    sort_input_images,
)

STORAGE_FILENAME = "catbox_storage.json"


def download_content():
    print("Hello")


def upload_content():
    output_folder = os.path.join(os.getcwd(), "output")
    catbox_client = CatBox()

    new_files = []
    time = datetime.datetime.now().ctime()

    album_name = time + " upscaled images"
    album_description = "Images upscaled on " + time

    for file in os.listdir(output_folder):
        catbox_filename = catbox_client.file_upload(os.path.join(output_folder, file))
        new_files.append(catbox_filename)
        print(catbox_filename)

    catbox_album_string = catbox_client.create_album(
        album_name, album_description, new_files
    )

    print(catbox_album_string)

    file_storage = []

    for new_file in new_files:
        file_storage.append(
            {
                "image_name": new_file,
                "datetime": time,
            }
        )

    add_content(
        file_storage,
        [
            {
                "album_name": album_name,
                "catbox_album_string": catbox_album_string,
                "description": album_description,
                "images": file_storage,
                "datetime": time,
            }
        ],
    )


def delete_old_content():
    current_time = datetime.datetime.now()

    with open(STORAGE_FILENAME, "r+") as file:
        file_data = json.load(file)

    for album in file_data["albums"]:
        catbox_client = CatBox()
        album_time = datetime.datetime.strptime(
            album["datetime"], "%a %b %d %H:%M:%S %Y"
        )
        if ((current_time - album_time).total_seconds() / 360) >= 3:
            print(album["catbox_album_string"])
            album_code = album["catbox_album_string"][
                album["catbox_album_string"].find("/c/") + 3 :
            ]
            album_images = album["images"]
            for album_image in album_images:
                print(album_image["image_name"])
                catbox_client.file_delete(album_image["image_name"])
            catbox_client.delete_album(album_code)

            remove_content(album["images"], [album])


def handle_command(user_command: str, user_id: str):
    print("na")


litterbox_client = LitterBox()
# upload_url = litterbox_client.file_upload("./output/Raw.zip", 72)

# print(upload_url)
upload_url = "https://files.catbox.moe/wj3fu7.zip"
# print("Downloading file...")
# res = litterbox_client.file_download(upload_url)
print("Unzipping file...")
unzip_files("./input/wj3fu7.zip")
print("Sorting images...")
sort_input_images()
