select writefilter(2, subb.tuid) as tuid, subb.DISTINCT_ATTRIBUTE_A as DISTINCT_ATTRIBUTE_A
from (
    select distinct on (sub.DISTINCT_ATTRIBUTE_A) sub.tuid as tuid, sub.DISTINCT_ATTRIBUTE_A
    from (
        select writejoin(1, r1.tuid, s1.tuid) as tuid, r1.DISTINCT_ATTRIBUTE_A
        from dj1_1 as r1(tuid, id, da, db, dc, hv), dj2_1 as s1(tuid, jid, da, db, dc, hv)
        where r1.DISTINCT_ATTRIBUTE_A = s1.DISTINCT_ATTRIBUTE_B
    ) sub
) subb;