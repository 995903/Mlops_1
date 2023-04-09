from db_connection import db_connect


def execute_query(query, fetch):
    """Get data from db by passing the query"""
    db = db_connect()
    conn = db["conn"]
    cur = db["cur"]
    cur.execute(query)
    res = []
    if fetch == 'one':
        res = cur.fetchone()
    elif fetch == 'all':
        res = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return res


def create_query(query):
    db = db_connect()
    conn = db["conn"]
    cur = db["cur"]
    try:
        cur.execute(query)
        cur.close()
        conn.commit()
        conn.close()
        return "created"
    except Exception as error:
        return str(error)


def insert_query(query):
    db = db_connect()
    conn = db["conn"]
    cur = db["cur"]
    cur.execute(query)
    cur.close()
    conn.commit()
    conn.close()


def update_query(query):
    db = db_connect()
    conn = db["conn"]
    cur = db["cur"]
    cur.execute(query)
    cur.close()
    conn.commit()
    conn.close()