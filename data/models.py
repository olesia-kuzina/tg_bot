import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, default=1)
