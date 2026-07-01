select (array_agg(provone) || (array_agg(provtwo)) ) as provs
from(
select jt.tuid as tuid, r2.tuid as provone, s2.tuid as provtwo
from vpgn1k_2 as r2(tuid, id, ga, va, vb),
    jc_2 as s2(tuid, jid, c1to1, c1to10, c1to50),
    lateral readjoin(1, r2.tuid, s2.tuid) as jt(tuid)
) sub, lateral readaggregation(2, sub.tuid) as aggs(tuid)
group by aggs.tuid;