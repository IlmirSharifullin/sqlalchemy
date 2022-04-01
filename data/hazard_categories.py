import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class HazardCategory(SqlAlchemyBase):
    __tablename__ = 'hazard_categories'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    hazard_category = sqlalchemy.Column(sqlalchemy.String, nullable=True)