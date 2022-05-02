import sqlalchemy
from .db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    money = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    event = orm.relation('Event')
    bet = orm.relation('Bet')

    def __init__(self, name, money=1000):
        self.name = name
        self.money = money

    def add_money(self, count) -> bool:
        if count > 0:
            self.money += count
            return True
        else:
            return False

    def subtract_money(self, count) -> bool:
        if 0 < count <= self.money:
            self.money -= count
            return True
        else:
            return False
