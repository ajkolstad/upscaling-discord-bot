import datetime
import json
import os


FILENAME = "catbox_storage.json"
BASE_FORMAT = {"images": [], "albums": []}

IMAGE_FORMAT = {
    "image_name": "",
    "datetime": datetime.datetime.now().ctime(),
}

ALBUM_FORMAT = {
    "album_name": "",
    "catbox_album_string": "",
    "description": "",
    "images": [],
    "datetime": datetime.datetime.now().ctime(),
}


def add_content(new_images, new_albums):
    if not os.path.isfile(FILENAME):
        with open(FILENAME, "w") as outfile:
            json.dump(BASE_FORMAT, outfile)

    with open(FILENAME, "r+") as file:
        file_data = json.load(file)
        for new_image in new_images:
            file_data["images"].append(new_image)
            file.seek(0)

        for new_album in new_albums:
            file_data["albums"].append(new_album)
            file.seek(0)

        json.dump(file_data, file, indent=4)


def remove_content(old_images, old_albums):
    if not os.path.isfile(FILENAME):
        with open(FILENAME, "w") as outfile:
            json.dump(BASE_FORMAT, outfile)
        return

    with open(FILENAME, "r+") as file:
        file_data = json.load(file)
        for old_image in old_images:
            if old_image in file_data["images"]:
                file_data["images"].remove(old_image)

        for old_album in old_albums:
            if old_album in file_data["albums"]:
                file_data["albums"].remove(old_album)

    with open(FILENAME, "w") as file:
        json.dump(file_data, file, indent=4)
