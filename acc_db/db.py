import psycopg2
import sys
from io import BytesIO

from settings.db import *

import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

class acc_db:
    def __init__(self):
        self.conn, self.cur = None, None
        self.db_connect()

    def __del__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def db_connect(self):
        try:
            self.conn = psycopg2.connect(None, dbname=DB, user=DBUSER, password=DBPASSWORD, host=DBHOST)
        except psycopr2.Error as e:
            print("unable to connect to DB")
            print("error code: ", e.pgcode)
            print("error str: ", e.pgerror)
            sys.exit(1) # what the fuck?
        self.cur = self.conn.cursor()

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

    def update_fullchans(self):
        pass

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

    def mode_list(self, limit=100, offset=0, like=None, load_archived=False):
        if like is None:
            if load_archived:
                self.execute("SELECT id,author,comment,stime FROM mode ORDER BY stime DESC LIMIT %s OFFSET %s",(limit, offset))
            else:
                self.execute("SELECT id,author,comment,stime FROM mode WHERE archived=0 ORDER BY stime DESC LIMIT %s OFFSET %s",(limit, offset))
        else:
            if load_archived:
                self.execute("SELECT id,author,comment,stime FROM mode"
                             " WHERE author ILIKE %s or comment ILIKE %s ORDER BY stime DESC LIMIT %s OFFSET %s",
                             (like, like, limit, offset))
            else:
                self.execute("SELECT id,author,comment,stime FROM mode"
                             " WHERE archived=0 and (author ILIKE %s or comment ILIKE %s) ORDER BY stime DESC LIMIT %s OFFSET %s",
                             (like, like, limit, offset))

        self.conn.commit()
        return self.cur.fetchall()

    def archive_mode(self, mode_id):
        self.execute('UPDATE mode SET archived=1 WHERE id=%s', (mode_id,))
        self.conn.commit()

    def sys_list_chans(self, syslist):
        pass

    def save_mode(self, author, comment, data):
        self.execute("INSERT INTO mode(author,comment,stime,archived) values(%s,%s,now(),0) RETURNING id",
                     (author, comment,))
        self.conn.commit()
        mode_id = self.cur.fetchone()[0]

        f_data = BytesIO()
        for row in data:
            f_data.write(('\t'.join([str(mode_id)] + [str(x) for x in row[2:]]) + '\n').encode())

        # this is for binary write
        # f_data.write(pack('!11sii', b'PGCOPY\n\377\r\n\0', 0, 0))
        # for row in data:
        #     f_data.write(pack('!h', 5))
        #     f_data.write(pack('!ii', 4, mode_id))
        #     f_data.write(pack('!ii', 4, row[2]))
        #     f_data.write(pack('!iq', 8, row[3]))
        #     f_data.write(pack('!id', 8, row[4]))
        #     f_data.write(pack('!ii', 4, row[5]))

        # fullchan_id, utime, value, available
        # File trailer
        # f_data.write(pack('!h', -1))

        io_size = f_data.tell()
        f_data.seek(0)
        cols = ['mode_id', 'fullchan_id', 'utime', 'value', 'available']
        # !! warning, no reconnection for this proc implemented
        # request to db, but connection should work from previous reques in this function
        self.cur.copy_from(f_data, 'modedata', size=io_size, columns=cols)
        #self.cur.copy_expert("COPY modedata(mode_id,fullchan_id,utime,value,available) FROM STDIN WITH BINARY", f_data)

        f_data.close()
        self.conn.commit()
        return mode_id

    # list of load types can be obtained with request: select distinct access from chan
    # r - read channels, like ADC results
    # rw - read/write, like DAC setting
    # settings - channels considered as software tunings
    # state - device state. 1 - if device considered as operated, 0 in other case

    def load_mode(self, mode_id, sysid_list, load_types=['rw']):
        self.execute("SELECT * FROM load_mode_names(%s, %s, %s) ", (mode_id, sysid_list, load_types))
        self.conn.commit()
        return self.cur.fetchall()

    def load_mode_bymark(self, mark_id, sysid_list, load_type=['rw']):
        self.execute("select * FROM load_mode_bymark_n(%s, %s, %s)", (mark_id, sysid_list, load_type))
        self.conn.commit()
        return self.cur.fetchall()

    def mark_mode(self, mode_id, name, comment, author, mark_id=0):
        self.execute("SELECT mark_mode(%s, %s, %s, %s, %s)",
                     (mode_id, name, comment, author, mark_id))
        self.conn.commit()

    def modebymark(self, modemark_id):
        self.execute('SELECT modebymark(%s)', (modemark_id,))
        self.conn.commit()
        return self.cur.fetchone()[0]
