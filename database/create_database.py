from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Images(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    img_path = Column(String, nullable=False)
    map = Column(String, nullable=False)
    coordinate_x = Column(Float, nullable=False)
    coordinate_y = Column(Float, nullable=False)


def create_database():
    eng = create_engine('sqlite:///images_database.db')
    Base.metadata.create_all(eng)
    print('Database created!')


if __name__ == '__main__':
    create_database()

