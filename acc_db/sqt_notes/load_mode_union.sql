SELECT modedata.protocol,modedata.chan_name,modedata.namesys_id, modedata.dev_id,
modedata.chan_id,modedata.value,modedata.available FROM modedata,chan,sys_devs
WHERE chan.id=modedata.chan_id and modedata.dev_id=sys_devs.dev_id
and chan.access='rw' and modedata.available=1 and mode_id=72 and sys_devs.sys_id=1
UNION
SELECT modedata.protocol,modedata.chan_name,modedata.namesys_id, modedata.dev_id,
modedata.chan_id,modedata.value,modedata.available FROM modedata,chan,sys_devs
WHERE chan.id=modedata.chan_id and modedata.dev_id=sys_devs.dev_id
and chan.access='rw' and modedata.available=1 and mode_id=72 and sys_devs.sys_id=2
