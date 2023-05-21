import sqlalchemy as sq
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id = sq.Column(sq.String(length=20), primary_key=True)
    age_range = sq.Column(sq.String(length=5))  # 18-99
    gender = sq.Column(sq.Integer)
    city = sq.Column(sq.String(length=50))

    likes = relationship("Likes", back_populates="user")
    dislikes = relationship("Dislikes", back_populates="user")
    favorites = relationship("Favorites", back_populates="user")
    blocklist = relationship("Blocklist", back_populates="user")

    def __str__(self):
        return f"user_id: {self.user_id} | age_range: {self.age_range} | gender: {self.gender}, city: {self.city}"


class Likes(Base):
    __tablename__ = "likes"
    user_id = sq.Column(
        sq.String(length=20), sq.ForeignKey("user.user_id"), nullable=False
    )
    like_id = sq.Column(sq.String(length=20), nullable=False)

    user = relationship("User", back_populates="likes")

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "like_id"),
        {},
    )

    def __str__(self):
        return f"user_id: {self.user_id} | like_id: {self.like_id}"


class Dislikes(Base):
    __tablename__ = "dislikes"
    user_id = sq.Column(
        sq.String(length=20), sq.ForeignKey("user.user_id"), nullable=False
    )
    dislike_id = sq.Column(sq.String(length=20), nullable=False)

    user = relationship("User", back_populates="dislikes")

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "dislike_id"),
        {},
    )

    def __str__(self):
        return f"user_id: {self.user_id} | dislike_id: {self.dislike_id}"


class Favorites(Base):
    __tablename__ = "favorites"
    user_id = sq.Column(
        sq.String(length=20), sq.ForeignKey("user.user_id"), nullable=False
    )
    favorite_id = sq.Column(sq.String(length=20), nullable=False)

    user = relationship("User", back_populates="favorites")

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "favorite_id"),
        {},
    )

    def __str__(self):
        return f"user_id: {self.user_id} | favorite_id: {self.favorite_id}"


class Blocklist(Base):
    __tablename__ = "blocklist"
    user_id = sq.Column(
        sq.String(length=20), sq.ForeignKey("user.user_id"), nullable=False
    )
    block_id = sq.Column(sq.String(length=20), nullable=False)

    user = relationship("User", back_populates="blocklist")

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "block_id"),
        {},
    )

    def __str__(self):
        return f"user_id: {self.user_id} | block_id: {self.block_id}"


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
