
from io import BytesIO

from .db import DBWrapper


class ModesDB(DBWrapper):
    def mode_chans(self):
        self.execute("SELECT protocol, cur_chan_name, id from fullchan WHERE is_current")
        return self.cur.fetchall()

    def mode_list(self, limit=100, offset=0, like=None, load_archived=False):
        if like is None:
            if load_archived:
                self.execute("SELECT id,author,comment,stime FROM mode ORDER BY stime DESC LIMIT %s OFFSET %s",(limit, offset))
            else:
                self.execute("SELECT id,author,comment,stime FROM mode WHERE archived=false ORDER BY stime DESC LIMIT %s OFFSET %s",(limit, offset))
        else:
            if load_archived:
                self.execute("SELECT id,author,comment,stime FROM mode"
                             " WHERE author ILIKE %s or comment ILIKE %s ORDER BY stime DESC LIMIT %s OFFSET %s",
                             (like, like, limit, offset))
            else:
                self.execute("SELECT id,author,comment,stime FROM mode"
                             " WHERE archived=false and (author ILIKE %s or comment ILIKE %s) ORDER BY stime DESC LIMIT %s OFFSET %s",
                             (like, like, limit, offset))
        return self.cur.fetchall()

    def marked_modes(self, mark_ids):
        self.execute("SELECT mode.id,mode.author,mode.comment,mode.stime,modemark.name FROM mode"
                    " LEFT JOIN modemark on mode.id = modemark.mode_id"
                    " WHERE modemark.id = ANY(%s) ORDER BY mode.stime DESC", (mark_ids,))
        return self.cur.fetchall()


    def archive_mode(self, mode_id):
        self.execute('UPDATE mode SET archived=true WHERE id=%s', (mode_id,))

    def mark_mode(self, mode_id, name, comment, author, mark_id=0):
        self.execute("SELECT mark_mode(%s, %s, %s, %s, %s)", (mode_id, name, comment, author, mark_id))

    def save_mode(self, author, comment, data):
        self.execute("INSERT INTO mode(author,comment,stime,archived) values(%s,%s,now(),false) RETURNING id",
                     (author, comment,))
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

    # list of load types can be obtained with request: select distinct access from chan
    # r - read channels, like ADC results
    # rw - read/write, like DAC setting
    # settings - channels considered as software tunings
    # state - device state. 1 - if device considered as operated, 0 in other case

    def load_mode(self, mode_id, sysid_list, load_types=['rw']):
        self.execute("SELECT * FROM load_mode(%s, %s, %s) ", (mode_id, sysid_list, load_types))
        return self.cur.fetchall()

    def load_mode_bymark(self, mark_id, sysid_list, load_type=['rw']):
        self.execute("select * FROM load_mode_bymark(%s, %s, %s)", (mark_id, sysid_list, load_type))
        return self.cur.fetchall()
