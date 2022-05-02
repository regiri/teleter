import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Bet(SqlAlchemyBase):
    __tablename__ = 'bets'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    event_open_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("events.open_id"))
    bet_cnt = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    is_first = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)

    event = orm.relation('Event', back_populates='bet')
    user = orm.relation('User', back_populates='bet')

    def __init__(self, event_open_id, user_id, is_first, bet_cnt=0):
        self.event_open_id = event_open_id
        self.is_first = is_first
        self.user_id = user_id
        self.bet_cnt = bet_cnt

    def add_money(self, money):
        self.bet_cnt += money
