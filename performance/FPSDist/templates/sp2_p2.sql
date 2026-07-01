select (array_agg(provone) || array_agg(provtwo)) as prov
from (
    select jt.tuid as tuid, sub1.provone as provone, sub2.provtwo as provtwo
    from
    (
        select ft1.tuid as tuid, r2.tuid as provone
        from dj1_2 as r2 (tuid, id, da, db, dc, hv), lateral readfilter(1, r2.tuid) as ft1(tuid)
    ) sub1,
    (
        select ft2.tuid as tuid, s2.tuid as provtwo
        from dj2_2 as s2(tuid, jid, da, db, dc, hv), lateral readfilter(2, s2.tuid) as ft2(tuid)
    ) sub2,
    lateral readjoin(3, sub1.tuid, sub2.tuid) as jt(tuid)
) subb, lateral readfilter(4, subb.tuid) as ft(tuid);