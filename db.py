# coding:utf-8
import sqlite3
import datetime


class SqliteDB(object):
    DATABASE = 'db.sqlite'

    def __init__(self):
        self.connection = sqlite3.connect(SqliteDB.DATABASE)

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def query_db(self, query, args=(), one=False):
        cur = self.connection.execute(query, args)
        rv = [dict((cur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

    def ack_file(self, id, res_img):
        sql = """
        update result set res_img = ? 
        where id = ?
        """
        print(res_img, id)
        self.connection.execute(sql, (res_img, id))
        self.connection.commit()

    def insert_file(self, src_img, ref_img, alg):
        self.connection.execute(
            """
        insert into result('src_img', 'ref_img', 'alg', 'add_time', 'res_img') 
        values (?,?,?,?,?)
        """, (src_img, ref_img, alg, datetime.datetime.now(), '')
        )
        cur = self.connection.execute(
            """
            SELECT LAST_INSERT_ROWID()
            """
        )
        r_id = cur.fetchall()[0][0]
        self.connection.commit()
        return r_id

    def del_file(self, id):
        self.connection.execute('delete from result where id = ?', (id,))
        self.connection.commit()


if __name__ == '__main__':
    pass
