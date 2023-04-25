import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import User, Likes, Dislikes, Favorites


DSN = 'postgresql://postgres:6996@localhost:5432/VKinder'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()


def create_user(user_url, age_range, gender, city):
    existing_user = session.query(User).filter_by(user_url=user_url).first()
    if existing_user:
        existing_user.age_range = age_range
        existing_user.gender = gender
        existing_user.city = city
        session.commit()
    else:
        session.add(User(user_url=user_url, age_range=age_range, gender=gender, city=city))
        session.commit()


def press_like(like_url, user_url):
    existing_like = session.query(Likes).filter_by(like_url=like_url, user_url=user_url).first()
    if existing_like:
        session.delete(existing_like)
        session.commit()
    else:
        session.add(Likes(like_url=like_url, user_url=user_url))
        session.commit()


def press_dislike(dislike_url, user_url):
    existing_dislike = session.query(Dislikes).filter_by(dislike_url=dislike_url, user_url=user_url).first()
    if existing_dislike:
        session.delete(existing_dislike)
        session.commit()
    else:
        session.add(Dislikes(dislike_url=dislike_url, user_url=user_url))
        session.commit()


def press_favorite(favorite_url, user_url):
    existing_favorite = session.query(Favorites).filter_by(favorite_url=favorite_url, user_url=user_url).first()
    if existing_favorite:
        session.delete(existing_favorite)
        session.commit()
    else:
        session.add(Favorites(favorite_url=favorite_url, user_url=user_url))
        session.commit()
