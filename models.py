import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    user_url = sq.Column(sq.String(length=200), primary_key=True)
    age_range = sq.Column(sq.String(length=6))  # 18-999
    gender = sq.Column(sq.Boolean)
    city = sq.Column(sq.String(length=50))

    likes = relationship('Likes', back_populates='user')
    dislikes = relationship('Dislikes', back_populates='user')
    favorites = relationship('Favorites', back_populates='user')


class Likes(Base):
    __tablename__ = 'likes'
    like_url = sq.Column(sq.String(length=200), primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)

    user = relationship('User', back_populates='likes')

    def __str__(self):
        return f'user_id: {self.user_id} | like_url: {self.like_url}'


class Dislikes(Base):
    __tablename__ = 'dislikes'
    dislike_url = sq.Column(sq.String(length=200), primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)

    user = relationship('User', back_populates='dislikes')

    def __str__(self):
        return f'user_id: {self.user_id} | dislike_url: {self.dislike_url}'


class Favorites(Base):
    __tablename__ = 'favorites'
    favorite_url = sq.Column(sq.String(length=200), primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)

    user = relationship('User', back_populates='favorites')

    def __str__(self):
        return f'user_id: {self.user_id} | favorite_url: {self.favorite_url}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
