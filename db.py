#coding:utf-8
from flask import g
import sqlite3
DATABASE = 'file.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def insert_file(id,src_img,ref_img,out_img,alg):
    g.db.execute('insert into file (?,?,?,?,?)',(
        id,src_img,ref_img,out_img,alg
    ))
    g.db.commit()
