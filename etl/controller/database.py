import logging
import os

from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
from tqdm import tqdm

from etl.utils.log_managment import init_logger

init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# get environment boolean variables from .env file PRODUCTION
PRODUCTION = os.getenv('PRODUCTION', 'False').lower() in ('true', '1', 't')
if PRODUCTION:
    DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
    DATABASE_USER = os.getenv("POSTGRES_USER")
    DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_DB_EX = os.getenv("DATABASE_DB_EX")

    EXTERNAL_SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (DATABASE_DIALECT, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_DB_EX)
    # production
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_DEV', EXTERNAL_SQLALCHEMY_DATABASE_URI)
    logger.info('The database uri is: ' + SQLALCHEMY_DATABASE_URI)
    engine = create_engine(url=SQLALCHEMY_DATABASE_URI)
else:
    # development
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'satellite').strip()
    logger.info('The database name is: ' + DATABASE_NAME)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_PROD', 'sqlite:///' + os.path.join(BASE_DIR, '{}.db'.format(DATABASE_NAME)))
    logger.info('The database uri is: ' + SQLALCHEMY_DATABASE_URI)
    engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})


# create a base class for declarative class definitions
Base = declarative_base()


def prepare_database():
    loop = tqdm(total=7, unit='%', position=0, leave=True)
    logger.info('Creating database')
    loop.set_description('Creating database'.format(1))
    loop.update(1)
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        # Connect the database if exists.
        engine.connect()
    logger.info('Database created')
    logger.info('Creating tables')
    loop.set_description('Creating tables'.format(2))
    loop.update(1)
    Base.metadata.create_all(bind=engine, checkfirst=True)
    loop.set_description('Creating tables'.format(3))
    loop.update(1)
    # create a view to see the number of rows in the table
    logger.info('Creating view')

    # get the view folder and the view file
    loop.set_description('Creating view'.format(4))
    loop.update(1)
    dll_folder = os.path.join(BASE_DIR, '../dll')
    view_file = os.path.join(dll_folder, 'views_postgres.sql')
    loop.set_description('Creating view'.format(5))
    loop.update(1)
    # read the view file
    with open(view_file, 'r') as f:
        view_sql = f.read()
    # execute the view
    logger.info('Executing view')
    loop.set_description('Executing view'.format(6))
    loop.update(1)
    with engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(text(view_sql))
        loop.set_description('Executing view'.format(7))
        loop.update(1)
        logger.info('View created')
        conn.close()
    logger.info('Database created')
    loop.set_description('Database created')
    loop.update(1)
    loop.close()
    return


def create_session() -> sessionmaker:
    logger.info('Creating session')
    # engine
    logger.info('Creating engine')
    sqlalchemy_uri = SQLALCHEMY_DATABASE_URI
    logger.info('Creating engine with uri: ' + sqlalchemy_uri)
    logger.info('Engine created')
    # create a configured "Session" class
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info('Session created')
    # create a Session
    session = Session()
    return session
