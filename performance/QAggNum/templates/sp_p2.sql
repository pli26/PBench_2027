select grp.tuid as tuid, array_agg(r2.tuid) as prov
    from fp_2 as r2(tuid, id, ga, gb, gc, hv, va, vb, vc), lateral readaggregation(2, r2.tuid) as grp(tuid)
group by grp.tuid;