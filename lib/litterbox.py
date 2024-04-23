import mimetypes
import sys
from os import path, getcwd
from typing import Optional

import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

CATBOX_URL = "https://catbox.moe/user/api.php"


def get_file_type(filename):
    _, extension = path.splitext(filename)
    if extension == "":
        extension = ".txt"
    mimetypes.init()
    try:
        return mimetypes.types_map[extension]
    except KeyError:
        return "plain/text"


class LitterBox:

    @staticmethod
    def _progress_bar(monitor):
        progress = int(monitor.bytes_read / monitor.len * 20)
        sys.stdout.write("\r[{}/{}] bytes |".format(monitor.bytes_read, monitor.len))
        sys.stdout.write("{}>".format("=" * progress))
        sys.stdout.write("{}|".format(" " * (20 - progress)))
        sys.stdout.flush()

    def file_upload(self, filename: str, time: int) -> Optional[str]:
        if time == 1:
            time_formatted = "1h"
        elif time == 12:
            time_formatted = "12h"
        elif time == 24:
            time_formatted = "24h"
        elif time == 72:
            time_formatted = "72h"
        else:
            print("Time must be 1, 12, 24, or 72")
            return None

        file = open(filename, "rb")
        try:
            data = {
                "reqtype": "fileupload",
                "time": time_formatted,
                "fileToUpload": (file.name, file, get_file_type(filename)),
            }
            encoder = MultipartEncoder(fields=data)
            monitor = MultipartEncoderMonitor(encoder, callback=self._progress_bar)
            response = requests.post(
                CATBOX_URL,
                data=monitor,
                headers={"Content-Type": monitor.content_type},
            )
        finally:
            file.close()

        catbox_filename = response.text

        return catbox_filename

    @staticmethod
    def file_download(url: str):
        filename = url[url.index(".moe/") + 5 :]
        input_folder = path.join(getcwd(), "input")
        file_path = path.join(input_folder, filename)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    if chunk:
                        f.write(chunk)
        return file_path
