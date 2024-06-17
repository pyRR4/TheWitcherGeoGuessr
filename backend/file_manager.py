import os
import random

images_path = (f"C:\\Users\\igopo\\OneDrive\\Pulpit\\Wszystko i nic\\IST 22-27\\IV sem\\JS\\TheWitcherGeoGuessr"
            f"\\TheWitcherGeoGuessr\\images\\")


def get_file(game_map, number):
    try:
        path = os.path.join(images_path, game_map, number)
        if os.path.exists(path):
            with open(f"{path}/coordinates.txt", "rb") as file:
                coordinates = get_coordinates(file.read())

                return f"{path}\\img.jpg", coordinates
    except FileNotFoundError:
        return None, None


def get_coordinates(coordinates_string):
    stripped = coordinates_string.strip()
    stripped = stripped[1:-1]
    parts = stripped.split(b',')
    result = tuple(float(part) for part in parts)

    return result


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


def create_folder_with_file(game_map, x, y):
    try:
        path = os.path.join(images_path, game_map)

        if not os.path.exists(path):
            raise ValueError("Podana mapa nie istnieje.")

        folder_path = os.path.join(path, str(get_file_count(game_map) + 1))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, 'coordinates.txt')

        with open(file_path, 'w') as file:
            file.write(f"{x},{y}")
            file.close()

    except FileNotFoundError:
        pass


def random_map():
    try:
        selected_map = random_dir(images_path)
        #return selected_map
        return "velen_novigrad"
    except FileNotFoundError:
        return None


def random_image(game_map):
    try:
        selected_image = random_dir(os.path.join(images_path, game_map))
        return selected_image
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
