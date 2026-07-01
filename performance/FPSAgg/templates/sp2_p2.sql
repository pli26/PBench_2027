select agg2.tuid, array_agg(subbb.provone) as provone, array_agg(subbb.provtwo) as provtwo
from (
    select flt.tuid as tuid, subb.provone as provone, s2.tuid as provtwo 
    from (
        select agg.tuid as tuid, array_agg(sub.provone) as provone
        from (
            select jt.tuid as tuid, r2.tuid as provone
            from fp_2 as r2 (tuid, id, ga, gb, gc, hv, va, vb, vc),
                 lateral readjoin(1, r2.tuid) as jt(tuid)
        ) sub, lateral readaggregation(2, sub.tuid) as agg(tuid)
        group by agg.tuid
    ) subb, jc_2 as s2 (tuid, jid, c1to1, c1to10, c1to50),
            lateral readjoin(3, subb.tuid, s2.tuid) as flt(tuid)
) subbb, lateral readaggregation(4, subbb.tuid) as agg2(tuid)
group by agg2.tuid;
