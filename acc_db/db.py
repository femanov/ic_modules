import psycopg2
from io import BytesIO

from settings.db import *

import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)



# since we use django for some tasks - will try to use djungo ORM
# kwargs mast be: dbname=DB, user=DBUSER,
# more kwargs: password=DBPASSWORD, host=DBHOST <-- from

class DBWrapper:
    def __init__(self, **kwargs):
        self.db_kwargs, self.conn, self.cur, self.connected = kwargs, None, None, False
        if 'dbname' not in kwargs or 'user' not in kwargs:
            print('Warning: no DB and user specified --> no connetion init')
            return
        self.db_connect()

    def __del__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def db_connect(self):
        try:
            self.conn = psycopg2.connect(None, **self.db_kwargs)
        except psycopg2.Error as e:
            print("unable to connect to DB")
            print("error code: ", e.pgcode)
            print("error str: ", e.pgerror)
            self.connected = False
        self.connected = True
        self.cur = self.conn.cursor()
        self.conn.autocommit = True

    # need to rewrite reconnection code.
    def execute(self, request, params=None):
        if params is None:
            try:
                self.cur.execute(request)
            except psycopg2.OperationalError:
                self.db_connect()
                self.cur.execute(request)
        else:
            try:
                self.cur.execute(request, params)
            except psycopg2.OperationalError:
                self.db_connect()
                self.cur.execute(request, params)


class AccConfig(DBWrapper):

    def fchans(self):
        self.execute("SELECT * FROM fchans()")
        data = self.cur.fetchall()
        self.conn.commit()
        chanlist = [[y for y in x] for x in data]
        return chanlist

    # before use of database fullchan table need to be updated
    def mode_chans(self):
        self.execute("SELECT protocol,chan_name,id FROM fullchan WHERE is_current=1")
        data = self.cur.fetchall()
        self.conn.commit()
        chanlist = [[y for y in x] for x in data]
        return chanlist


    def sys_list(self):
        self.execute("SELECT id,label FROM sys order by id")
        self.conn.commit()
        return self.cur.fetchall()


    def sys_list_chans(self, syslist):
        pass


