select array_agg(provone) || array_agg(provtwo) as provs
from (
select
    _t.tuid as tuid,
    provSize(s_suppkey) as s_suppkey,
    provSize(s_name) as s_name,
    provSize(s_address) as s_address,
    provSize(s_phone) as s_phone,
    provSize(total_revenue) as total_revenue,
    provone,
    provtwo
from
    (
        select
            _j.tuid as tuid,
            s_suppkey as s_suppkey,
            s_name as s_name,
            s_address as s_address,
            s_phone as s_phone,
            total_revenue as total_revenue,
            s.tuid as provone,
            r.tuid as provtwo
        from
        	supplier_2 s,
        	revenue0_2 r
            , readJoin(4, s.tuid, r.tuid) _j
    ) as _t
    , readOrderBy(3, _t.tuid) _o
order by
    _o.sequence
)subs;