select (array_agg(provone) || array_agg(provtwo)) as prov
from (
    select jt.tuid as tuid, r2.tuid as provone, s2.tuid as provtwo
    from dj1_2 as r2 (tuid, id, da, db, dc, hv),
        dj2_2 as s2(tuid, jid, da, db, dc, hv),
        lateral readjoin(1, r2.tuid, s2.tuid) as jt(tuid)
) sub, lateral readfilter(2, sub.tuid) as ft(tuid);