import io
from pathlib import Path

from apiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials

from upscale import Upscale

scopes = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
]

V1_PATH = "./models/4x_eula_digimanga_bw_v1_860k.pth"

V2_PATH = "./models/4x_eula_digimanga_bw_v2_nc1_307k.pth"

creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, scopes)


def get_input_files():
    try:
        service = build("drive", "v3", credentials=creds)
        files = []
        page_token = None
        while True:
            response = (
                service.files()
                .list(
                    q="'" + INPUT_FOLDER_ID + "' in parents",
                    spaces="drive",
                    fields="nextPageToken, " "files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )
            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

    except HttpError as error:
        print(f"An error occurred: {error}")
        files = None

    return files


def get_output_files():
    """Search file in drive location

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)
        files = []
        page_token = None
        while True:
            # pylint: disable=maybe-no-member
            response = (
                service.files()
                .list(
                    q="'" + OUTPUT_FOLDER_ID + "' in parents",
                    spaces="drive",
                    fields="nextPageToken, " "files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )
            for file in response.get("files", []):
                # Process change
                print(f'Found file: {file.get("name")}, {file.get("id")}')
            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

    except HttpError as error:
        print(f"An error occurred: {error}")
        files = None

    return files


def download_file(file_id, file_name):
    try:
        service = build("drive", "v3", credentials=creds)

        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    with open("./input/" + file_name, "wb") as f:
        f.write(file.getbuffer())


def upload_file(file_path, file_name):
    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)

        file_metadata = {"name": file_name, "parents": [OUTPUT_FOLDER_ID]}
        media = MediaFileUpload(file_path, mimetype="image/png")

        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(f'File ID: {file.get("id")}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.get("id")


def get_new_files():
    input_files = get_input_files()
    output_files = get_output_files()
    old_files = []
    new_files = []

    for input_file in input_files:
        for output_file in output_files:
            if (
                input_file["name"][: input_file["name"].index(".")]
                == output_file["name"][: output_file["name"].index(".")]
            ):
                old_files.append(input_file)
                break

    for input_file in input_files:
        if input_file not in old_files:
            new_files.append(input_file)

    return new_files


def download_new_files(new_files):
    print("New files: " + str(new_files))

    for file in new_files:
        if file["name"][file["name"].index(".") :].lower() in [".jpg", ".jpeg", ".png"]:
            download_file(file["id"], file["name"])


def upscaling_process(channel, upscaler):
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
    num_new_files = 0
