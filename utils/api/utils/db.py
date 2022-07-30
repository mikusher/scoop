import os
import psycopg2
import psycopg2.extras
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self):
        self.conn = None
        try:
            if hasattr(self, 'conn') and self.conn is not None:
                self.close()

            self.conn = psycopg2.connect(
                database=os.getenv("DATABASE_DB_EX"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("DATABASE_HOST"),
                port=os.getenv("DATABASE_PORT")
            )
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except psycopg2.Error as error:
            print("Oops! An exception has occurred:", error)

    def getCursor(self):
        return self.cur

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
