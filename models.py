from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Sequence,
    DateTime,
    ForeignKey, ARRAY, Table, Numeric, MetaData, select, SmallInteger
)
from sqlalchemy.orm import relationship
from wheel.util import as_unicode

import constants
from database import Base
from log_managment import create_logger
logger = create_logger('{}.log'.format(__name__))


class GameDate(Base):
    __tablename__ = constants.TABLE_NAME_GAME_DAY
    id = Column('id', Integer, Sequence("euro_game_day_id_seq"), primary_key=True)
    game_date = Column('game_date', DateTime, unique=True, nullable=False, default=datetime.now)
    euroall = relationship("EuroAll", back_populates="game_date")
    winresults = relationship("WinResults", back_populates="game_date")

    def __repr__(self):
        return self.game_date

    def get_id(self):
        return as_unicode(self.id)

    def get_game_date(self):
        return as_unicode(self.game_date)

    def get_game_date_str(self):
        return self.game_date.strftime("%d-%m-%Y")

    def get_game_date_id_by_date(self, date):
        try:
            return GameDate.query.filter_by(game_date=date).first().id
        except Exception as e:
            print(e)
            return None


class EuroAll(Base):
    __tablename__ = constants.TABLE_NAME_ALL
    id = Column(Integer, primary_key=True, index=True)
    game_date_id = Column(Integer, ForeignKey('euro_game_day.id'))
    game_date = relationship("GameDate", back_populates="euroall")
    million = Column('million', String, nullable=True, default='')
    ball_week_1 = Column('ball_week_1', SmallInteger, nullable=False)
    ball_week_2 = Column('ball_week_2', SmallInteger, nullable=False)
    ball_week_3 = Column('ball_week_3', SmallInteger, nullable=False)
    ball_week_4 = Column('ball_week_4', SmallInteger, nullable=False)
    ball_week_5 = Column('ball_week_5', SmallInteger, nullable=False)
    star_week_1 = Column('star_week_1', SmallInteger, nullable=False)
    star_week_2 = Column('star_week_2', SmallInteger, nullable=False)

    def __repr__(self):
        return self.game_date

    def get_id(self):
        return as_unicode(self.id)

    def get_game_date(self):
        return as_unicode(self.game_date)

    def get_game_date_str(self):
        return self.game_date.strftime("%d-%m-%Y")

    def get_game_date_id_by_date(self, date):
        try:
            return EuroAll.query.filter_by(game_date=date).first().id
        except Exception as e:
            print(e)
            return None


class WinResults(Base):
    __tablename__ = constants.TABLE_NAME_WIN_RESULTS
    id = Column(Integer, primary_key=True, index=True)
    game_date_id = Column(Integer, ForeignKey('euro_game_day.id'))
    game_date = relationship("GameDate", back_populates="winresults")
    five_two_winners = Column('five_two_winners', Numeric, nullable=True)
    five_two_money = Column('five_two_money', Numeric, nullable=True)
    five_one_winners = Column('five_one_winners', Numeric, nullable=True)
    five_one_money = Column('five_one_money', Numeric, nullable=True)
    five_winners = Column('five_winners', Numeric, nullable=True)
    five_money = Column('five_money', Numeric, nullable=True)
    four_two_winners = Column('four_two_winners', Numeric, nullable=True)
    four_two_money = Column('four_two_money', Numeric, nullable=True)
    four_one_winners = Column('four_one_winners', Numeric, nullable=True)
    four_one_money = Column('four_one_money', Numeric, nullable=True)
    four_winners = Column('four_winners', Numeric, nullable=True)
    four_money = Column('four_money', Numeric, nullable=True)
    three_two_winners = Column('three_two_winners', Numeric, nullable=True)
    three_two_money = Column('three_two_money', Numeric, nullable=True)
    three_one_winners = Column('three_one_winners', Numeric, nullable=True)
    three_one_money = Column('three_one_money', Numeric, nullable=True)
    three_winners = Column('three_winners', Numeric, nullable=True)
    three_money = Column('three_money', Numeric, nullable=True)
    two_two_winners = Column('two_two_winners', Numeric, nullable=True)
    two_two_money = Column('two_two_money', Numeric, nullable=True)
    two_one_winners = Column('two_one_winners', Numeric, nullable=True)
    two_one_money = Column('two_one_money', Numeric, nullable=True)
    one_two_winners = Column('one_two_winners', Numeric, nullable=True)
    one_two_money = Column('one_two_money', Numeric, nullable=True)

    def __repr__(self):
        return self.game_date

    def get_id(self):
        return as_unicode(self.id)

    def get_game_date(self):
        return as_unicode(self.game_date)

    def get_game_date_str(self):
        return self.game_date.strftime("%d-%m-%Y")

    def get_game_date_id_by_date(self, date):
        try:
            return WinResults.query.filter_by(game_date=date).first().id
        except Exception as e:
            print(e)
            return None
