SELECT nation, o_year, sum(amount) AS sum_profit
FROM (
    SELECT n_name AS nation, cast(to_char(o_orderdate, 'YYYY') AS int) AS o_year, l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity AS amount
    FROM part, supplier, lineitem, partsupp, orders, nation
    where s_suppkey = l_suppkey AND ps_suppkey = l_suppkey AND ps_partkey = l_partkey AND p_partkey = l_partkey AND o_orderkey = l_orderkey AND s_nationkey = n_nationkey AND p_name LIKE '%green%'
    ) l
GROUP BY nation, o_year ORDER BY nation, o_year desc;
