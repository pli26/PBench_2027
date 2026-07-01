PROVENANCE OF(
    SELECT 100.00 * sum(CASE WHEN p_type LIKE 'PROMO%' THEN l_extendedprice * (1 - l_discount) ELSE 0 END) / sum(l_extendedprice * (1 - l_discount)) AS promo_revenue
    FROM lineitem use provenance(l_linenumber),
        part use provenance(p_partkey)
    WHERE l_partkey = p_partkey
        AND l_shipdate >= TO_DATE('1995-09-01', 'YYYY-MM-DD')
        AND l_shipdate < TO_DATE('1995-10-01', 'YYYY-MM-DD')
);