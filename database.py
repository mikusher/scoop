import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
from log_managment import create_logger
logger = create_logger('{}.log'.format(__name__))

load_dotenv(find_dotenv())
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'score.sqlite3')
ENGINE = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

Base = declarative_base()


def create_all():
    logger.info('Creating database')
    Base.metadata.create_all(bind=ENGINE, checkfirst=True)
    logger.info('Database created')
    return


def create_session() -> sessionmaker:
    logger.info('Creating session')
    # engine
    logger.info('Creating engine')
    sqlalchemy_uri = SQLALCHEMY_DATABASE_URI
    logger.info('Creating engine with uri: ' + sqlalchemy_uri)
    engine = ENGINE
    logger.info('Engine created')
    # create a configured "Session" class
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info('Session created')
    # create a Session
    session = Session()
    return session
