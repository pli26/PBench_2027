
-- PgLlProvenance
-- translation date: 08.02.18 14:04:39


-- *** preparation steps
DROP SEQUENCE IF EXISTS prov_id CASCADE;
CREATE SEQUENCE prov_id;
DROP MATERIALIZED VIEW IF EXISTS customer_1;
CREATE MATERIALIZED VIEW customer_1 AS
(SELECT nextval('prov_id') :: int4 AS "tuid", 
        "customer"."c_custkey" AS "c_custkey", 
        "customer"."c_name" AS "c_name", 
        "customer"."c_address" AS "c_address", 
        "customer"."c_nationkey" AS "c_nationkey", 
        "customer"."c_phone" AS "c_phone", 
        "customer"."c_acctbal" AS "c_acctbal", 
        "customer"."c_mktsegment" AS "c_mktsegment", 
        "customer"."c_comment" AS "c_comment"
 FROM customer AS "customer"("c_custkey", 
                             "c_name", 
                             "c_address", 
                             "c_nationkey", 
                             "c_phone", 
                             "c_acctbal", 
                             "c_mktsegment", 
                             "c_comment"));
DROP MATERIALIZED VIEW IF EXISTS customer_2;
CREATE MATERIALIZED VIEW customer_2 AS
(SELECT "customer_1"."tuid" AS "tuid", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_custkey", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_name", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_address", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_nationkey", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_phone", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_acctbal", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_mktsegment", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_comment"
 FROM customer_1 AS "customer_1"("tuid", 
                                 "c_custkey", 
                                 "c_name", 
                                 "c_address", 
                                 "c_nationkey", 
                                 "c_phone", 
                                 "c_acctbal", 
                                 "c_mktsegment", 
                                 "c_comment"));
DROP MATERIALIZED VIEW IF EXISTS customer_1;
CREATE MATERIALIZED VIEW customer_1 AS
(SELECT nextval('prov_id') :: int4 AS "tuid", 
        "customer"."c_custkey" AS "c_custkey", 
        "customer"."c_name" AS "c_name", 
        "customer"."c_address" AS "c_address", 
        "customer"."c_nationkey" AS "c_nationkey", 
        "customer"."c_phone" AS "c_phone", 
        "customer"."c_acctbal" AS "c_acctbal", 
        "customer"."c_mktsegment" AS "c_mktsegment", 
        "customer"."c_comment" AS "c_comment"
 FROM customer AS "customer"("c_custkey", 
                             "c_name", 
                             "c_address", 
                             "c_nationkey", 
                             "c_phone", 
                             "c_acctbal", 
                             "c_mktsegment", 
                             "c_comment"));
DROP MATERIALIZED VIEW IF EXISTS customer_2;
CREATE MATERIALIZED VIEW customer_2 AS
(SELECT "customer_1"."tuid" AS "tuid", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_custkey", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_name", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_address", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_nationkey", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_phone", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_acctbal", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_mktsegment", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "c_comment"
 FROM customer_1 AS "customer_1"("tuid", 
                                 "c_custkey", 
                                 "c_name", 
                                 "c_address", 
                                 "c_nationkey", 
                                 "c_phone", 
                                 "c_acctbal", 
                                 "c_mktsegment", 
                                 "c_comment"));
DROP MATERIALIZED VIEW IF EXISTS orders_1;
CREATE MATERIALIZED VIEW orders_1 AS
(SELECT nextval('prov_id') :: int4 AS "tuid", 
        "orders"."o_orderkey" AS "o_orderkey", 
        "orders"."o_custkey" AS "o_custkey", 
        "orders"."o_orderstatus" AS "o_orderstatus", 
        "orders"."o_totalprice" AS "o_totalprice", 
        "orders"."o_orderdate" AS "o_orderdate", 
        "orders"."o_orderpriority" AS "o_orderpriority", 
        "orders"."o_clerk" AS "o_clerk", 
        "orders"."o_shippriority" AS "o_shippriority", 
        "orders"."o_comment" AS "o_comment"
 FROM orders AS "orders"("o_orderkey", 
                         "o_custkey", 
                         "o_orderstatus", 
                         "o_totalprice", 
                         "o_orderdate", 
                         "o_orderpriority", 
                         "o_clerk", 
                         "o_shippriority", 
                         "o_comment"));
DROP MATERIALIZED VIEW IF EXISTS orders_2;
CREATE MATERIALIZED VIEW orders_2 AS
(SELECT "orders_1"."tuid" AS "tuid", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "o_orderkey", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "o_custkey", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "o_orderstatus", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "o_totalprice", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "o_orderdate", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "o_orderpriority", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "o_clerk", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "o_shippriority", 
        ARRAY[nextval('prov_id') :: int4] :: int4[] AS "o_comment"
 FROM orders_1 AS "orders_1"("tuid", 
                             "o_orderkey", 
                             "o_custkey", 
                             "o_orderstatus", 
                             "o_totalprice", 
                             "o_orderdate", 
                             "o_orderpriority", 
                             "o_clerk", 
                             "o_shippriority", 
                             "o_comment"));


