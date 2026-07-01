PROVENANCE OF(
    SELECT c_custkey,
        c_name,
        sum(l_extendedprice * (1 - l_discount)) as revenue,
        c_acctbal,
        n_name,
        c_address,
        c_phone,
        c_comment
    FROM customer use provenance(c_custkey),
        orders use provenance(o_orderkey),
        lineitem use provenance(l_linenumber),
        nation use provenance(n_nationkey)
    WHERE c_custkey = o_custkey
        and l_orderkey = o_orderkey
        and o_orderdate >= TO_DATE('1993-10-01', 'YYYY-MM-DD')
        and o_orderdate < TO_DATE('1994-01-01', 'YYYY-MM-DD')
        and l_returnflag = 'R'
        and c_nationkey = n_nationkey
    GROUP BY c_custkey,
        c_name,
        c_acctbal,
        c_phone,
        n_name,
        c_address,
        c_comment
    ORDER BY revenue desc
    limit 20
);
