import logging
import os
import contextlib

from typing import Any

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from tqdm import tqdm

from src.utils.log_managment import init_logger

init_logger('{}.log'.format(__name__), __name__)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

# get environment boolean variables from .env file PRODUCTION
PRODUCTION = os.getenv('PRODUCTION', 'False').lower() in ('true', '1', 't')
ETL_DATABASE_DIALECT = os.getenv("ETL_DATABASE_DIALECT")
ETL_DATABASE_USER = os.getenv("ETL_DATABASE_USER")
ETL_DATABASE_PASSWORD = os.getenv("ETL_DATABASE_PASSWORD")
ETL_DATABASE_HOST = os.getenv("ETL_DATABASE_HOST")
ETL_DATABASE_PORT = os.getenv("ETL_DATABASE_PORT")
ETL_DATABASE_DB_EX = os.getenv("ETL_DATABASE_DB_EX", "externals")


@contextlib.contextmanager
def get_session(cleanup=False):
    session = Session(bind=engine)
    Base.metadata.create_all(engine)

    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()

    if cleanup:
        Base.metadata.drop_all(engine)


@contextlib.contextmanager
def get_conn(cleanup=False):
    conn = engine.connect()
    Base.metadata.create_all(engine)

    yield conn
    conn.close()

    if cleanup:
        Base.metadata.drop_all(engine)


def production_engine(dialect, user, password, host, port, db) -> Any:
    # create a database engine for etl database
    EXTERNAL_SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (dialect, user, password, host, port, db)
    # production
    _db_uri = os.getenv('SQLALCHEMY_DATABASE_URI_DEV', EXTERNAL_SQLALCHEMY_DATABASE_URI)
    _engine = create_engine(url=_db_uri)
    logger.info('The database uri is: ' + _db_uri)
    return _db_uri, _engine


def development_engine(basedir) -> Any:
    # development
    DATABASE_NAME = os.getenv('DATABASE_DB_EX', 'externals').strip()
    logger.info('The database name is: ' + DATABASE_NAME)
    _db_uri = os.getenv('SQLALCHEMY_DATABASE_URI_PROD',
                        'sqlite:///' + os.path.join(basedir, '{}.db'.format(DATABASE_NAME)))
    _engine = create_engine(_db_uri, connect_args={"check_same_thread": False})
    logger.info('The database uri is: ' + _db_uri)
    return _db_uri, _engine


if PRODUCTION:
    db_uri, engine = production_engine(ETL_DATABASE_DIALECT, ETL_DATABASE_USER, ETL_DATABASE_PASSWORD,
                                       ETL_DATABASE_HOST, ETL_DATABASE_PORT, ETL_DATABASE_DB_EX)
else:
    db_uri, engine = development_engine(BASE_DIR)

# create a base class for declarative class definitions
Base = declarative_base()


def create_superset_database():
    logger.info('Creating superset database')
    SUPERSET_DB_NAME = os.getenv("SUPERSET_DB_NAME", "superset")
    # create a database engine for superset database
    superset_sqlalchemy_uri = "%s://%s:%s@%s:%s/%s" % (
        ETL_DATABASE_DIALECT, ETL_DATABASE_USER, ETL_DATABASE_PASSWORD, ETL_DATABASE_HOST, ETL_DATABASE_PORT,
        SUPERSET_DB_NAME)
    logger.info('The superset database uri is: ' + superset_sqlalchemy_uri)
    superset_engine = create_engine(superset_sqlalchemy_uri)
    if not database_exists(superset_engine.url):
        logger.info('Superset Database does not exist')
        create_database(superset_engine.url)
        logger.info('Superset Database created')


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
    dll_folder = os.path.join(BASE_DIR, 'dll')

    view_files = []
    for dir_path, dir_names, filenames in os.walk(dll_folder):
        for filename in filenames:
            if filename.endswith('.sql'):
                view_files.append(os.path.join(dir_path, filename))

    for view_file in view_files:
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
    # sqlalchemy_uri = SQLALCHEMY_DATABASE_URI
    # logger.info('Creating engine with uri: ' + sqlalchemy_uri)
    logger.info('Engine created')
    # create a configured "Session" class
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info('Session created')
    # create a Session
    session = Session()
    return session


def refresh_materialized_views():
    refresh_folder = os.path.join(BASE_DIR, 'dll', 'refresh')
    ref = os.path.join(refresh_folder, 'mat.sql')
    with open(ref, 'r') as f:
        ref_file = f.read()

    with engine.connect().execution_options(autocommit=True) as conn:
        conn.execute(text(ref_file))
        conn.close()
        logger.info('Materialized view as ended, successful.')
