select (array_agg(sub.provone) || array_agg(sub.provtwo)) as prov
from (
select jt.tuid, r2.tuid as provone, s2.tuid as provtwo
from vpgn1k_2 as r2 (tuid, id, ga, va, vb), js_2 as s2 (tuid, jid, p1, p10, p50),
    lateral readjoin(1, r2.tuid, s2.tuid) as jt(tuid)
) as sub, lateral readaggregation(2, sub.tuid) as agg(tuid)
group by agg.tuid