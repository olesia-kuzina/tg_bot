from .db_session import create_session
from .models import User

class DataBase:
    @staticmethod
    def add_user(name: str, tg_id: int):
        session = create_session()
        user = User()
        user.tg_id = tg_id
        user.user_name = name
        session.add(user)
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
        user.count += 1
        session.commit()
        session.close()