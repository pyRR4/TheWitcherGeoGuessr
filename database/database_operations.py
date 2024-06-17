from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from TheWitcherGeoGuessr.database.create_database import Base, Images


def create_session(db):
    engine = create_engine(f'sqlite:///{db}.db')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def load_image(db, path, map_name, coordinates):
    session = create_session(db)

    coordinate_x, coordinate_y = coordinates

    new_img = Images(
        img_path=path,
        map=map_name,
        coordinate_x=coordinate_x,
        coordinate_y=coordinate_y,
    )

    session.add(new_img)
    session.commit()
    session.close()

    return True


def delete_image_by_id(db, image_id):
    session = create_session(db)

    image_to_delete = session.query(Images).filter_by(id=image_id).first()

    if image_to_delete:
        session.delete(image_to_delete)
        session.commit()
        print(f"Image with id {image_id} deleted successfully.")
    else:
        print(f"Image with id {image_id} not found.")

    session.close()


def get_all_images(db):
    session = create_session(db)

    images = session.query(Images).all()

    image_list = []
    for image in images:
        image_dict = {
            'id': image.id,
            'img_path': image.img_path,
            'map': image.map,
            'coordinate_x': image.coordinate_x,
            'coordinate_y': image.coordinate_y
        }
        image_list.append(image_dict)

    session.close()

    return image_list


def get_items_by_map(db, game_map):
    session = create_session(db)

    images = session.query(Images).filter(Images.map == game_map).all()

    image_list = []
    for image in images:
        image_dict = {
            'id': image.id,
            'img_path': image.img_path,
            'map': image.map,
            'coordinate_x': image.coordinate_x,
            'coordinate_y': image.coordinate_y
        }
        image_list.append(image_dict)

    session.close()

    return image_list


def get_unique_maps(db):
    session = create_session(db)

    unique_maps = session.query(Images.map).distinct().all()
    session.close()

    unique_maps = [game_map[0] for game_map in unique_maps]
    return unique_maps


def get_coordinates_by_path(db, path):
    session = create_session(db)

    coordinates = session.query(Images.coordinate_x, Images.coordinate_y).filter(Images.img_path == path).first()

    session.close()

    if coordinates:
        coordinate_x, coordinate_y = coordinates
        return coordinate_x, coordinate_y
    else:
        return None

