import sqlalchemy
from models import create_tables
from data_changers import update_user, get_user, press_like, get_likes, press_dislike, get_dislikes, press_favorite, get_favorites



if __name__ == '__main__':
    DSN = 'postgresql://postgres:6996@localhost:5432/VKinder'
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)
