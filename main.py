from configparser import ConfigParser
import sqlalchemy
from models import create_tables
from data_changers import update_user, get_user, press_like, get_likes, press_dislike, get_dislikes, press_favorite, get_favorites

def get_db(file_name):
    """
    Берёт строчку для коннекта с БД
    """
    config = ConfigParser()
    config.read(file_name)
    group_token = config["Vk_info"]["DB_connect"]
    return group_token

if __name__ == '__main__':
    DSN = get_db("config.ini")
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)
