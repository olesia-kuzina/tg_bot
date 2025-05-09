import logging

from .db_session import create_session
from .models import User

class DataBase:
    @staticmethod
    def add_user(name: str, tg_id: int):
        session = create_session()
        user = session.query(User).filter(User.tg_id == tg_id).first()
        if user:
            if user.user_name != name:
                user.user_name = name
                logging.info(f'updated username({name}) for user {tg_id}')
        else:
            user = User()
            user.tg_id = tg_id
            user.user_name = name
            session.add(user)
            logging.info(f'added user [{name}: {tg_id}]')
        session.commit()
        session.close()

    @staticmethod
    def get_count(tg_id: int):
        session = create_session()
        count = session.query(User.count).filter(User.tg_id == tg_id).first()[0]
        session.close()
        return count

    @staticmethod
    def increment_count(tg_id: int):
        session = create_session()
        user = session.query(User).filter(User.tg_id == tg_id).first()
        if user:
            user.count += 1
            session.commit()
        session.close()

    @staticmethod
    def get_users():
        session = create_session()
        users = session.query(User).all()
        users = [f"{user.id} {user.user_name} {user.tg_id}" for user in users]
        session.close()
        return users