select writefilter(3, subb.tuid) as tuid, gc, ava, avb
from (
    select writeaggregation(2, array_agg(sub.tuid)) as tuid, gc, avg(va) as ava, avg(vb) as avc
        from fp_1 as sub (tuid, id, ga, gb, gc, hv, va, vb, vc)
    group by gc
) subb (tuid, gc, ava, avb)
limit LIMIT_VALUE;