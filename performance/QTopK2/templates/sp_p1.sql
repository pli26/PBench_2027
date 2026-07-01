select writeorderby(3, subb.tuid, row_number() over(order by subb.ava range unbounded preceding)) as tuid, gc, ava, avb
from (
    select writeaggregation(2, array_agg(sub.tuid)) as tuid, gc, min(va) as ava, avg(vb) as avc
        from fp_1 as sub (tuid, id, ga, gb, gc, hv, va, vb, vc)
    group by gc
) subb (tuid, gc, ava, avb)
order by subb.ava
limit LIMIT_VALUE;
