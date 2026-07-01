select grp.tuid as tuid, array_agg(sub.prov) as prov
from (
    select jnd.tuid as tuid, v.tuid as prov
    from vpgn100_2 v, lateral readjoin(1, v.tuid) as jnd(tuid)
) sub, lateral readaggregation(2, sub.tuid) as grp(tuid)
group by grp.tuid
