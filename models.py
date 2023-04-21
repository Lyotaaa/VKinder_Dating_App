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


class Likes(Base):
    __tablename__ = 'likes'
    likes_url = sq.Column(sq.String(length=200), primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)

    user = relationship('User', back_populates='liked')

    def __str__(self):
        return f'user_id: {self.user_id} | likes_url: {self.dislikes_url}'


class Dislikes(Base):
    __tablename__ = 'disliked'
    dislikes_url = sq.Column(sq.String(length=200), primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.user_id'), nullable=False)

    user = relationship('User', back_populates='disliked')

    def __str__(self):
        return f'user_id: {self.user_id} | dislike_url: {self.dislikes_url}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)