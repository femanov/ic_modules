
import psycopg2
import time
import psycopg2.extensions
from settings.db import acc_cfg, mode_db_cfg


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

    def loadable_access_kinds(self):
        self.execute("SELECT ARRAY(SELECT access FROM caccess_type WHERE savable and load_implemented)")
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
        self.execute("SELECT protocol, cur_chan_name, id from fullchan WHERE is_current ORDER BY dev_id,chan_id")
        return self.cur.fetchall()

    def mode_list(self, limit=100, offset=0, like=None, load_archived=False):
        if like is None or like == '':
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

    def save_mode(self, author, comment, data_json):
        self.execute("INSERT INTO mode(author,comment,stime,archived,info,data)"
                     " values(%s,%s,now(),false,%s,%s)  RETURNING id", (author, comment, "{\"saver\":1}", data_json))
        mode_id = self.cur.fetchone()[0]
        return mode_id

    def load_mode(self, mode_id, sysid_list, load_types=['rw']):
        self.execute("SELECT * FROM load_mode(%s, %s, %s) ", (mode_id, sysid_list, load_types))
        # since json standart do not have numerical keys in dict
        # load_mode database function returns list of
        db_data = self.cur.fetchall()[0][0]
        data = {int(k): db_data[k] for k in db_data}
        return data

    def load_mode_bymark(self, mark_name, sysid_list, load_type=['rw']):
        self.execute("select * FROM load_mode_bymark(%s, %s, %s)", (mark_name, sysid_list, load_type))
        db_data = self.cur.fetchall()[0][0]
        data = {int(k): db_data[k] for k in db_data}
        return data

    def mark_mode(self, mode_id, name, comment, author):
        self.execute("SELECT mark_mode(%s, %s, %s, %s)", (mode_id, name, comment, author))

    def get_marks(self):
        self.execute("SELECT name from modemark ORDER BY id")
        return [x[0] for x in self.cur.fetchall()]

    def update_mode(self, id, **kwargs):
        ks = kwargs.keys()
        req = "update mode set " + "=%s,".join(ks) + '=%s where id=%s'
        self.execute(req, [kwargs[k] for k in ks] + [id])

    def access_kinds(self):
        self.execute('select array_agg(distinct access) from fullchan')
        return self.cur.fetchall()[0][0]

