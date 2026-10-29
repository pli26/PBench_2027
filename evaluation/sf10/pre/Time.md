# Synthetic
## DB
```sql
SELECT pg_database_size(current_database()) AS size_bytes;
 size_bytes
-------------
 34221601419
 ```
## MULLER
```sql
\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/fp_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/fp_sqlprov.sql:1: NOTICE:  materialized view "fp_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.551 ms
SELECT 100000000
Time: 40770.789 ms (00:40.771)
CREATE INDEX
Time: 25936.116 ms (00:25.936)
CREATE INDEX
Time: 20617.793 ms (00:20.618)
CREATE INDEX
Time: 18506.093 ms (00:18.506)
CREATE INDEX
Time: 20886.431 ms (00:20.886)
CREATE INDEX
Time: 20527.182 ms (00:20.527)
CREATE INDEX
Time: 20655.958 ms (00:20.656)
CREATE INDEX
Time: 20011.084 ms (00:20.011)
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/fp_sqlprov.sql:10: NOTICE:  materialized view "fp_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.169 ms
SELECT 100000000
Time: 171952.705 ms (02:51.953)
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/fp_sqlprov.sql:21: NOTICE:  index "idx_fp_2_tuid" does not exist, skipping
DROP INDEX
Time: 373.536 ms
CREATE INDEX
Time: 24141.927 ms (00:24.142)



\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/dj1_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/dj1_sqlprov.sql:1: NOTICE:  materialized view "dj1_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.489 ms
SELECT 100000
Time: 80.742 ms
CREATE INDEX
Time: 16.167 ms
CREATE INDEX
Time: 28.198 ms
CREATE INDEX
Time: 25.257 ms
CREATE INDEX
Time: 25.267 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/dj1_sqlprov.sql:7: NOTICE:  materialized view "dj1_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.119 ms
SELECT 100000
Time: 116.622 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/dj1_sqlprov.sql:15: NOTICE:  index "idx_dj1_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.885 ms
CREATE INDEX
Time: 23.022 ms

\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/dj2_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/dj2_sqlprov.sql:1: NOTICE:  materialized view "dj2_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.492 ms
SELECT 100000
Time: 84.635 ms
CREATE INDEX
Time: 20.506 ms
CREATE INDEX
Time: 28.609 ms
CREATE INDEX
Time: 24.212 ms
CREATE INDEX
Time: 24.590 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/dj2_sqlprov.sql:7: NOTICE:  materialized view "dj2_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.104 ms
SELECT 100000
Time: 116.836 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/dj2_sqlprov.sql:15: NOTICE:  index "idx_dj2_2_tuid" does not exist, skipping
DROP INDEX
Time: 1.041 ms
CREATE INDEX
Time: 21.767 ms


\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/jc_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/jc_sqlprov.sql:1: NOTICE:  materialized view "jc_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.833 ms
SELECT 500000
Time: 240.560 ms
CREATE INDEX
Time: 103.300 ms
CREATE INDEX
Time: 92.328 ms
CREATE INDEX
Time: 95.792 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/jc_sqlprov.sql:6: NOTICE:  materialized view "jc_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.145 ms
SELECT 500000
Time: 495.495 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/jc_sqlprov.sql:13: NOTICE:  index "idx_jc_2_tuid" does not exist, skipping
DROP INDEX
Time: 7.505 ms
CREATE INDEX
Time: 79.265 ms



\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/js_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/js_sqlprov.sql:1: NOTICE:  materialized view "js_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.512 ms
SELECT 25000
Time: 36.778 ms
CREATE INDEX
Time: 16.805 ms
CREATE INDEX
Time: 10.503 ms
CREATE INDEX
Time: 8.544 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/js_sqlprov.sql:6: NOTICE:  materialized view "js_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.108 ms
SELECT 25000
Time: 28.378 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/js_sqlprov.sql:13: NOTICE:  index "idx_js_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.695 ms
CREATE INDEX
Time: 4.266 ms

\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/jj_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/jj_sqlprov.sql:1: NOTICE:  materialized view "jj_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.646 ms
SELECT 10000
Time: 21.750 ms
CREATE INDEX
Time: 7.648 ms
CREATE INDEX
Time: 5.723 ms
CREATE INDEX
Time: 5.528 ms
CREATE INDEX
Time: 4.681 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/jj_sqlprov.sql:7: NOTICE:  materialized view "jj_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.150 ms
SELECT 10000
Time: 22.513 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/jj_sqlprov.sql:15: NOTICE:  index "idx_jj_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.205 ms
CREATE INDEX
Time: 4.546 ms


\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/jjj_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/jjj_sqlprov.sql:1: NOTICE:  materialized view "jjj_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.536 ms
SELECT 10000
Time: 22.586 ms
CREATE INDEX
Time: 8.159 ms
CREATE INDEX
Time: 6.080 ms
CREATE INDEX
Time: 5.336 ms
CREATE INDEX
Time: 8.598 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/jjj_sqlprov.sql:7: NOTICE:  materialized view "jjj_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.154 ms
SELECT 10000
Time: 20.150 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/jjj_sqlprov.sql:15: NOTICE:  index "idx_jjj_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.220 ms
CREATE INDEX
Time: 2.623 ms


\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgn100_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgn100_sqlprov.sql:1: NOTICE:  materialized view "vpgn100_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.468 ms
SELECT 1000000
Time: 441.959 ms
CREATE INDEX
Time: 212.278 ms
CREATE INDEX
Time: 204.217 ms
CREATE INDEX
Time: 198.724 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgn100_sqlprov.sql:6: NOTICE:  materialized view "vpgn100_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.136 ms
SELECT 1000000
Time: 1000.151 ms (00:01.000)
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgn100_sqlprov.sql:13: NOTICE:  index "idx_vpgn100_2_tuid" does not exist, skipping
DROP INDEX
Time: 21.320 ms
CREATE INDEX
Time: 198.374 ms


\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgn1k_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgn1k_sqlprov.sql:1: NOTICE:  materialized view "vpgn1k_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.482 ms
SELECT 10000000
Time: 3909.044 ms (00:03.909)
CREATE INDEX
Time: 2002.823 ms (00:02.003)
CREATE INDEX
Time: 1908.837 ms (00:01.909)
CREATE INDEX
Time: 1928.928 ms (00:01.929)
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgn1k_sqlprov.sql:6: NOTICE:  materialized view "vpgn1k_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.131 ms
SELECT 10000000
Time: 9836.518 ms (00:09.837)
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgn1k_sqlprov.sql:13: NOTICE:  index "idx_vpgn1k_2_tuid" does not exist, skipping
DROP INDEX
Time: 190.102 ms
CREATE INDEX
Time: 1508.852 ms (00:01.509)

\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgn10k_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgn10k_sqlprov.sql:1: NOTICE:  materialized view "vpgn10k_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.536 ms
SELECT 100000000
Time: 37799.428 ms (00:37.799)
CREATE INDEX
Time: 21639.673 ms (00:21.640)
CREATE INDEX
Time: 20689.576 ms (00:20.690)
CREATE INDEX
Time: 20874.003 ms (00:20.874)
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgn10k_sqlprov.sql:6: NOTICE:  materialized view "vpgn10k_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.164 ms
SELECT 100000000
Time: 98441.026 ms (01:38.441)
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgn10k_sqlprov.sql:13: NOTICE:  index "idx_vpgn10k_2_tuid" does not exist, skipping
DROP INDEX
Time: 367.226 ms
CREATE INDEX
Time: 25559.526 ms (00:25.560)

\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgs100_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgs100_sqlprov.sql:1: NOTICE:  materialized view "vpgs100_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 1.007 ms
SELECT 1000000
Time: 489.468 ms
CREATE INDEX
Time: 193.037 ms
CREATE INDEX
Time: 177.046 ms
CREATE INDEX
Time: 178.160 ms
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgs100_sqlprov.sql:6: NOTICE:  materialized view "vpgs100_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.154 ms
SELECT 1000000
Time: 1008.497 ms (00:01.008)
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgs100_sqlprov.sql:13: NOTICE:  index "idx_vpgs100_2_tuid" does not exist, skipping
DROP INDEX
Time: 23.819 ms
CREATE INDEX
Time: 149.960 ms

\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgs1k_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgs1k_sqlprov.sql:1: NOTICE:  materialized view "vpgs1k_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.502 ms
SELECT 10000000
Time: 3911.741 ms (00:03.912)
CREATE INDEX
Time: 1965.156 ms (00:01.965)
CREATE INDEX
Time: 1825.762 ms (00:01.826)
CREATE INDEX
Time: 1779.278 ms (00:01.779)
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgs1k_sqlprov.sql:6: NOTICE:  materialized view "vpgs1k_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.137 ms
SELECT 10000000
Time: 9912.569 ms (00:09.913)
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgs1k_sqlprov.sql:13: NOTICE:  index "idx_vpgs1k_2_tuid" does not exist, skipping
DROP INDEX
Time: 207.196 ms
CREATE INDEX
Time: 1700.839 ms (00:01.701)

\i /Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgs10k_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgs10k_sqlprov.sql:1: NOTICE:  materialized view "vpgs10k_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.538 ms
SELECT 100000000
Time: 38227.346 ms (00:38.227)
CREATE INDEX
Time: 23141.277 ms (00:23.141)
CREATE INDEX
Time: 22034.824 ms (00:22.035)
CREATE INDEX
Time: 21372.183 ms (00:21.372)
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgs10k_sqlprov.sql:6: NOTICE:  materialized view "vpgs10k_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.187 ms
SELECT 100000000
Time: 99271.434 ms (01:39.271)
psql:/Users/uicdbgroup/pengyuan/exp/pbench/performance/GenData/data/sf10/vpgs10k_sqlprov.sql:13: NOTICE:  index "idx_vpgs10k_2_tuid" does not exist, skipping
DROP INDEX
Time: 579.392 ms
CREATE INDEX
Time: 21388.325 ms (00:21.388)


NOTICE:  materialized view "fp1_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.510 ms
SELECT 10000
Time: 25.417 ms
CREATE INDEX
Time: 6.229 ms
CREATE INDEX
Time: 5.424 ms
CREATE INDEX
Time: 7.709 ms
CREATE INDEX
Time: 3.246 ms
CREATE INDEX
Time: 4.129 ms
CREATE INDEX
Time: 2.820 ms
CREATE INDEX
Time: 3.468 ms
NOTICE:  materialized view "fp1_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.115 ms
SELECT 10000
Time: 25.639 ms
NOTICE:  index "idx_fp_1_tuid" does not exist, skipping
DROP INDEX
Time: 0.463 ms
CREATE INDEX
Time: 2.252 ms


NOTICE:  materialized view "fp2_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.488 ms
SELECT 1000000
Time: 491.103 ms
CREATE INDEX
Time: 136.250 ms
CREATE INDEX
Time: 114.618 ms
CREATE INDEX
Time: 160.894 ms
CREATE INDEX
Time: 120.504 ms
CREATE INDEX
Time: 119.473 ms
CREATE INDEX
Time: 121.979 ms
CREATE INDEX
Time: 122.353 ms
NOTICE:  materialized view "fp2_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.122 ms
SELECT 1000000
Time: 1788.009 ms (00:01.788)
DROP INDEX
Time: 1081.923 ms (00:01.082)
CREATE INDEX
Time: 181.924 ms

DROP MATERIALIZED VIEW
Time: 0.568 ms
SELECT 20000000
Time: 8802.864 ms (00:08.803)
CREATE INDEX
Time: 2805.699 ms (00:02.806)
CREATE INDEX
Time: 1946.614 ms (00:01.947)
CREATE INDEX
Time: 2933.725 ms (00:02.934)
CREATE INDEX
Time: 2005.744 ms (00:02.006)
CREATE INDEX
Time: 1996.854 ms (00:01.997)
CREATE INDEX
Time: 1991.704 ms (00:01.992)
CREATE INDEX
Time: 2011.583 ms (00:02.012)
NOTICE:  materialized view "fp3_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.127 ms
ERROR:  integer out of range
Time: 22835.702 ms (00:22.836)
NOTICE:  index "idx_fp_3_tuid" does not exist, skipping
DROP INDEX
Time: 0.219 ms
CREATE INDEX
Time: 2485.304 ms (00:02.485)

```

