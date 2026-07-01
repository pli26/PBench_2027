PROVENANCE OF(
    select * from (
        SELECT supp_nation,
            cust_nation,
            l_year,
            sum(volume) AS revenue
        FROM (
            SELECT n1.n_name AS supp_nation,
                n2.n_name AS cust_nation,
                cast(substring(cast(l_shipdate as varchar), 1, 4) as int) AS l_year,
                l_extendedprice * (1 - l_discount) AS volume
            FROM supplier USE PROVENANCE(s_suppkey),
                lineitem USE PROVENANCE(l_orderkey),
                orders USE PROVENANCE(o_orderkey),
                customer USE PROVENANCE(c_custkey),
                nation USE PROVENANCE(n_nationkey) as n1,
                nation USE PROVENANCE(n_nationkey) as n2
            WHERE s_suppkey = l_suppkey
                AND o_orderkey = l_orderkey
                AND c_custkey = o_custkey
                AND s_nationkey = n1.n_nationkey
                AND c_nationkey = n2.n_nationkey
                AND ((n1.n_name = 'FRANCE' AND n2.n_name = 'GERMANY') OR (n1.n_name = 'GERMANY' AND n2.n_name = 'FRANCE'))
                AND l_shipdate >= cast('1995-01-01' as date)
                AND l_shipdate <= cast('1996-12-31' as date)
        ) aa
        GROUP BY supp_nation,
            cust_nation,
            l_year
    )tt
    ORDER BY supp_nation,
        cust_nation,
        l_year
);
