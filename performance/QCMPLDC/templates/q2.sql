select ga, count(vb) as cvb, avg(vb) as avb
from vpgn1k, jc
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

group by ga