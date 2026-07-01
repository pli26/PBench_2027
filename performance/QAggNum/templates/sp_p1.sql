select writeaggregation(2, array_agg(r1.tuid)) as tuid, gb, AGG_COUNT
    from fp_1 as r1 (tuid, id, ga, gb, gc, hv, va, vb, vc)
group by r1.gb;



