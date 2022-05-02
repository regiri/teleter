import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Event(SqlAlchemyBase):
    __tablename__ = 'events'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    creator = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    first_end = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    first_bank = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    second_end = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    second_bank = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    min_raise = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    closed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)

    user_created = orm.relation('User', back_populates='event')

    def __init__(self, creator, name, first_end, second_end, min_raise=0):
        self.creator = creator
        self.name = name
        self.first_end = first_end
        self.second_end = second_end
        self.min_raise = min_raise
        self.first_bank = 0
        self.second_bank = 0
        self.closed = False

    def close_event(self):
        self.closed = True
