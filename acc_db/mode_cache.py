from acc_db.db import *


# this creates a cache of sys to cnames on init
# than can be used to select names
class SysCache:
    def __init__(self, database=None):
        self.db = database
        if self.db is None:
            self.db = acc_db()

        self.cache = {}
        self.db.execute("SELECT id from sys")
        res = self.db.cur.fetchall()
        self.sys = [x[0] for x in res]
        for x in self.sys:
            self.db.execute("select chan_name from fullchan,chan where is_current=1 and chan.id=fullchan.chan_id AND chan.access=\'rw\' and "
                            "dev_id=any(select sys_devs.dev_id from sys_devs where sys_id=%s)", (x,))
            self.cache[x] = [y[0] for y in self.db.cur.fetchall()]

    def cnames(self, syslist):
        ret = set()
        for x in syslist:
            ret = ret.union(self.cache[x])
        return ret


class ModeCache:
    def __init__(self, mark_id, database=None, sys_cache=None, name=None):
        self.db = database
        self.name = name
        if self.db is None:
            self.db = acc_db()

        self.sys_cache = sys_cache
        if self.sys_cache is None:
            self.sys_cache = SysCache(self.db)

        # loading mode for ["rw"] type of channels
        self.mode_data = self.db.load_mode_bymark(mark_id, self.sys_cache.sys)
        # modedata: protocol, chan_name, value

        # create a
        self.data = {x[1]: x for x in self.mode_data}


    def extract(self, syslist):
        namelist = self.sys_cache.cnames(syslist)
        try:
            # the faster call
            res = [self.data[key] for key in namelist]
        except:
            # works in case of key errors in try
            res = []
            for key in namelist:
                if key in self.data:
                    res.append(self.data[key])
                else:
                    print(key)
        return res