### DB SIZE:
```sql

select pg_database_size('pp');
 pg_database_size
------------------
     124926276235
(1 row)

Time: 11.655 ms
```

## ProvSQL
### DB BEFORE
```sql
pg_database_size
------------------
      34220262071
```

### add_provenance
```sql
select add_provenance('dj1');
 add_provenance
----------------

(1 row)

Time: 938.845 ms

select add_provenance('dj2');
 add_provenance
----------------

(1 row)

Time: 940.045 ms

select add_provenance('jc');
 add_provenance
----------------

(1 row)

Time: 3747.466 ms (00:03.747)
select add_provenance('js');
 add_provenance
----------------

(1 row)

Time: 192.928 ms



select add_provenance('jj');
 add_provenance
----------------

(1 row)

Time: 127.093 ms
select add_provenance('jjj');
 add_provenance
----------------

(1 row)

Time: 128.732 ms

select add_provenance('vpgn100');
 add_provenance
----------------

(1 row)

Time: 6975.533 ms (00:06.976)
select add_provenance('vpgs100');
 add_provenance
----------------

(1 row)

Time: 9420.902 ms (00:09.421)


select add_provenance('vpgn1k');
 add_provenance
----------------

(1 row)

Time: 74778.617 ms (01:14.779)
select add_provenance('vpgs1k');
 add_provenance
----------------

(1 row)

Time: 107917.461 ms (01:47.917)



select add_provenance('vpgn10k');
 add_provenance
----------------

(1 row)

Time: 811343.929 ms (13:31.344)


elect add_provenance('vpgs10k');
 add_provenance
----------------

(1 row)

Time: 962840.452 ms (16:02.840)

select add_provenance('fp');
 add_provenance
----------------

(1 row)

Time: 3040743.657 ms (50:40.744)
select add_provenance('fp1');
 add_provenance
----------------

(1 row)

Time: 60.094 ms
select add_provenance('fp2');
 add_provenance
----------------

(1 row)

Time: 1581.470 ms (00:01.581)
select add_provenance('fp3');
 add_provenance
----------------

(1 row)

Time: 30145.290 ms (00:30.145)

```

