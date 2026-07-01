select writejoin(3, subb.tuid, s1.tuid) as tuid, subb.ga as ga, subb.minv as minv, s1.c1to10 as c1to10
from (
    select writeaggregation(2, array_agg(sub.tuid)) as tuid, sub.ga as ga, min(sub.va) as minv
        from vpgn100_1 as sub (tuid, id, ga, va, vb)
    group by sub.ga
) as subb, jc_1 as s1(tuid, jid, c1to1, c1to10, c1to50)
where subb.minv = s1.c1to10;
