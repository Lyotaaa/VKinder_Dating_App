import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    user_id = sq.Column(sq.Integer, primary_key=True)
    age = sq.Column(sq.Integer)
    gender = sq.Column(sq.Boolean)

    likes = relationship('Likes', back_populates='user')
    dislikes = relationship('Dislikes', back_populates='user')
    favorites = relationship('Favorites', back_populates='user')


class Likes(Base):
    __tablename__ = 'likes'
    likes_url = sq.Column(sq.String(length=200), primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)

    user = relationship('User', back_populates='likes')

    def __str__(self):
        return f'user_id: {self.user_id} | likes_url: {self.likes_url}'


class Dislikes(Base):
    __tablename__ = 'dislikes'
    dislikes_url = sq.Column(sq.String(length=200), primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)

    user = relationship('User', back_populates='dislikes')

    def __str__(self):
        return f'user_id: {self.user_id} | dislikes_url: {self.dislikes_url}'


class Favorites(Base):
    __tablename__ = 'favorites'
    favorites_url = sq.Column(sq.String(length=200), primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)

    user = relationship('User', back_populates='favorites')

    def __str__(self):
        return f'user_id: {self.user_id} | favorites_url: {self.favorites_url}'



def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)