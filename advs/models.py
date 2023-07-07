from typing import Type
from cachetools import cached
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import EmailType

import config

Base = declarative_base()


class HttpError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class User(Base, UserMixin):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(EmailType, unique=True, index=True)
    password = Column(String(60), nullable=False)


class Advertisement(Base):

    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(60), nullable=False)
    description = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")


@cached({})
def get_engine():
    return create_engine(config.PG_DSN)


@cached({})
def get_session_maker():
    return sessionmaker(bind=get_engine())


def init_db():
    Base.metadata.create_all(bind=get_engine())


def close_db():
    get_engine().dispose()


ORM_MODEL_CLS = Type[User] | Type[Advertisement]
ORM_MODEL = User | Advertisement
