select writeaggregation(2, array_agg(sub.tuid)) as tuid, sub.ga, avg(sub.va) as va, avg(sub.vb) as vb
from(
    select writejoin(1, r1.tuid, s1.tuid, t1.tuid, u1.tuid) as tuid, r1.ga, r1.va, r1.vb
    from vpgn1k_1 as r1 (tuid, id, ga, va, vb),
        js_1 as s1 (tuid, jid, p1, p10, p50),
        jj_1 as t1 (tuid, jjid, c1, c2, c5, c10),
        jjj_1 as u1 (tuid, jjjid, cc1, cc2, cc5, cc10)
    where r1.ga = p10 and r1.ga = t1.c5 and ga = cc2
) sub
group by sub.ga