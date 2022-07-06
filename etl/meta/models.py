import logging
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Sequence,
    DateTime,
    ForeignKey, Numeric, SmallInteger, Index, UniqueConstraint, Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from wheel.util import as_unicode

from etl.utils import constants
from etl.controller.database import Base
from etl.utils.log_managment import init_logger

init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)


# for Api
class Draw(Base):
    __tablename__ = constants.TABLE_DRAWS

    id = Column('id', UUID(as_uuid=True), Sequence('draw_id_seq'), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    draw_id = Column(String, unique=True)
    numbers = Column(ARRAY(Integer))
    stars = Column(ARRAY(Integer))
    date = Column(DateTime)
    prize = Column(Numeric)
    has_winner = Column(Boolean)

    __table_args__ = (UniqueConstraint('id', 'draw_id', name='draw_id_constrain'), Index('draw_id_index', 'draw_id'))

    def __init__(self, draw_id, numbers, stars, date, prize, has_winner):
        self.draw_id = draw_id
        self.numbers = numbers
        self.stars = stars
        self.date = date
        self.prize = prize
        self.has_winner = has_winner

    def __repr__(self):
        return '<Draw {}>'.format(self.draw_id)

    def __str__(self):
        return '<Draw {}>'.format(self.draw_id)

    def __eq__(self, other):
        return self.draw_id == other.draw_id

    def __hash__(self):
        return hash(self.draw_id)

    def to_dict(self):
        return {
            'id': self.id,
            'draw_id': self.draw_id,
            'numbers': self.numbers,
            'stars': self.stars,
            'date': self.date,
            'prize': self.prize,
            'has_winner': self.has_winner
        }

    def to_json(self):
        return {
            'id': self.id,
            'draw_id': self.draw_id,
            'numbers': self.numbers,
            'stars': self.stars,
            'date': self.date,
            'prize': self.prize,
            'has_winner': self.has_winner
        }

    def to_csv(self):
        return '{},{},{},{},{},{},{}'.format(
            self.id,
            self.draw_id,
            self.numbers,
            self.stars,
            self.date,
            self.prize,
            self.has_winner
        )


class GameDate(Base):
    __tablename__ = constants.TABLE_NAME_GAME_DAY
    #  id = Column('id', Integer, Sequence("euro_game_day_id_seq"), primary_key=True)
    id = Column('id', UUID(as_uuid=True), Sequence("euro_game_day_id_seq"), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    game_date = Column('game_date', DateTime, unique=True, nullable=False, default=datetime.now)
    euroall = relationship("EuroAll", back_populates="game_date")
    winresults = relationship("WinResults", back_populates="game_date")
    eurostarnumbers = relationship("EuroStarNumbers", back_populates="game_date")
    unionnumbers = relationship("UnionNumbers", back_populates="game_date")
    unionstars = relationship("UnionStars", back_populates="game_date")

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
    # id = Column(Integer, Sequence("euro_all_seq"), primary_key=True, index=True)
    id = Column('id', UUID(as_uuid=True), Sequence("euro_all_seq"), primary_key=True, default=uuid.uuid4, unique=True,
                nullable=False)
    # game_date_id = Column(Integer, ForeignKey('euro_game_day.id'))
    game_date_id = Column(UUID(as_uuid=True), ForeignKey('euro_game_day.id'))
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
    # id = Column(Integer, Sequence("win_results_seq"), primary_key=True, index=True)
    id = Column('id', UUID(as_uuid=True), Sequence("win_results_seq"), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False)
    # game_date_id = Column(Integer, ForeignKey('euro_game_day.id'))
    game_date_id = Column(UUID(as_uuid=True), ForeignKey('euro_game_day.id'))
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


# class euro number and star in array
class EuroStarNumbers(Base):
    __tablename__ = constants.TABLE_NAME_EURO_STAR_NUMBERS
    # id = Column(Integer, Sequence("euro_star_numbers_seq"), primary_key=True, index=True)
    id = Column('id', UUID(as_uuid=True), Sequence("euro_star_numbers_seq"), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False)
    # game_date_id = Column(Integer, ForeignKey('euro_game_day.id'))
    game_date_id = Column(UUID(as_uuid=True), ForeignKey('euro_game_day.id'))
    game_date = relationship("GameDate", back_populates="eurostarnumbers")
    euro_numbers = Column(ARRAY(Integer))  # Column('euro_numbers', ARRAY(Integer))
    star_numbers = Column(ARRAY(Integer))  # Column('star_numbers', ARRAY(Integer))

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
            return EuroStarNumbers.query.filter_by(game_date=date).first().id
        except Exception as e:
            print(e)
            return None


class UnionNumbers(Base):
    __tablename__ = constants.TABLE_UNION_NUMBER
    id = Column('id', UUID(as_uuid=True), Sequence("union_number_seq"), primary_key=True, default=uuid.uuid4,
                unique=True,
                nullable=False)
    game_date_id = Column(UUID(as_uuid=True), ForeignKey('euro_game_day.id'))
    game_date = relationship("GameDate", back_populates="unionnumbers")
    numbers = Column('numbers', SmallInteger, nullable=True)

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


class UnionStars(Base):
    __tablename__ = constants.TABLE_UNION_STAR
    id = Column('id', UUID(as_uuid=True), Sequence("union_star_seq"), primary_key=True, default=uuid.uuid4, unique=True,
                nullable=False)
    game_date_id = Column(UUID(as_uuid=True), ForeignKey('euro_game_day.id'))
    game_date = relationship("GameDate", back_populates="unionstars")
    stars = Column('stars', SmallInteger, nullable=True)

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
