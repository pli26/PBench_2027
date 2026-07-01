select writeorderby(3, subb.tuid, row_number() over(order by subb.gc range unbounded preceding)) as tuid, gc, ava, avb
from (
    select writeaggregation(2, array_agg(sub.tuid)) as tuid, gc, avg(va) as ava, avg(vb) as avc
    from (
        select writejoin(1, r1.tuid) as tuid, gc, va, vb, vc
        from fp_1 as r1 (tuid, id, ga, gb, gc, hv, va, vb, vc)
    ) sub
    group by gc
) subb (tuid, gc, ava, avb)
order by subb.gc
limit LIMIT_VALUE;