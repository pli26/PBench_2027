PROVENANCE OF(
    SELECT l_shipmode,
        sum(CASE WHEN o_orderpriORity = '1-URGENT' OR o_orderpriority = '2-HIGH' THEN 1 ELSE 0 END) AS high_line_count,
        sum(CASE WHEN o_orderpriORity <> '1-URGENT' AND o_orderpriORity <> '2-HIGH' THEN 1 ELSE 0 END) AS low_line_count
    FROM orders USE PROVENANCE(o_orderkey),
        lineitem USE PROVENANCE(l_linenumber)
    WHERE o_orderkey = l_orderkey
        AND (l_shipmode = 'MAIL' OR l_shipmode = 'SHIP')
        AND l_commitdate < l_receiptdate
        AND l_shipdate < l_commitdate
        AND l_receiptdate >= cast('1994-01-01' as date)
        AND l_receiptdate < cast('1995-01-01' as date)
    GROUP BY l_shipmode
    ORDER BY l_shipmode
);
