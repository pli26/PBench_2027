select writefilter(2, subb.tuid) as tuid, subb.gb as gb
from (
    select distinct on (sub.gb) sub.tuid as tuid, sub.gb
    from (
        select writejoin(1, r1.tuid, s1.tuid) as tuid, r1.gb as gb
        from TABLE_1 as r1 (tuid, id, ga, gb, gc, hv, va, vb, vc),
            JOINED_TBL_1 as s1 (tuid, jid, c1to1, c1to10, c1to50)
        where r1.gb = s1.c1to10
    ) sub
) subb;