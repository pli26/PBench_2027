select writeaggregation(2, array_agg(sub.tuid)) as tuid, sub.ga as ga, avg(vb) as avb, count(vb) as cvb
from (
    select writejoin(1, r1.tuid, s1.tuid) as tuid, r1.ga as ga, r1.vb as vb
    from vpgn1k_1 as r1( tuid, id, ga, va, vb),
        jc_1 as s1(tuid, jid, c1to1, c1to10, c1to50)
    where
    (
        ga >= 0 and ga <= 300
        AND va >= 20 and va <= 280
        AND vb >= 150 and vb <= 250
        AND ga = c1to50
    )
    OR
    (
        ga >= 301 and ga <= 600
        AND va >= 320 and va <= 580
        AND vb >= 450 and vb <= 550
        AND ga = c1to50
    )
    OR
    (
        ga >= 601 and ga <= 900
        AND va >= 620 and va <= 880
        AND vb >= 750 and vb <= 850
        AND ga = c1to50
    )
) sub
group by sub.ga;