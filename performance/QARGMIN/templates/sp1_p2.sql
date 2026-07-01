select (array_agg(subb.tuid) || (array_agg(s2.tuid)) ) as provs
from (
    select aggs.tuid as tuid, array_agg(sub.tuid) as provone
        from vpgn100_2 as sub(tuid, id, ga, va, vb), lateral readaggregation(2, sub.tuid) as aggs(tuid)
    group by aggs.tuid
) subb, jc_2 as s2( tuid, jid, c1to1, c1to10, c1to50), lateral readjoin(3, subb.tuid, s2.tuid) as jt2(tuid)