select jt.tuid as tuid, r2.tuid as provone, s2.tuid as provtwo
from TABLE_2 as r2 (tuid, id, ga, va, vb),
    JOINED_TBL_2 as s2 (tuid, jid, c1to1, c1to10, c1to50),
    lateral readjoin(1, r2.tuid, s2.tuid) as jt(tuid);