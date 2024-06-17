import os
import random
import shutil

from TheWitcherGeoGuessr.database.database_operations import get_items_by_map, get_unique_maps

images_path = (f"C:\\Users\\igopo\\OneDrive\\Pulpit\\Wszystko i nic\\IST 22-27\\IV sem\\JS\\TheWitcherGeoGuessr"
               f"\\TheWitcherGeoGuessr\\images\\")


def add_image(image):
    if os.path.exists(os.path.join(images_path, os.path.basename(image))):
        pass
    elif os.path.exists(image):
        shutil.copy(image, images_path)
    else:
        raise FileNotFoundError("Image not found")


def remove_image(image):
    if os.path.exists(image):
        os.remove(image)
    else:
        raise FileNotFoundError("Image not found")


def get_file_count(game_map):
    try:
        path = os.path.join(images_path, game_map)

        if not os.path.exists(path):
            raise ValueError("Podana mapa nie istnieje.")

        items = os.listdir(path)
        directories = [item for item in items if os.path.isdir(os.path.join(path, item))]
        count = len(directories)

        return count

    except FileNotFoundError:
        return None


def random_map():
    try:
        maps = get_unique_maps('images_database')
        if len(maps) > 0:
            selected_map = random.choice(maps)
        else:
            selected_map = None
        #return selected_map
        return "velen_novigrad"
    except FileNotFoundError:
        return None


def random_image(game_map):
    try:
        images = get_items_by_map('images_database', game_map)
        if len(images) > 0:
            selected_image = random.choice(images)
        else:
            return None
        return selected_image['img_path']
    except FileNotFoundError:
        return None


def random_dir(path):
    try:
        items = os.listdir(path)
        directories = [item for item in items if os.path.isdir(os.path.join(path, item))]

        if not directories:
            raise FileNotFoundError

        random_folder = random.choice(directories)
        return random_folder

    except FileNotFoundError:
        return None
