﻿SELECT chan.protocol,namesys.name,chan.devpref,dev.name,chan.name,chan.access,chan.dtype,chan.dsize
from namesys,dev,dev_devtype,devtype_chans,chan,devtype
WHERE namesys.id=dev.namesys_id and
dev.id=dev_devtype.dev_id and
dev_devtype.devtype_id=devtype.id and dev_devtype.devtype_id=devtype_chans.devtype_id and 
devtype_chans.chan_id=chan.id
order by namesys.id,dev.id,chan.id 