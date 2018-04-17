SELECT modedata.protocol,modedata.chan_name,modedata.namesys_id,modedata.dev_id,modedata.chan_id,modedata.value,modedata.available
from namesys,dev,dev_devtype,devtype_chans,chan,devtype,sys_devs,modedata
WHERE namesys.id=dev.namesys_id and dev.id=dev_devtype.dev_id and
dev_devtype.devtype_id=devtype.id and dev_devtype.devtype_id=devtype_chans.devtype_id and 
devtype_chans.chan_id=chan.id and dev.id=modedata.dev_id and namesys.id=modedata.namesys_id and chan.id=modedata.chan_id
and dev.id=sys_devs.dev_id and sys_devs.sys_id=1 and modedata.mode_id=72