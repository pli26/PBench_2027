PROVENANCE OF(
    SELECT *
    FROM (
        SELECT c_count, count(*) AS custdist
        FROM (
            SELECT c_custkey, count(o_orderkey) AS c_count
            FROM customer use provenance(c_custkey) LEFT OUTER JOIN orders use provenance(o_orderkey) ON (c_custkey = o_custkey AND NOT(o_comment LIKE '%special%requests%'))
            GROUP BY c_custkey
        ) c_orders
    GROUP BY c_count
    ) x
    ORDER BY custdist DESC,
    c_count DESC
);
