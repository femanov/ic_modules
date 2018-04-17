CREATE OR REPLACE FUNCTION load_mode(in_mode_id integer, sys_ids integer[], build_names integer, load_type integer)
  RETURNS TABLE(protocol varchar, chan_name text, value double precision) AS
$BODY$
DECLARE
    alist character varying[];
BEGIN
    alist := ARRAY ['rw', 's', 'c', 'r'];
IF build_names = 0 THEN
    RETURN QUERY SELECT DISTINCT chan.protocol, text(modedata.chan_name), modedata.value
    FROM chan,modedata,sys_devs,dev
    WHERE modedata.mode_id = in_mode_id and chan.id = modedata.chan_id and modedata.dev_id=dev.id
    and dev.enabled = 1
    and modedata.dev_id = sys_devs.dev_id and sys_devs.sys_id = ANY(sys_ids)
    and chan.access = ANY(alist[1:load_type]);
ELSE
    RETURN QUERY SELECT DISTINCT chan.protocol, namesys.name || '.' || dev.name || '.' || chan.name, modedata.value
    FROM chan, dev, namesys, modedata, sys_devs
    WHERE modedata.mode_id = in_mode_id
    and chan.id = modedata.chan_id and dev.id = modedata.dev_id and namesys.id = modedata.namesys_id
    and dev.enabled = 1
    and modedata.dev_id = sys_devs.dev_id and sys_devs.sys_id = ANY(sys_ids)
    and chan.access = ANY(alist[1:load_type]);
END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION load_mode(in_mode_id integer, sys_ids integer[], build_names integer, load_type integer)
  OWNER TO postgres;
