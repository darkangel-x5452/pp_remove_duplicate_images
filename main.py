import shutil

from PIL import Image
import imagehash
import os

import dotenv

dotenv.load_dotenv()
def calculate_hash(image_path: str):
    # Open and convert the image to a grayscale mode
    image = Image.open(image_path).convert('L')
    # Set the desired width and height
    new_width = 500
    new_height = 500

    # Resize the image
    resized_image = image.resize((new_width, new_height))
    # Calculate the hash
    # image_hash = imagehash.average_hash(image)
    image_hash = imagehash.dhash(resized_image)

    return image_hash

def create_hash_ls(folder_path: str):
    hash_dict = {}

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            image_hash = calculate_hash(file_path)

            # Check if the hash already exists
            if image_hash in hash_dict:
                hash_dict[str(image_hash)].append(file_path)
            else:
                hash_dict[str(image_hash)] = [file_path]

    return hash_dict


def move_duplicates(selected_ls: dict, raw_ls: dict, dupe_dir: str):

    for _hash, _photo_fps in selected_ls.items():

        if _hash in raw_ls.keys():
            print(f"found dupe, {_hash}, {raw_ls[_hash]}")
            raw_photos = raw_ls[_hash]
            for raw_photo_fp in raw_photos:
                shutil.move(raw_photo_fp, dupe_dir)


def run_app():
    selected_photo_dir = os.getenv("SELECTED_PHOTO_DIR")
    raw_photo_dir = os.getenv("RAW_PHOTO_DIR")
    dup_photos_dir = os.getenv("DUP_PHOTOS_DIR")

    print("get raw hash list")
    raw_photo_hash_ls = create_hash_ls(raw_photo_dir)
    print("get selected hash list")
    selected_photo_has_ls = create_hash_ls(selected_photo_dir)

    print("moving dupes")
    move_duplicates(selected_ls=selected_photo_has_ls, raw_ls=raw_photo_hash_ls, dupe_dir=dup_photos_dir)


if __name__ == '__main__':
    run_app()
