select writefilter(1, sub.tuid) as tuid, sub.DISTINCT_ATTRIBUTE as DISTINCT_ATTRIBUTE
from (
    select distinct on (r1.DISTINCT_ATTRIBUTE) r1.tuid as tuid, r1.DISTINCT_ATTRIBUTE as DISTINCT_ATTRIBUTE
    from fp_1 as r1 (tuid, id, ga, gb, gc, hv, va, vb, vc)
) sub;