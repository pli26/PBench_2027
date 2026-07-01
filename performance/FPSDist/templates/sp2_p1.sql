select writefilter(4, subbb.tuid) as tuid, subbb.DISTINCT_ATTRIBUTE_A as DISTINCT_ATTRIBUTE_A
from (
    select distinct on (subb.DISTINCT_ATTRIBUTE_A) subb.tuid as tuid, subb.DISTINCT_ATTRIBUTE_A as DISTINCT_ATTRIBUTE_A
    from (
        select writejoin(3, t1.tuid, t2.tuid) as tuid, t1.DISTINCT_ATTRIBUTE_A
        from (
            select writefilter(1, sub1.tuid) as tuid, sub1.DISTINCT_ATTRIBUTE_A as DISTINCT_ATTRIBUTE_A
            from (
                select distinct on (r1.DISTINCT_ATTRIBUTE_A) tuid as tuid, r1.DISTINCT_ATTRIBUTE_A
                from dj1_1 as r1(tuid, id, da, db, dc, hv)
            ) sub1
        ) t1,
        (
            select writefilter(2, sub2.tuid) as tuid, sub2.DISTINCT_ATTRIBUTE_B as DISTINCT_ATTRIBUTE_B
            from (
                select distinct on (s1.DISTINCT_ATTRIBUTE_B) tuid as tuid, s1.DISTINCT_ATTRIBUTE_B
                from dj2_1 as s1(tuid, jid, da, db, dc, hv)
            ) sub2
        ) t2
        where t1.DISTINCT_ATTRIBUTE_A = t2.DISTINCT_ATTRIBUTE_B
    ) subb
) subbb;