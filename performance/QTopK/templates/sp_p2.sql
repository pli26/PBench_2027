select ord.tuid as tuid, provone as prov
from (
    select agg.tuid as tuid, array_agg(provone) as provone
    from (
        select jt.tuid as tuid, r2.tuid as provone
        from fp_2 as r2(tuid, id, ga, gb, gc, hv, va, vb, vc),
            lateral readjoin(1, r2.tuid) as jt(tuid);
    ) sub (tuid, provone), lateral readaggregation(2, sub.tuid) as agg(tuid)
    group by agg.tuid
) subb, lateral readorderby(3, subb.tuid) as ord(tuid);
