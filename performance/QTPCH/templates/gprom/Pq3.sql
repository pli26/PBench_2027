PROVENANCE OF(
    select l_orderkey,
        sum(l_extendedprice*(1-l_discount)) as revenue,
        o_orderdate,
        o_shippriority
    from lineitem USE PROVENANCE(l_orderkey),
        orders USE PROVENANCE(o_orderkey),
        customer USE PROVENANCE(c_custkey)
    where c_mktsegment = 'BUILDING'
        and c_custkey = o_custkey
        and l_orderkey = o_orderkey
        and o_orderdate < TO_DATE('1995-03-15', 'YYYY-MM-DD')
        and l_shipdate > TO_DATE('1995-03-15', 'YYYY-MM-DD')
    group by l_orderkey,
        o_orderdate,
        o_shippriority
    order by revenue desc,
        o_orderdate
    limit 10
);
