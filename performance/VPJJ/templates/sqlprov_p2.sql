select (array_agg(sub.provone) || array_agg(sub.provtwo) || array_agg(sub.provthree)) as prov
from (
select jt.tuid, r2.tuid as provone, s2.tuid as provtwo, t2.tuid as provthree
from vpgn1k_2 as r2 (tuid, id, ga, va, vb),
    js_2 as s2 (tuid, jid, p1, p10, p50),
    jj_2 as t2 (tuid, jjid, c1, c2, c5, c10),
    lateral readjoin(1, r2.tuid, s2.tuid, t2.tuid) as jt(tuid)
) as sub, lateral readaggregation(2, sub.tuid) as agg(tuid)
group by agg.tuid