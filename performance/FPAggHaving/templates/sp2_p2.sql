select (provone || s2.tuid) as prov
from (
    select flt.tuid as tuid, provone as provone
    from (
        select agg.tuid as tuid, (array_agg(provone)) as provone
        from (
            select jt.tuid as tuid, r2.tuid as provone
            from fp_2 as r2 (tuid, id, ga, gb, gc, hv, va, vb, vc),
                lateral readjoin(1, r2.tuid) as jt(tuid)
        ) sub, lateral readaggregation(2, sub.tuid) as agg(tuid)
        group by agg.tuid
    ) subb, lateral readjoin(3, subb.tuid) as flt(tuid)
) as subbb, jc_2 as s2(tuid, jid, c1to1, c1to10, c1to50),
lateral readjoin(4, subbb.tuid, s2.tuid) as jjt(tuid);