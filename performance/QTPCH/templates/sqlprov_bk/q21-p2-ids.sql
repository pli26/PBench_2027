SELECT
       "subs"."provone" || "subs"."provtwo" || "subs"."provthree" || "subs"."provfour" AS provs
from
       (
              SELECT
                     "orderby"."tuid" AS "tuid",
                     "subquery7"."s_name" AS "s_name",
                     "subquery7"."numwait" AS "numwait",
                     "subquery7"."provone" AS "provone",
                     "subquery7"."provtwo" AS "provtwo",
                     "subquery7"."provthree" AS "provthree",
                     "subquery7"."provfour" AS "provfour"
              FROM
                     (
                            SELECT
                                   "group"."tuid" AS "tuid",
                                   concat_agg("subquery6"."s_name") AS "s_name",
                                   ARRAY [] :: int4 [] AS "numwait",
                                   array_agg("subquery6"."provone") AS "provone",
                                   array_agg("subquery6"."provtwo") AS "provtwo",
                                   array_agg("subquery6"."provthree") AS "provthree",
                                   array_agg("subquery6"."provfour") AS "provfour"
                            FROM
                                   (
                                          SELECT
                                                 "join"."tuid" AS "tuid",
                                                 "RTE0"."s_name" AS "s_name",
                                                 "RTE0"."tuid" AS "provone",
                                                 "RTE1"."tuid" AS "provtwo",
                                                 "RTE2"."tuid" AS "provthree",
                                                 "RTE3"."tuid" AS "provfour"
                                          FROM
                                                 supplier_2 AS "RTE0"(
                                                        "tuid",
                                                        "s_suppkey",
                                                        "s_name",
                                                        "s_address",
                                                        "s_nationkey",
                                                        "s_phone",
                                                        "s_acctbal",
                                                        "s_comment"
                                                 ),
                                                 lineitem_2 AS "RTE1"(
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
                                                 orders_2 AS "RTE2"(
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
                                                 nation_2 AS "RTE3"(
                                                        "tuid",
                                                        "n_nationkey",
                                                        "n_name",
                                                        "n_regionkey",
                                                        "n_comment"
                                                 ),
                                                 LATERAL readjoin(
                                                        3,
                                                        "RTE0"."tuid",
                                                        "RTE1"."tuid",
                                                        "RTE2"."tuid",
                                                        "RTE3"."tuid"
                                                 ) AS "join"("tuid")
                                   ) AS "subquery6"(
                                          "tuid",
                                          "s_name"
                                   ),
                                   LATERAL readaggregation(
                                          4,
                                          "subquery6"."tuid"
                                   ) AS "group"("tuid")
                            GROUP BY
                                   ("group"."tuid")
                     ) AS "subquery7"(
                            "tuid",
                            "s_name",
                            "numwait"
                     ),
                     LATERAL readorderby(6, "subquery7"."tuid") AS "orderby"("tuid")
       ) subs;