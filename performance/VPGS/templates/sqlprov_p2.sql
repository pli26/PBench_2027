select grp.tuid as tuid, array_agg(sub.tuid) as prov
    from FROM_TABLE as sub (tuid, ATTRIBUTES),
    lateral readaggregation(2, sub.tuid) as grp(tuid)
group by grp.tuid;