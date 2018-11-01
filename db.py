#coding:utf-8
from flask import g
import sqlite3
DATABASE = 'db.sqlite'

def connect_db():
    return sqlite3.connect(DATABASE)

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def insert_file(id,src_img,ref_img,res_img,alg):
    g.db.execute('insert into result values (?,?,?,?,?)',(
        id,src_img,ref_img,res_img,alg
    ))
    g.db.commit()
def del_file(id):
    g.db.execute('delete from result where id = ?',(id,))
    g.db.commit()
    