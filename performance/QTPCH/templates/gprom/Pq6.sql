PROVENANCE OF(
    SELECT sum(l_extendedprice * l_discount) as revenue
    FROM lineitem USE PROVENANCE(l_orderkey)
    WHERE l_shipdate >= TO_DATE('1994-01-01', 'YYYY-MM-DD')
        AND l_shipdate < TO_DATE('1995-01-01', 'YYYY-MM-DD')
        AND l_discount > 0.05
        AND l_discount < 0.07
        AND l_quantity < 24
);
