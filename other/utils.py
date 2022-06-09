import json
import psycopg2


def db(database_name='pepe'):
    return psycopg2.connect(database=database_name)


def query_db(query, args=(), one=False):
    cur = db().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r


my_query = query_db("select * from majorroadstiger limit %s", (3,))
json_output = json.dumps(my_query)
