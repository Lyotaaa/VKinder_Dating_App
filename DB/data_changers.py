from configparser import ConfigParser
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import User, Likes, Dislikes, Favorites, Blocklist, create_tables


def open_session(dsn: str):
    """
    Открывает соединение с БД
    """
    config = ConfigParser()
    config.read("config.ini")
    DSN = config["Vk_info"]["DB_connect"]

    engine = sqlalchemy.create_engine(dsn)
    Session = sessionmaker(bind=engine)
    return Session()


# User
def update_user(session, user_id, age_range, gender, city):
    existing_user = session.query(User).filter_by(user_id=str(user_id)).first()
    if existing_user:
        existing_user.age_range = str(age_range)
        existing_user.gender = True if gender == 1 else False
        existing_user.city = city
        session.commit()
    else:
        session.add(User(
            user_id=str(user_id), age_range=str(age_range), gender=(True if gender == 1 else False), city=city)
        )
        session.commit()


def get_user(user_id):
    return session.query(User).filter_by(user_id=str(user_id)).first()


# Likes

def set_like(session, user_id, like_id):
    existing_like = session.query(Likes).filter_by(user_id=str(user_id), like_id=str(like_id), ).first()
    if existing_like:
        pass
    else:
        session.add(Likes(user_id=str(user_id), like_id=str(like_id)))
        session.commit()


def unset_like(session, user_id, like_id):
    existing_like = session.query(Likes).filter_by(user_id=str(user_id), like_id=str(like_id), ).first()
    if existing_like:
        session.delete(existing_like)
        session.commit()
    else:
        pass


def get_likes(session, user_id):
    q = session.query(Likes).filter_by(user_id=str(user_id))
    return [r.like_id for r in q.all()]


# Dislikes

def set_dislike(session, user_id, dislike_id):
    existing_dislike = session.query(Dislikes).filter_by(user_id=str(user_id), dislike_id=str(dislike_id)).first()
    if existing_dislike:
        pass
    else:
        session.add(Dislikes(user_id=str(user_id), dislike_id=str(dislike_id)))
        session.commit()


def unset_dislike(session, user_id, dislike_id):
    existing_dislike = session.query(Dislikes).filter_by(user_id=str(user_id), dislike_id=str(dislike_id)).first()
    if existing_dislike:
        session.delete(existing_dislike)
        session.commit()
    else:
        pass


def get_dislikes(session, user_id):
    q = session.query(Dislikes).filter_by(user_id=str(user_id))
    return [r.dislike_id for r in q.all()]


# Favorites
def set_favorite(session, user_id, favorite_id):
    existing_favorite = (
        session.query(Favorites)
        .filter_by(user_id=str(user_id), favorite_id=str(favorite_id))
        .first()
    )
    if existing_favorite:
        pass
    else:
        session.add(Favorites(user_id=str(user_id), favorite_id=str(favorite_id)))
        session.commit()


def unset_favorite(session, user_id, favorite_id):
    existing_favorite = (
        session.query(Favorites)
        .filter_by(user_id=str(user_id), favorite_id=str(favorite_id))
        .first()
    )
    if existing_favorite:
        session.delete(existing_favorite)
        session.commit()
    else:
        pass


def get_favorites(session, user_id):
    q = session.query(Favorites).filter_by(user_id=str(user_id))
    return [r.favorite_id for r in q.all()]


# Blocklist
def set_blocklist(session, user_id, block_id):
    existing_block = (
        session.query(Blocklist).filter_by(user_id=str(user_id), block_id=str(block_id)).first()
    )
    if existing_block:
        pass
    else:
        session.add(Blocklist(user_id=str(user_id), block_id=str(block_id)))
        session.commit()


def unset_blocklist(session, user_id, block_id):
<<<<<<< HEAD:DB/data_changers.py
    existing_block = (
        session.query(Blocklist).filter_by(user_id=str(user_id), block_id=block_id).first()
    )
=======
    existing_block = session.query(Blocklist).filter_by(user_id=str(user_id), block_id=str(block_id)).first()
>>>>>>> d73dd2c (Add more Bot to DB integration):data_changers.py
    if existing_block:
        session.delete(existing_block)
        session.commit()
    else:
        pass


def get_blocklist(session, user_id):
<<<<<<< HEAD:DB/data_changers.py
    return session.query(Blocklist).filter_by(user_id=str(user_id))
=======
    q = session.query(Blocklist).filter_by(user_id=str(user_id))
    return [r.block_id for r in q.all()]
>>>>>>> d73dd2c (Add more Bot to DB integration):data_changers.py


# DSN
def get_DSN(file_name):
    config = ConfigParser()
    config.read(file_name)
    return config["DB_info"]["DSN"]


if __name__ == "__main__":
    DSN = get_DSN("../config.ini")
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
