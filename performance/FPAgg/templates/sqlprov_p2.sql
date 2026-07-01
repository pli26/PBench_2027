select grp.tuid as tuid, array_agg(r2.tuid) as prov
    from FROM_TABLE as r2(tuid, ATTRIBUTES), lateral readaggregation(2, r2.tuid) as grp(tuid)
group by grp.tuid;