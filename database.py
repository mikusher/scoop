import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv

from log_managment import _init_logger

_init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

DATABASE_NAME = os.getenv('DATABASE_NAME', 'score.sqlite3')
logger.info('The database name is: ' + DATABASE_NAME)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE_NAME)
ENGINE = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

Base = declarative_base()


def prepare_database():
    logger.info('Creating database')
    Base.metadata.create_all(bind=ENGINE, checkfirst=True)
    # create a view to see the number of rows in the table
    logger.info('Creating view')
    # get the view file
    dll_folder = os.path.join(BASE_DIR, 'dll')
    view_file = os.path.join(dll_folder, 'views.sql')
    # read the view file
    with open(view_file, 'r') as f:
        view_sql = f.read()
    # execute the view
    logger.info('Executing view')
    ENGINE.execute(view_sql)
    logger.info('View created')
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
