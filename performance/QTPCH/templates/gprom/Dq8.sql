-- SELECT substr(cast(o_orderdate as varchar), 1, 4) AS o_year,
PROVENANCE OF(
    SELECT o_year,
        sum(CASE WHEN nation = 'BRAZIL' THEN volume ELSE 0 END) / sum(volume) AS mkt_share
    FROM (
        SELECT cast(substring(cast(o_orderdate as varchar), 1, 4) as int) AS o_year,
            l_extendedprice * (1 - l_discount) AS volume,
            n2.n_name AS nation
        FROM part use PROVENANCE(p_partkey),
            supplier use provenance(s_suppkey),
            lineitem use provenance(l_orderkey),
            orders use provenance(o_orderkey),
            customer use provenance(c_custkey),
            nation use provenance(n_nationkey) as n1,
            nation use provenance(n_nationkey) as n2,
            region use provenance(r_regionkey)
        WHERE p_partkey = l_partkey
            AND s_suppkey = l_suppkey
            AND l_orderkey = o_orderkey
            AND o_custkey = c_custkey
            AND c_nationkey = n1.n_nationkey
            AND n1.n_regionkey = r_regionkey
            AND r_name = 'AMERICA'
            AND s_nationkey = n2.n_nationkey
            AND o_orderdate >= cast('1995-01-01' as date)
            AND o_orderdate <= cast('1996-12-31' as date)
            AND p_type = 'ECONOMY ANODIZED STEEL'
    ) l
    GROUP BY o_year
    ORDER BY o_year
);
