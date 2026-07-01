select writeaggregation(2, array_agg(sub.tuid)) as tuid, sub.ga, avg(sub.va) as va, avg(sub.vb) as vb
from(
    select writejoin(1, r1.tuid, s1.tuid) as tuid, r1.ga, r1.va, r1.vb
    from vpgn1k_1 as r1 (tuid, id, ga, va, vb), jc_1 as s1 (tuid, jid, c1to1, c1to10, c1to50)
    where JOIN_CONDITION
) sub
group by sub.ga