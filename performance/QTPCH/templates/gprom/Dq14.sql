PROVENANCE OF(
    SELECT 100.00 * sum(CASE WHEN p_type LIKE 'PROMO%' THEN l_extendedprice * (1 - l_discount) ELSE 0 END) / sum(l_extendedprice * (1 - l_discount)) AS promo_revenue
    FROM lineitem use provenance(l_orderkey),
        part use provenance(p_partkey)
    WHERE l_partkey = p_partkey
        AND l_shipdate >= cast('1995-09-01' as date)
        AND l_shipdate < cast('1995-10-01' as date)
);