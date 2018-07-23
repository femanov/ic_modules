-- Function: public.mode_chans()

-- DROP FUNCTION public.mode_chans();

CREATE OR REPLACE FUNCTION public.mode_chans()
  RETURNS TABLE(protocol varchar, name varchar, access varchar, namesys_id integer,
    dev_id integer, chan_id integer, systems integer[]) AS
$BODY$
DECLARE
def_soft_namesys_id integer;
def_soft_namesys_name varchar;
BEGIN
SELECT id,namesys.name INTO def_soft_namesys_id, def_soft_namesys_name FROM namesys WHERE def_soft;
RETURN QUERY
SELECT chan.protocol, CAST(namesys.name || '.' || dev.name || '.' || chan.name AS varchar), chan.access,
namesys.id, dev.id, chan.id, array_agg(sys_devs.sys_id)
from namesys,dev,dev_devtype,devtype,devtype_chans,chan,sys_devs
WHERE namesys.id=dev.namesys_id and dev.id=dev_devtype.dev_id and dev_devtype.devtype_id=devtype.id and
devtype_chans.devtype_id=devtype.id and devtype_chans.chan_id=chan.id and dev.enabled and chan.savable and chan.dsize=1
and (not devtype.soft or ( devtype.soft and namesys.soft))
and dev.id=sys_devs.dev_id GROUP BY dev.id
UNION
SELECT chan.protocol, CAST(def_soft_namesys_name || '.' || dev.name || '.' || chan.name AS varchar), chan.access,
def_soft_namesys_id, dev.id, chan.id, array_agg(sys_devs.sys_id)
from namesys,dev,dev_devtype,devtype,devtype_chans,chan,sys_devs
WHERE namesys.id=dev.namesys_id and dev.id=dev_devtype.dev_id and dev_devtype.devtype_id=devtype.id and
devtype_chans.devtype_id=devtype.id and devtype_chans.chan_id=chan.id and
dev.enabled and devtype.soft and not namesys.soft and chan.dsize=1 and chan.savable
and dev.id=sys_devs.dev_id GROUP BY dev.id;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION public.mode_chans()
  OWNER TO postgres;
