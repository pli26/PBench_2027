select writejoin(4, subbb.tuid, s1.tuid) as tuid, subbb.gb, subbb.va, subbb.vb
from (
    select writejoin(3, subb.tuid) as tuid, subb.gb, subb.va, subb.vb
    from (
        select writeaggregation(2, array_agg(sub.tuid)) as tuid, sub.gb, avg(sub.va) as va, avg(sub.vb) as vb
        from(
            select writejoin(1, r1.tuid) as tuid, r1.gb, r1.va, r1.vb
            from fp_1 as r1 (tuid, id, ga, gb, gc, hv, va, vb, vc)
        ) as sub
        group by sub.gb
    ) as subb
    where subb.va < HAVING_VALUE
) as subbb, jc_1 as s1 (tuid, jid, c1to1, c1to10, c1to50)
where subbb.gb = c1to1;