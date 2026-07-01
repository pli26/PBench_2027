-- using default substitutions
-- $ID$
-- TPC-H/TPC-R Customer Distribution Query (Q13)
-- Functional Query Definition
-- Approved February 1998

select
    _t.tuid as tuid,
    provSize(c_count) as c_count,
    provSize(custdist) as custdist,
    provtwo || provone as provs
from
    (
        select
            _g.tuid as tuid,
        	concat_agg(c_count) as c_count,
        	empty() as custdist,
            array_agg(provone) as provone,
            array_agg(provtwo) as provtwo
        from
        	(
                select
                    _g.tuid as tuid,
                    concat_agg(c_custkey) as c_custkey,
                    concat_agg(o_orderkey) as c_count,
                    array_agg(provone) as provone,
                    array_agg(provtwo) as provtwo
                from
                    (
                		select
                            _j.tuid as tuid,
                			c_custkey as c_custkey,
                			o_orderkey as o_orderkey,
                            c.tuid as provone,
                            o.tuid as provtwo
                		from
                            logJoin _j
                            join customer_2 c on (location = 4 AND _j.tuids[1]=c.tuid)
                			left outer join orders_2 o on (_j.tuids[2]=o.tuid)
                    ) as _t
                    , readAggregation(3, _t.tuid) _g
        		group by
        			_g.tuid
        	) as c_orders
            , readAggregation(2, c_orders.tuid) _g
        group by
        	_g.tuid
    ) as _t
    , readOrderBy(1, _t.tuid) _o
order by
    _o.sequence;