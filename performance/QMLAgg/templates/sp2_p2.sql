select array_agg(prov) as prov
from (
    select agg.tuid as tuid, array_agg(sub.tuid) as prov
            from fp_2 as sub(tuid, id, ga, gb, gc, hv, va, vb, vc),
            lateral readaggregation(2, sub.tuid) as agg(tuid)
    group by agg.tuid
) as subb, lateral readaggregation(3, subb.tuid) as finals(tuid)
group by finals.tuid;