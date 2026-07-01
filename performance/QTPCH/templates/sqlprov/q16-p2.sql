select
    provone || provtwo as provs
from
    (
        select
            _t.tuid as tuid,
            provSize(p_brand) as p_brand,
            provSize(p_type) as p_type,
            provSize(p_size) as p_size,
            provSize(supplier_cnt) as supplier_cnt,
            provone,
            provtwo
        from
            (
                select
                    _g.tuid as tuid,
                    concat_agg(p_brand) as p_brand,
                    concat_agg(p_type) as p_type,
                    concat_agg(p_size) as p_size,
                    concat_agg(ps_suppkey) as supplier_cnt,
                    array_agg(provone) as provone,
                    array_agg(provtwo) as provtwo
                from
                    (
                        select
                            _j.tuid as tuid,
                            p_brand as p_brand,
                            p_type as p_type,
                            p_size as p_size,
                            ps_suppkey as ps_suppkey,
                            ps.tuid as provone,
                            p.tuid as provtwo
                        from
                            partsupp_2 ps,
                            part_2 p,
                            readJoin(3, ps.tuid, p.tuid) _j
                    ) as _t,
                    readAggregation(2, _t.tuid) _g
                group by
                    _g.tuid
            ) as _t,
            readOrderBy(1, _t.tuid) _o
        order by
            _o.sequence
    ) subs;