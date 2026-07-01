select ord.tuid as tuid, provone as prov
from (
    select agg.tuid as tuid, array_agg(sub.tuid) as provone
        from fp_2 as sub (tuid, id, ga, gb, gc, hv, va, vb, vc),
            lateral readaggregation(2, sub.tuid) as agg(tuid)
    group by agg.tuid
) subb, lateral readorderby(3, subb.tuid) as ord(tuid);
