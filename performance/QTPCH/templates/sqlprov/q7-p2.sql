select
       (
              "subs"."provone" || "subs"."provtwo" || "subs"."provthree" || "subs"."provfour" || "subs"."provfive" || "subs"."provsix"
       ) as provs
from
       (
              SELECT
                     "orderby"."tuid" AS "tuid",
                     "subquery7"."supp_nation" AS "supp_nation",
                     "subquery7"."cust_nation" AS "cust_nation",
                     "subquery7"."l_year" AS "l_year",
                     "subquery7"."revenue" AS "revenue",
                     "subquery7"."provone" AS "provone",
                     "subquery7"."provtwo" AS "provtwo",
                     "subquery7"."provthree" AS "provthree",
                     "subquery7"."provfour" AS "provfour",
                     "subquery7"."provfive" AS "provfive",
                     "subquery7"."provsix" AS "provsix"
              FROM
                     (
                            SELECT
                                   "group"."tuid" AS "tuid",
                                   concat_agg("subquery6"."supp_nation") AS "supp_nation",
                                   concat_agg("subquery6"."cust_nation") AS "cust_nation",
                                   concat_agg("subquery6"."l_year") AS "l_year",
                                   concat_agg("subquery6"."volume") AS "revenue",
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
                                                 "RTE4"."n_name" AS "supp_nation",
                                                 "RTE5"."n_name" AS "cust_nation",
                                                 "RTE1"."l_shipdate" AS "l_year",
                                                 ("RTE1"."l_extendedprice") || (
                                                        (ARRAY [] :: int4 []) || ("RTE1"."l_discount")
                                                 ) AS "volume",
                                                 "RTE0"."tuid" AS "provone",
                                                 "RTE1"."tuid" AS "provtwo",
                                                 "RTE2"."tuid" AS "provthree",
                                                 "RTE3"."tuid" AS "provfour",
                                                 "RTE4"."tuid" AS "provfive",
                                                 "RTE5"."tuid" AS "provsix"
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
                                                 customer_2 AS "RTE3"(
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
                                                 nation_2 AS "RTE4"(
                                                        "tuid",
                                                        "n_nationkey",
                                                        "n_name",
                                                        "n_regionkey",
                                                        "n_comment"
                                                 ),
                                                 nation_2 AS "RTE5"(
                                                        "tuid",
                                                        "n_nationkey",
                                                        "n_name",
                                                        "n_regionkey",
                                                        "n_comment"
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
                                          "supp_nation",
                                          "cust_nation",
                                          "l_year",
                                          "volume"
                                   ),
                                   LATERAL readaggregation(
                                          2,
                                          "subquery6"."tuid"
                                   ) AS "group"("tuid")
                            GROUP BY
                                   ("group"."tuid")
                     ) AS "subquery7"(
                            "tuid",
                            "supp_nation",
                            "cust_nation",
                            "l_year",
                            "revenue"
                     ),
                     LATERAL readorderby(4, "subquery7"."tuid") AS "orderby"("tuid")
       ) subs;