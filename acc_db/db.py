import psycopg2
import time
from io import BytesIO

import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

from settings.db import acc_cfg, mode_db_cfg

# since we use django for some tasks - will try to use djungo ORM
# kwargs mast be: dbname=DB, user=DBUSER,
# more kwargs: password=DBPASSWORD, host=DBHOST <-- from

class DBWrapper:
    def __init__(self, **kwargs):
        self.db_kwargs, self.conn, self.cur, self.connected = kwargs, None, None, False
        if 'dbname' not in kwargs or 'user' not in kwargs:
            print('Warning: no DB and user specified --> no connection init')
            return
        self.connected = False
        self.db_connect()

    def __del__(self):
        if self.connected:
            self.cur.close()
            self.conn.close()

    def db_connect(self):
        while True:
            try:
                self.conn = psycopg2.connect(None, **self.db_kwargs)
                self.connected = True
                self.cur = self.conn.cursor()
                self.conn.autocommit = True
                break
            except psycopg2.Error as e:
                print("unable to connect to DB, errcode:", e.pgcode, e.pgerror)
                print(self.db_kwargs)
                self.connected = False
                time.sleep(1)
                continue

    # need to rewrite reconnection code.
    def execute(self, request, params=None):
        if not self.connected:
            self.db_connect()
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
    def __init__(self, **kwargs):
        if 'dbname' not in kwargs or 'user' not in kwargs:
            kwargs.update(acc_cfg)
        super(AccConfig, self).__init__(**kwargs)


    def fchans(self):
        self.execute("SELECT * FROM fchans()")
        data = self.cur.fetchall()
        chanlist = [[y for y in x] for x in data]
        return chanlist

    # before use of database fullchan table need to be updated
    def mode_chans(self):
        self.execute("SELECT protocol,chan_name,id FROM fullchan WHERE is_current=1")
        data = self.cur.fetchall()
        chanlist = [[y for y in x] for x in data]
        return chanlist

    def sys_list(self):
        self.execute("SELECT id,label FROM sys order by id")
        return self.cur.fetchall()

    def sys_list_chans(self, syslist):
        pass

    def savable_access_kinds(self):
        self.execute("SELECT ARRAY(SELECT access FROM caccess_type WHERE savable)")
        return self.cur.fetchall()[0][0]

    def sys_descendants(self, sys_name, **kwargs):
        return_empty = kwargs.get('return_empty', True)
        #sys_name = kwargs.get('sys_name', False)

        if not sys_name:
            return []

        if return_empty:
            self.execute('SELECT id from sys where path like'
                         ' (select (path || %s) from sys where name=%s)', ('%', sys_name))
        else:
            self.execute('select id from sys where path like'
                         ' (select(path || %s) from sys where name=%s and'
                         ' exists(select id from sys_devs where sys_id = sys.id)', ('%', sys_name))

        return [x[0] for x in self.cur.fetchall()]


class ModesDB(DBWrapper):
    def __init__(self, **kwargs):
        if 'dbname' not in kwargs or 'user' not in kwargs:
            kwargs.update(mode_db_cfg)
        super(ModesDB, self).__init__(**kwargs)


    def mode_chans(self):
        self.execute("SELECT protocol, cur_chan_name, id from fullchan WHERE is_current ORDER BY namesys_id,dev_id,chan_id")
        return self.cur.fetchall()

    def mode_list(self, limit=100, offset=0, like=None, load_archived=False):
        if like is None:
            if load_archived:
                self.execute("SELECT id,author,comment,stime,mode_type(id) FROM mode ORDER BY stime DESC LIMIT %s OFFSET %s",(limit, offset))
            else:
                self.execute("SELECT id,author,comment,stime,mode_type(id) FROM mode WHERE archived=false ORDER BY stime DESC LIMIT %s OFFSET %s",(limit, offset))
        else:
            if load_archived:
                self.execute("SELECT id,author,comment,stime,mode_type(id) FROM mode"
                             " WHERE author ILIKE %s or comment ILIKE %s ORDER BY stime DESC LIMIT %s OFFSET %s",
                             (like, like, limit, offset))
            else:
                self.execute("SELECT id,author,comment,stime,mode_type(id) FROM mode"
                             " WHERE archived=false and (author ILIKE %s or comment ILIKE %s) ORDER BY stime DESC LIMIT %s OFFSET %s",
                             (like, like, limit, offset))
        return self.cur.fetchall()

    def marked_modes(self, mark_ids):
        self.execute("SELECT mode.id,mode.author,mode.comment,mode.stime,mode_type(mode.id),modemark.name FROM mode"
                    " LEFT JOIN modemark on mode.id = modemark.mode_id"
                    " WHERE modemark.id = ANY(%s) ORDER BY mode.stime DESC", (mark_ids,))
        return self.cur.fetchall()


    def archive_mode(self, mode_id):
        self.execute('UPDATE mode SET archived=true WHERE id=%s', (mode_id,))

    def mark_mode_old(self, mode_id, name, comment, author, mark_id=0):
        self.execute("SELECT mark_mode(%s, %s, %s, %s, %s)", (mode_id, name, comment, author, mark_id))

    def save_mode(self, author, comment, data):
        self.execute("INSERT INTO mode(author,comment,stime,info,archived) values(%s,%s,now(),jsonb_build_object(),false) RETURNING id",
                     (author, comment))
        mode_id = self.cur.fetchone()[0]

        f_data = BytesIO()
        for row in data:
            f_data.write(('\t'.join([str(mode_id)] + [str(x) for x in row[2:]]) + '\n').encode())

        io_size = f_data.tell()
        f_data.seek(0)
        cols = ['mode_id', 'fullchan_id', 'utime', 'value', 'available']
        # !! warning, no reconnection for this proc implemented
        # request to db, but connection should work from previous requests in this function
        self.cur.copy_from(f_data, 'modedata', size=io_size, columns=cols)

        f_data.close()
        return mode_id

    def load_mode(self, mode_id, sysid_list, load_types=['rw']):
        self.execute("SELECT * FROM load_mode(%s, %s, %s) ", (mode_id, sysid_list, load_types))
        return self.cur.fetchall()

    def load_mode_bymark_old(self, mark_id, sysid_list, load_type=['rw']):
        self.execute("select * FROM load_mode_bymark(%s, %s, %s)", (mark_id, sysid_list, load_type))
        return self.cur.fetchall()

    def load_mode_bymark(self, mark_name, sysid_list, load_type=['rw']):
        print("loading mode by mark: ", mark_name, sysid_list, load_type)
        self.execute("select * FROM load_mode_bymarkt(%s, %s, %s)", (mark_name, sysid_list, load_type))
        return self.cur.fetchall()

    def mark_mode(self, mode_id, name, comment, author):
        self.execute("SELECT mark_modet(%s, %s, %s, %s)", (mode_id, name, comment, author))

    def get_marks(self):
        self.execute("SELECT name from modemark ORDER BY id")
        return [x[0] for x in self.cur.fetchall()]

