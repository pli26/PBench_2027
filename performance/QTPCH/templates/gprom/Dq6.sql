PROVENANCE OF (
    SELECT sum(l_extendedprice * l_discount) as revenue
    FROM lineitem USE PROVENANCE(l_orderkey)
    WHERE l_shipdate >= cast('1994-01-01' as date)
        AND l_shipdate < cast('1995-01-01' as date)
        AND l_discount > 0.05
        AND l_discount < 0.07
        AND l_quantity < 24
);
