import mimetypes
import sys
from os import path
from typing import List

import requests
from dotenv import dotenv_values
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

CATBOX_URL = "https://catbox.moe/user/api.php"

try:
    USERHASH = dotenv_values(".env")["CATBOX_USERHASH"]
    if USERHASH is None or USERHASH == "":
        raise KeyError
except KeyError:
    print(
        "Please enter your CatBox.moe user hash. Script will not work in anonymous mode."
    )
    sys.exit(0)


def get_file_type(filename):
    _, extension = path.splitext(filename)
    if extension == "":
        extension = ".txt"
    mimetypes.init()
    try:
        return mimetypes.types_map[extension]
    except KeyError:
        return "plain/text"


class CatBox:

    @staticmethod
    def file_upload(filename: str):
        file = open(filename, "rb")
        try:
            data = {
                "reqtype": "fileupload",
                "userhash": USERHASH,
                "fileToUpload": (file.name, file, get_file_type(filename)),
            }
            encoder = MultipartEncoder(fields=data)
            monitor = MultipartEncoderMonitor(encoder)
            response = requests.post(
                CATBOX_URL,
                data=monitor,
                headers={"Content-Type": monitor.content_type},
            )
        finally:
            file.close()

        catbox_filename = response.text[response.text.index(".moe/") + 5 :]

        return catbox_filename

    @staticmethod
    def file_delete(catbox_filename: str):
        data = {
            "reqtype": "deletefiles",
            "userhash": USERHASH,
            "files": catbox_filename,
        }
        encoder = MultipartEncoder(fields=data)
        monitor = MultipartEncoderMonitor(encoder)
        response = requests.post(
            CATBOX_URL,
            data=monitor,
            headers={"Content-Type": monitor.content_type},
        )

        return response.text == "Files successfully deleted."

    @staticmethod
    def create_album(album_name: str, description: str, catbox_filenames: List[str]):
        filenames_string = ""
        for catbox_filename in catbox_filenames:
            filenames_string += str(catbox_filename) + " "

        data = {
            "reqtype": "createalbum",
            "userhash": USERHASH,
            "title": album_name,
            "desc": description,
            "files": filenames_string,
        }
        encoder = MultipartEncoder(fields=data)
        monitor = MultipartEncoderMonitor(encoder)
        response = requests.post(
            CATBOX_URL,
            data=monitor,
            headers={"Content-Type": monitor.content_type},
        )

        return response.text

    @staticmethod
    def edit_album(
        catbox_album_string: str,
        album_name: str,
        description: str,
        catbox_filenames: List[str],
    ):
        filenames_string = ""
        for catbox_filename in catbox_filenames:
            filenames_string += str(catbox_filename) + " "

        data = {
            "reqtype": "editalbum",
            "userhash": USERHASH,
            "short": catbox_album_string,
            "title": album_name,
            "desc": description,
            "files": filenames_string,
        }
        encoder = MultipartEncoder(fields=data)
        monitor = MultipartEncoderMonitor(encoder)
        response = requests.post(
            CATBOX_URL,
            data=monitor,
            headers={"Content-Type": monitor.content_type},
        )

        return response.text

    @staticmethod
    def add_to_album(
        catbox_album_string: str,
        catbox_filenames: List[str],
    ):
        filenames_string = ""
        for catbox_filename in catbox_filenames:
            filenames_string += str(catbox_filename) + " "

        data = {
            "reqtype": "addtoalbum",
            "userhash": USERHASH,
            "short": catbox_album_string,
            "files": filenames_string,
        }
        encoder = MultipartEncoder(fields=data)
        monitor = MultipartEncoderMonitor(encoder)
        response = requests.post(
            CATBOX_URL,
            data=monitor,
            headers={"Content-Type": monitor.content_type},
        )

        return response.text

    @staticmethod
    def remove_from_album(
        catbox_album_string: str,
        catbox_filenames: List[str],
    ):
        filenames_string = ""
        for catbox_filename in catbox_filenames:
            filenames_string += str(catbox_filename) + " "

        data = {
            "reqtype": "removefromalbum",
            "userhash": USERHASH,
            "short": catbox_album_string,
            "files": filenames_string,
        }
        encoder = MultipartEncoder(fields=data)
        monitor = MultipartEncoderMonitor(encoder)
        response = requests.post(
            CATBOX_URL,
            data=monitor,
            headers={"Content-Type": monitor.content_type},
        )

        return response.text

    @staticmethod
    def delete_album(
        catbox_album_string: str,
    ):
        data = {
            "reqtype": "deletealbum",
            "userhash": USERHASH,
            "short": catbox_album_string,
        }
        encoder = MultipartEncoder(fields=data)
        monitor = MultipartEncoderMonitor(encoder)
        response = requests.post(
            CATBOX_URL,
            data=monitor,
            headers={"Content-Type": monitor.content_type},
        )

        return response.text
