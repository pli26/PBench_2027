select writeaggregation(3, array_agg(subb.tuid)) as tuid, max(subb.va) as maxva, max(subb.vb) as maxvb
from (
    select writeaggregation(2, array_agg(sub.tuid)) as tuid, sub.gb, avg(sub.va) as va, avg(sub.vb) as vb
        from fp_1 as sub (tuid, id, ga, gb, gc, hv, va, vb, vc)
    group by sub.gb
) as subb;