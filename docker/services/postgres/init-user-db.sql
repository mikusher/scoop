-- create a user and a database for the superset app
CREATE USER superset WITH PASSWORD 'superset';
CREATE DATABASE superset WITH OWNER superset;
GRANT ALL PRIVILEGES ON DATABASE superset TO superset;
