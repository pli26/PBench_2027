select writejoin(1, r1.tuid, s1.tuid) as tuid, r1.ga as ga, r1.va as va, r1.vb as vb
from TABLE_1 as r1 (tuid, id, ga, va, vb),
    JOINED_TBL_1 as s1 (tuid, jid, c1to1, c1to10, c1to50)
where r1.ga = s1.c1to10 AND WHERECONDITION