import json
import sys

def str2u(input_str):
    if sys.version_info < (3,):
        return unicode(input_str)
    return str(input_str)

def cmd_text(cmd, params={}):
    cdict = {}
    cdict['cmd'] = cmd
    cdict.update(params)
    return json.dumps(cdict)

