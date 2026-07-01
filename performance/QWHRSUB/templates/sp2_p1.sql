select writeaggregation(2, array_agg(sub.tuid)) as tuid, avg(sub.va) as ava, sub.ga as ga
from (
    select writejoin(1, v.tuid) as tuid, v.ga as ga, v.va as va
    from vpgn100_1 v
    where exists (select 1 from jc_1 j1 where v.ga = j1.c1to10)
    and exists (select 1 from jc_1 j2 where v.ga = j2.c1to10)
) sub
group by sub.ga
