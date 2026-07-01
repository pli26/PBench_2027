SELECT
       "orderby"."tuid" AS "tuid",
       "subquery7"."n_name" AS "n_name",
       "subquery7"."revenue" AS "revenue",
       (
              array_agg("subquery7"."provone") || array_agg("subquery7"."provtwo") || array_agg("subquery7"."provthree") || array_agg("subquery7"."provfour") || array_agg("subquery7"."provfive") || array_agg("subquery7"."provsix")
       ) as provs
FROM
       (
              SELECT
                     "group"."tuid" AS "tuid",
                     concat_agg("subquery6"."n_name") AS "n_name",
                     concat_agg(
                            ("subquery6"."l_extendedprice") || (
                                   (ARRAY [] :: int4 []) || ("subquery6"."l_discount")
                            )
                     ) AS "revenue",
                     array_agg("subquery6"."provone") AS "provone",
                     array_agg("subquery6"."provtwo") AS "provtwo",
                     array_agg("subquery6"."provthree") AS "provthree",
                     array_agg("subquery6"."provfour") AS "provfour",
                     array_agg("subquery6"."provfive") AS "provfive",
                     array_agg("subquery6"."provsix") AS "provsix"
              FROM
                     (
                            SELECT
                                   "join"."tuid" AS "tuid",
                                   "RTE4"."n_name" AS "n_name",
                                   "RTE2"."l_extendedprice" AS "l_extendedprice",
                                   "RTE2"."l_discount" AS "l_discount",
                                   "RTE0"."tuid" AS "provone",
                                   "RTE1"."tuid" AS "provtwo",
                                   "RTE2"."tuid" AS "provthree",
                                   "RTE3"."tuid" AS "provfour",
                                   "RTE4"."tuid" AS "provfive",
                                   "RTE5"."tuid" AS "provsix"
                            FROM
                                   customer_2 AS "RTE0"(
                                          "tuid",
                                          "c_custkey",
                                          "c_name",
                                          "c_address",
                                          "c_nationkey",
                                          "c_phone",
                                          "c_acctbal",
                                          "c_mktsegment",
                                          "c_comment"
                                   ),
                                   orders_2 AS "RTE1"(
                                          "tuid",
                                          "o_orderkey",
                                          "o_custkey",
                                          "o_orderstatus",
                                          "o_totalprice",
                                          "o_orderdate",
                                          "o_orderpriority",
                                          "o_clerk",
                                          "o_shippriority",
                                          "o_comment"
                                   ),
                                   lineitem_2 AS "RTE2"(
                                          "tuid",
                                          "l_orderkey",
                                          "l_partkey",
                                          "l_suppkey",
                                          "l_linenumber",
                                          "l_quantity",
                                          "l_extendedprice",
                                          "l_discount",
                                          "l_tax",
                                          "l_returnflag",
                                          "l_linestatus",
                                          "l_shipdate",
                                          "l_commitdate",
                                          "l_receiptdate",
                                          "l_shipinstruct",
                                          "l_shipmode",
                                          "l_comment"
                                   ),
                                   supplier_2 AS "RTE3"(
                                          "tuid",
                                          "s_suppkey",
                                          "s_name",
                                          "s_address",
                                          "s_nationkey",
                                          "s_phone",
                                          "s_acctbal",
                                          "s_comment"
                                   ),
                                   nation_2 AS "RTE4"(
                                          "tuid",
                                          "n_nationkey",
                                          "n_name",
                                          "n_regionkey",
                                          "n_comment"
                                   ),
                                   region_2 AS "RTE5"(
                                          "tuid",
                                          "r_regionkey",
                                          "r_name",
                                          "r_comment"
                                   ),
                                   LATERAL readjoin(
                                          1,
                                          "RTE0"."tuid",
                                          "RTE1"."tuid",
                                          "RTE2"."tuid",
                                          "RTE3"."tuid",
                                          "RTE4"."tuid",
                                          "RTE5"."tuid"
                                   ) AS "join"("tuid")
                     ) AS "subquery6"(
                            "tuid",
                            "n_name",
                            "l_extendedprice",
                            "l_discount"
                     ),
                     LATERAL readaggregation(
                            2,
                            "subquery6"."tuid"
                     ) AS "group"("tuid")
              GROUP BY
                     ("group"."tuid")
       ) AS "subquery7"(
              "tuid",
              "n_name",
              "revenue"
       ),
       LATERAL readorderby(4, "subquery7"."tuid") AS "orderby"("tuid");