### db after:
```sql
pg_database_size
------------------
      87282840203
```

# TPCH

## DB
```sql
select pg_database_size('sizetpch');
 pg_database_size
------------------
      17060389391
(1 row)
```

## Muller
```sql
psql:/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/SQLProv_TPCH_Setup.sql:7: NOTICE:  sequence "prov_ids" does not exist, skipping
DROP SEQUENCE
Time: 0.172 ms
CREATE SEQUENCE
Time: 1.837 ms
SELECT 5
Time: 4.610 ms
SELECT 25
Time: 2.496 ms
SELECT 2000000
Time: 1395.721 ms (00:01.396)
SELECT 100000
Time: 115.893 ms
SELECT 8000000
Time: 4316.913 ms (00:04.317)
SELECT 1500000
Time: 1233.184 ms (00:01.233)
SELECT 15000000
Time: 8913.082 ms (00:08.913)
SELECT 59986052
Time: 40662.334 ms (00:40.662)
CREATE INDEX
Time: 6.178 ms
CREATE INDEX
Time: 1.692 ms
CREATE INDEX
Time: 331.987 ms
CREATE INDEX
Time: 28.111 ms
CREATE INDEX
Time: 1774.722 ms (00:01.775)
CREATE INDEX
Time: 267.158 ms
CREATE INDEX
Time: 3062.942 ms (00:03.063)
CREATE INDEX
Time: 12379.051 ms (00:12.379)
psql:/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/SQLProv_TPCH_Setup.sql:48: NOTICE:  index "nation_fkey_region_1" does not exist, skipping
DROP INDEX
Time: 0.233 ms
psql:/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/SQLProv_TPCH_Setup.sql:49: NOTICE:  index "supplier_fkey_nation_1" does not exist, skipping
DROP INDEX
Time: 0.200 ms
psql:/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/SQLProv_TPCH_Setup.sql:50: NOTICE:  index "partsupp_fkey_part_1" does not exist, skipping
DROP INDEX
Time: 0.135 ms
psql:/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/SQLProv_TPCH_Setup.sql:51: NOTICE:  index "partsupp_fkey_supplier_1" does not exist, skipping
DROP INDEX
Time: 0.137 ms
psql:/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/SQLProv_TPCH_Setup.sql:52: NOTICE:  index "customer_fkey_nation_1" does not exist, skipping
DROP INDEX
Time: 0.135 ms
psql:/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/SQLProv_TPCH_Setup.sql:53: NOTICE:  index "orders_fkey_customer_1" does not exist, skipping
DROP INDEX
Time: 0.143 ms
psql:/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/SQLProv_TPCH_Setup.sql:54: NOTICE:  index "lineitem_fkey_partsupp_1" does not exist, skipping
DROP INDEX
Time: 0.133 ms
psql:/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/SQLProv_TPCH_Setup.sql:55: NOTICE:  index "lineitem_fkey_orders_1" does not exist, skipping
DROP INDEX
Time: 0.153 ms
CREATE INDEX
Time: 1.353 ms
CREATE INDEX
Time: 44.630 ms
CREATE INDEX
Time: 2116.124 ms (00:02.116)
CREATE INDEX
Time: 1267.225 ms (00:01.267)
CREATE INDEX
Time: 1370.423 ms (00:01.370)
CREATE INDEX
Time: 2502.414 ms (00:02.502)
CREATE INDEX
Time: 14025.496 ms (00:14.025)
CREATE INDEX
Time: 8393.005 ms (00:08.393)
SELECT 5
Time: 1.006 ms
SELECT 25
Time: 4.000 ms
SELECT 2000000
Time: 3813.554 ms (00:03.814)
SELECT 100000
Time: 234.713 ms
SELECT 8000000
Time: 9512.424 ms (00:09.512)
SELECT 1500000
Time: 2635.680 ms (00:02.636)
SELECT 15000000
Time: 28648.311 ms (00:28.648)
SELECT 59986052
Time: 192788.690 ms (03:12.789)
CREATE INDEX
Time: 160.417 ms
CREATE INDEX
Time: 0.612 ms
CREATE INDEX
Time: 2547.897 ms (00:02.548)
CREATE INDEX
Time: 47.525 ms
CREATE INDEX
Time: 6270.784 ms (00:06.271)
CREATE INDEX
Time: 553.806 ms
CREATE INDEX
Time: 7483.765 ms (00:07.484)
CREATE INDEX
Time: 28725.641 ms (00:28.726)
```

### Size After
```sql
 after_size
-------------
 69968343691
 ```
## ProvSQL
```sql
Time: 8.587 ms
          before_time
-------------------------------
 2026-10-27 11:25:50.475245-05
(1 row)

Time: 0.360 ms
 add_provenance
----------------

(1 row)

Time: 7199.725 ms (00:07.200)
 add_provenance
----------------

(1 row)

Time: 633972.142 ms (10:33.972)
 add_provenance
----------------

(1 row)

Time: 94722.965 ms (01:34.723)
 add_provenance
----------------

(1 row)

Time: 5940.097 ms (00:05.940)
 add_provenance
----------------

(1 row)

Time: 52718.517 ms (00:52.719)
 add_provenance
----------------

(1 row)

Time: 0.951 ms
 add_provenance
----------------

(1 row)

Time: 0.699 ms
 add_provenance
----------------

(1 row)

Time: 479.777 ms
          after_time
-------------------------------
 2026-10-27 11:39:05.433016-05
(1 row)

Time: 0.178 ms
 after_size
-------------
 38878098059
(1 row)
```
### Size After
```sql
 ```

