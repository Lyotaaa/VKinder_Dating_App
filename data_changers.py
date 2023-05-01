
from configparser import ConfigParser
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import User, Likes, Dislikes, Favorites, Blocklist

DSN = 'postgresql://postgres:6996@localhost:5432/VKinder'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

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
def update_user(user_id, age_range, gender, city):
    existing_user = session.query(User).filter_by(user_id=user_id).first()
    if existing_user:
        existing_user.age_range = age_range
        existing_user.gender = gender
        existing_user.city = city
        session.commit()
    else:
        session.add(User(user_id=user_id, age_range=age_range, gender=gender, city=city))
        session.commit()


def get_user(user_id):
    return session.query(User).filter_by(user_id=user_id).first()


# Likes
def press_like(user_id, like_id):
    existing_like = session.query(Likes).filter_by(user_id=user_id, like_id=like_id, ).first()
    if existing_like:
        session.delete(existing_like)
        session.commit()
    else:
        session.add(Likes(user_id=user_id, like_id=like_id))
        session.commit()


def get_likes(session, user_id):
    q = session.query(Likes).filter_by(user_id=str(user_id))
    return [r[1] for r in q.all()]


# Dislikes
def press_dislike(user_id, dislike_id):
    existing_dislike = session.query(Dislikes).filter_by(user_id=user_id, dislike_id=dislike_id).first()
    if existing_dislike:
        session.delete(existing_dislike)
        session.commit()
    else:
        session.add(Dislikes(user_id=user_id, dislike_id=dislike_id))
        session.commit()


def get_dislikes(session, user_id):
    q = session.query(Dislikes).filter_by(user_id=str(user_id))
    return [r[1] for r in q.all()]


# Favorites
def press_favorite(user_id, favorite_id):
    existing_favorite = session.query(Favorites).filter_by(user_id=user_id, favorite_id=favorite_id).first()
    if existing_favorite:
        session.delete(existing_favorite)
        session.commit()
    else:
        session.add(Favorites(user_id=user_id, favorite_id=favorite_id))
        session.commit()


def get_favorites(session, user_id):
    q = session.query(Favorites).filter_by(user_id=str(user_id))
    return [r[1] for r in q.all()]


# Blocklist

def press_blocklist(user_id, block_id):
    existing_block = session.query(Blocklist).filter_by(user_id=user_id, block_id=block_id).first()
    if existing_block:
        session.delete(existing_block)
        session.commit()
    else:
        session.add(Blocklist(user_id=user_id, block_id=block_id))
        session.commit()


def get_blocklist(user_id):
    return session.query(Blocklist).filter_by(user_id=user_id)
