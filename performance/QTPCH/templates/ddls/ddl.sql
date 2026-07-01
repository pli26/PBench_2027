drop table if exists part ;
drop table if exists supplier ;
drop table if exists partsupp ;
drop table if exists customer ;
drop table if exists orders ;
drop table if exists lineitem ;
drop table if exists nation ;
drop table if exists region ;

DROP INDEX if exists fkey_1;
DROP INDEX if exists fkey_2;
DROP INDEX if exists fkey_3;
DROP INDEX if exists fkey_4;
DROP INDEX if exists fkey_5;
DROP INDEX if exists fkey_6;
DROP INDEX if exists fkey_7;
DROP INDEX if exists fkey_8;
DROP INDEX if exists fkey_9;
DROP INDEX if exists fkey_10;

CREATE TABLE lineitem
(

    L_ORDERKEY bigint,
    L_PARTKEY bigint,
    L_SUPPKEY bigint,
    L_LINENUMBER bigint,
    L_QUANTITY FLOAT(53),
    L_EXTENDEDPRICE FLOAT(53),
    L_DISCOUNT FLOAT(53),
    L_TAX FLOAT(53),
    L_RETURNFLAG VARCHAR(2),
    L_LINESTATUS VARCHAR(2),
    L_SHIPDATE DATE,
    L_COMMITDATE DATE,
    L_RECEIPTDATE DATE,
    L_SHIPINSTRUCT VARCHAR(25),
    L_SHIPMODE VARCHAR(10),
    L_COMMENT VARCHAR(44),
    PRIMARY KEY (L_ORDERKEY, L_LINENUMBER)
);


CREATE TABLE nation
(
   N_NATIONKEY bigint,
   N_NAME VARCHAR(25),
   N_REGIONKEY bigint,
   N_COMMENT VARCHAR(152),
   PRIMARY KEY (N_NATIONKEY)
);



CREATE TABLE orders
(
   O_ORDERKEY bigint,
   O_CUSTKEY bigint,
   O_ORDERSTATUS VARCHAR(2),
   O_TOTALPRICE FLOAT(53),
   O_ORDERDATE DATE,
   O_ORDERPRIORITY VARCHAR(15),
   O_CLERK VARCHAR(15),
   O_SHIPPRIORITY bigint,
   O_COMMENT VARCHAR(79),
   PRIMARY KEY (O_ORDERKEY)
);


CREATE TABLE customer
(
  C_CUSTKEY bigint,
  C_NAME VARCHAR(25),
  C_ADDRESS VARCHAR(40),
  C_NATIONKEY bigint,
  C_PHONE VARCHAR(15),
  C_ACCTBAL FLOAT(53),
  C_MKTSEGMENT VARCHAR(10),
  C_COMMENT VARCHAR(117),
  PRIMARY KEY (C_CUSTKEY)
);


CREATE TABLE part
(
  P_PARTKEY bigint,
  P_NAME VARCHAR(55),
  P_MFGR VARCHAR(25),
  P_BRAND VARCHAR(10),
  P_TYPE VARCHAR(25),
  P_SIZE bigint,
  P_CONTAINER VARCHAR(10),
  P_RETAILPRICE FLOAT(53),
  P_COMMENT VARCHAR(23),
  PRIMARY KEY (P_PARTKEY)
);


CREATE TABLE partsupp
(
  PS_PARTKEY bigint,
  PS_SUPPKEY bigint,
  PS_AVAILQTY bigint,
  PS_SUPPLYCOST FLOAT(53),
  PS_COMMENT VARCHAR(199),
  PRIMARY KEY (PS_PARTKEY, PS_SUPPKEY)
);

CREATE TABLE region
(
  R_REGIONKEY bigint,
  R_NAME VARCHAR(25),
  R_COMMENT VARCHAR(152),
  PRIMARY KEY (R_REGIONKEY)
);


CREATE TABLE supplier
(
  S_SUPPKEY bigint,
  S_NAME VARCHAR(25),
  S_ADDRESS VARCHAR(40),
  S_NATIONKEY bigint,
  S_PHONE VARCHAR(15),
  S_ACCTBAL FLOAT(53),
  S_COMMENT VARCHAR(101),
  PRIMARY KEY (S_SUPPKEY)
);

\COPY part FROM     '/Users/pengyuanli/Documents/Academics/provBenchs/tpchv3/dbgen/1gb/part.csv' WITH CSV DELIMITER '|';
\COPY supplier FROM '/Users/pengyuanli/Documents/Academics/provBenchs/tpchv3/dbgen/1gb/supplier.csv' WITH CSV DELIMITER '|';
\COPY partsupp FROM '/Users/pengyuanli/Documents/Academics/provBenchs/tpchv3/dbgen/1gb/partsupp.csv' WITH CSV DELIMITER '|';
\COPY customer FROM '/Users/pengyuanli/Documents/Academics/provBenchs/tpchv3/dbgen/1gb/customer.csv' WITH CSV DELIMITER '|';
\COPY orders FROM   '/Users/pengyuanli/Documents/Academics/provBenchs/tpchv3/dbgen/1gb/orders.csv' WITH CSV DELIMITER '|';
\COPY lineitem FROM '/Users/pengyuanli/Documents/Academics/provBenchs/tpchv3/dbgen/1gb/lineitem.csv' WITH CSV DELIMITER '|';
\COPY nation FROM   '/Users/pengyuanli/Documents/Academics/provBenchs/tpchv3/dbgen/1gb/nation.csv' WITH CSV DELIMITER '|';
\COPY region FROM   '/Users/pengyuanli/Documents/Academics/provBenchs/tpchv3/dbgen/1gb/region.csv' WITH CSV DELIMITER '|';

ALTER TABLE supplier ADD FOREIGN KEY (s_nationkey) REFERENCES nation (n_nationkey);

ALTER TABLE partsupp ADD FOREIGN KEY (ps_partkey) REFERENCES part (p_partkey);
ALTER TABLE partsupp ADD FOREIGN KEY (ps_suppkey) REFERENCES supplier (s_suppkey);

ALTER TABLE customer ADD FOREIGN KEY (c_nationkey) REFERENCES nation (n_nationkey);

ALTER TABLE orders ADD FOREIGN KEY (o_custkey) REFERENCES customer (c_custkey);

ALTER TABLE lineitem ADD FOREIGN KEY (l_partkey, l_suppkey) REFERENCES partsupp (ps_partkey, ps_suppkey);
ALTER TABLE lineitem ADD FOREIGN KEY (l_partkey) REFERENCES part (p_partkey);
ALTER TABLE lineitem ADD FOREIGN KEY (l_suppkey) REFERENCES supplier (s_suppkey);
ALTER TABLE lineitem ADD FOREIGN KEY (l_orderkey) REFERENCES orders (o_orderkey);

ALTER TABLE nation ADD FOREIGN KEY (n_regionkey) REFERENCES region (r_regionkey);

CREATE INDEX fkey_1 ON customer (c_nationkey);

CREATE INDEX fkey_2 ON lineitem (l_orderkey);
CREATE INDEX fkey_3 ON lineitem (l_partkey, l_suppkey);
CREATE INDEX fkey_4 ON lineitem (l_partkey);
CREATE INDEX fkey_5 ON lineitem (l_suppkey);

CREATE INDEX fkey_6 ON nation (n_regionkey);

CREATE INDEX fkey_7 ON orders (o_custkey);

CREATE INDEX fkey_8 ON partsupp (ps_partkey);
CREATE INDEX fkey_9 ON partsupp (ps_suppkey);

CREATE INDEX fkey_10 ON supplier (s_nationkey);


analyze;
