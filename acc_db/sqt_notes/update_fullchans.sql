

CREATE OR REPLACE FUNCTION public.update_fullchans_pre1()
  RETURNS TABLE(
    protocol character varying(50),
    chan_name character varying(1024),
    cur_chan_name character varying(1024),
    access character varying(10),
    namesys_id integer,
    dev_id integer,
    chan_id integer,
    is_current boolean,
    systems integer[]
  ) AS
$BODY$
BEGIN
CREATE TEMP TABLE fullchan_temp (
  protocol character varying(50),
  chan_name character varying(1024),
  cur_chan_name character varying(1024),
  access character varying(10),
  namesys_id integer,
  dev_id integer,
  chan_id integer,
  is_current boolean,
  systems integer[]

);
SELECT protocol,name,access,namesys_id,dev_id,chan_id,1,{} into fullchan_temp from mode_chans();

RETURN query select * from fullchan_temp;

END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION public.update_fullchans_pre1()
  OWNER TO postgres;
