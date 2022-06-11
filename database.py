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

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# get environment boolean variables from .env file PRODUCTION

PRODUCTION = os.getenv('PRODUCTION', 'False').lower() in ('true', '1', 't')
if PRODUCTION:
    DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_DB_EX = os.getenv("DATABASE_DB_EX")

    EXTERNAL_SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
        DATABASE_DIALECT,
        DATABASE_USER,
        DATABASE_PASSWORD,
        DATABASE_HOST,
        DATABASE_PORT,
        DATABASE_DB_EX,
    )
    # production
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_DEV',  EXTERNAL_SQLALCHEMY_DATABASE_URI)
    logger.info('The database uri is: ' + SQLALCHEMY_DATABASE_URI)
    ENGINE = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
else:
    # development
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'satellite').strip()
    logger.info('The database name is: ' + DATABASE_NAME)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_PROD', 'sqlite:///' + os.path.join(BASE_DIR, '{}.db'.format(DATABASE_NAME)))
    logger.info('The database uri is: ' + SQLALCHEMY_DATABASE_URI)
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
