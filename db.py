# coding:utf-8
from flask import g
import sqlite3
import datetime

DATABASE = 'db.sqlite'


def connect_db():
    return sqlite3.connect(DATABASE)


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def insert_file(src_img, ref_img, alg):
    g.db.execute(
        """
    insert into result('src_img', 'ref_img', 'alg', 'add_time') values (?,?,?,?)
    """, (src_img, ref_img, alg, datetime.datetime.now())
    )
    cur = g.db.execute(
        """
        SELECT LAST_INSERT_ROWID()
        """
    )
    r_id = cur.fetchall()[0][0]
    g.db.commit()
    return r_id


def del_file(id):
    g.db.execute('delete from result where id = ?', (id,))
    g.db.commit()


def init():
    with open('schema.sql') as f:
        conn = connect_db()
        conn.executescript(f.read())
        conn.commit()


if __name__ == '__main__':
    db = connect_db()
    db.execute("""
    insert into result('src_img', 'ref_img', 'res_img', 'alg', 'add_time') values (?,?,?,?,?)
    """, (
        'src_img', 'ref_img', 'res_img', 'alg', datetime.datetime.now()
    ))
    cur = db.execute(
        """
                SELECT LAST_INSERT_ROWID()
        """
    )
    print(cur.fetchall()[0][0])
    db.commit()
