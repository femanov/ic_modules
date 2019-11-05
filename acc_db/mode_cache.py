from acc_db.db import ModesDB

# this creates a cache of sys to cnames on init
# than can be used to select names
class SysCache:
    def __init__(self, **kwargs):
        self.db = kwargs.get('db', ModesDB())

        self.a_kinds = self.db.access_kinds()
        self.db.execute("select array_agg(sys order by sys) from "
                        "(select distinct unnest(systems) from fullchan where is_current) as t(sys)")
        self.sys = self.db.cur.fetchall()[0][0]

        self.cache = {ak: {s: self.get_namelist(s, ak) for s in self.sys} for ak in self.a_kinds}

    def get_namelist(self, sys, a_kind):
        self.db.execute("select array_agg(id) from fullchan where is_current"
                        " AND access=%s and %s=ANY(systems)", (a_kind, sys))
        return self.db.cur.fetchall()[0][0]

    def cids(self, syslist, a_kinds):
        ret = set()
        for ak in a_kinds:
            for s in syslist:
                try:
                    ret = ret.union(self.cache[ak][s])
                except KeyError:
                    #print("key not found:", ak, s)
                    pass
                except TypeError:
                    #print("type err", ak, s)
                    #print(self.cache[ak][s])
                    pass
        return ret


class ModeCache:
    def __init__(self, mark, **kwargs):
        self.db = kwargs.get('db', ModesDB())
        self.sys_cache = kwargs.get('sys_cache', SysCache(db=self.db))
        self.name = mark
        self.data = self.db.load_mode_bymark(mark, self.sys_cache.sys, self.sys_cache.a_kinds)

    def extract(self, syslist, a_kinds):
        id_list = self.sys_cache.cids(syslist, a_kinds)
        return {key: self.data[key] for key in id_list if key in self.data}

