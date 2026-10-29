# database size before any provsql or sqlprov:

p1=# select pg_database_size('p1');
 pg_database_size
------------------
       3447534051
(1 row)

# provsql
## synthetic
### before add provenance, Size
```
-rw-------    1 uicdbgroup  staff    65552 Mar 27 21:09 provsql_extra.mmap
-rw-------    1 uicdbgroup  staff  3145744 Mar 27 21:09 provsql_gates.mmap
-rw-------    1 uicdbgroup  staff  1572888 Mar 27 21:09 provsql_mapping.mmap
-rw-------    1 uicdbgroup  staff  1048592 Mar 27 21:09 provsql_wires.mmap
```

### add provenance for tables
dj1: 88.523 ms
dj2: 75.651 ms
fp: 40226.581 ms
jc: 257.847
jj: 90.743 ms
jjj: 93.809 ms
js: 152.364
vpgn100: 467.946
vpgn1k: 3372.322
vpgn10k: 33145.834
vpgs100: 403.098
vpgs1k: 3491.393
vpgs10k: 32917.426
fp1: 17.881
fp2: 408.579
fp3: 6822.457

### after add provenance, size:
```
-rw-------    1 uicdbgroup  staff       65552 Mar 27 21:09 provsql_extra.mmap
-rw-------    1 uicdbgroup  staff  3221225488 Mar 27 21:25 provsql_gates.mmap
-rw-------    1 uicdbgroup  staff  3221225496 Mar 27 21:25 provsql_mapping.mmap
-rw-------    1 uicdbgroup  staff     1048592 Mar 27 21:09 provsql_wires.mmap
```

### DB After:
```
5768548835
```

## TPCH
### Before Size
```
2266862051
```

### adding prov column:
customer: 692.226 ms
lineiterm:26755.955 ms
nation: 13.275 ms
orders: 5403.817 ms
part: 890.701 ms
partsupp: 3337.658 ms
region:12.022 ms
supplier: 94.442 ms

### DBAfter:
```
2681618959
```
# sqlprov
## Synthetic
### before:
```
3451949539
```
### adding provnance tables:
```
mullstorage=# \i /Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/dj1_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/dj1_sqlprov.sql:1: NOTICE:  materialized view "dj1_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.370 ms
SELECT 10000
Time: 20.804 ms
CREATE INDEX
Time: 4.853 ms
CREATE INDEX
Time: 7.388 ms
CREATE INDEX
Time: 5.868 ms
CREATE INDEX
Time: 5.111 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/dj1_sqlprov.sql:7: NOTICE:  materialized view "dj1_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.133 ms
SELECT 10000
Time: 21.232 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/dj1_sqlprov.sql:15: NOTICE:  index "idx_dj1_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.274 ms
CREATE INDEX
Time: 2.676 ms
```

```
mullstorage=# \i /Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/dj2_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/dj2_sqlprov.sql:1: NOTICE:  materialized view "dj2_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.543 ms
SELECT 10000
Time: 21.636 ms
CREATE INDEX
Time: 5.586 ms
CREATE INDEX
Time: 6.616 ms
CREATE INDEX
Time: 5.152 ms
CREATE INDEX
Time: 4.508 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/dj2_sqlprov.sql:7: NOTICE:  materialized view "dj2_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.144 ms
SELECT 10000
Time: 21.172 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/dj2_sqlprov.sql:15: NOTICE:  index "idx_dj2_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.293 ms
CREATE INDEX
Time: 2.517 ms
```

```
mullstorage=# \i /Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/fp_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/fp_sqlprov.sql:1: NOTICE:  materialized view "fp_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.641 ms
SELECT 10000000
Time: 4166.233 ms (00:04.166)
CREATE INDEX
Time: 2244.508 ms (00:02.245)
CREATE INDEX
Time: 1823.458 ms (00:01.823)
CREATE INDEX
Time: 1599.499 ms (00:01.599)
CREATE INDEX
Time: 1827.809 ms (00:01.828)
CREATE INDEX
Time: 1835.377 ms (00:01.835)
CREATE INDEX
Time: 1843.742 ms (00:01.844)
CREATE INDEX
Time: 1851.880 ms (00:01.852)
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/fp_sqlprov.sql:10: NOTICE:  materialized view "fp_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.141 ms
SELECT 10000000
Time: 17448.020 ms (00:17.448)
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/fp_sqlprov.sql:21: NOTICE:  index "idx_fp_2_tuid" does not exist, skipping
DROP INDEX
Time: 205.495 ms
CREATE INDEX
Time: 1711.512 ms (00:01.712)
```

- JC
  ```
  mullstorage=# \i /Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/jc_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/jc_sqlprov.sql:1: NOTICE:  materialized view "jc_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.706 ms
SELECT 50000
Time: 57.260 ms
CREATE INDEX
Time: 19.578 ms
CREATE INDEX
Time: 11.957 ms
CREATE INDEX
Time: 11.903 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/jc_sqlprov.sql:6: NOTICE:  materialized view "jc_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.103 ms
SELECT 50000
Time: 48.276 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/jc_sqlprov.sql:13: NOTICE:  index "idx_jc_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.275 ms
CREATE INDEX
Time: 7.315 ms
```

- jj
```
mullstorage=# \i /Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/jj_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/jj_sqlprov.sql:1: NOTICE:  drop cascades to materialized view jj_2
DROP MATERIALIZED VIEW
Time: 18.266 ms
SELECT 10000
Time: 12.563 ms
CREATE INDEX
Time: 6.231 ms
CREATE INDEX
Time: 4.503 ms
CREATE INDEX
Time: 4.571 ms
CREATE INDEX
Time: 4.149 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/jj_sqlprov.sql:7: NOTICE:  materialized view "jj_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.144 ms
SELECT 10000
Time: 19.758 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/jj_sqlprov.sql:15: NOTICE:  index "idx_jj_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.261 ms
CREATE INDEX
Time: 2.431 ms
```
- jjj
```
mullstorage=# \i /Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/jjj_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/jjj_sqlprov.sql:1: NOTICE:  materialized view "jjj_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.702 ms
SELECT 10000
Time: 20.388 ms
CREATE INDEX
Time: 7.527 ms
CREATE INDEX
Time: 5.628 ms
CREATE INDEX
Time: 4.979 ms
CREATE INDEX
Time: 4.608 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/jjj_sqlprov.sql:7: NOTICE:  materialized view "jjj_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.142 ms
SELECT 10000
Time: 21.373 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/jjj_sqlprov.sql:15: NOTICE:  index "idx_jjj_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.261 ms
CREATE INDEX
Time: 2.548 ms
```
- js
```
mullstorage=# \i /Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/js_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/js_sqlprov.sql:1: NOTICE:  materialized view "js_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.584 ms
SELECT 25000
Time: 35.894 ms
CREATE INDEX
Time: 11.960 ms
CREATE INDEX
Time: 9.108 ms
CREATE INDEX
Time: 7.749 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/js_sqlprov.sql:6: NOTICE:  materialized view "js_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.118 ms
SELECT 25000
Time: 30.238 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/js_sqlprov.sql:13: NOTICE:  index "idx_js_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.488 ms
CREATE INDEX
Time: 4.431 ms
```

- vpgn100
```psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgn100_sqlprov.sql:1: NOTICE:  materialized view "vpgn100_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.490 ms
SELECT 100000
Time: 83.291 ms
CREATE INDEX
Time: 30.009 ms
CREATE INDEX
Time: 25.823 ms
CREATE INDEX
Time: 25.894 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgn100_sqlprov.sql:6: NOTICE:  materialized view "vpgn100_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.131 ms
SELECT 100000
Time: 96.853 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgn100_sqlprov.sql:13: NOTICE:  index "idx_vpgn100_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.251 ms
CREATE INDEX
Time: 16.555 mst
```

- vpgn1k
```
mullstorage=# \i /Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgn1k_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgn1k_sqlprov.sql:1: NOTICE:  materialized view "vpgn1k_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.668 ms
SELECT 1000000
Time: 447.447 ms
CREATE INDEX
Time: 178.307 ms
CREATE INDEX
Time: 160.228 ms
CREATE INDEX
Time: 159.413 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgn1k_sqlprov.sql:6: NOTICE:  materialized view "vpgn1k_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.154 ms
SELECT 1000000
Time: 987.121 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgn1k_sqlprov.sql:13: NOTICE:  index "idx_vpgn1k_2_tuid" does not exist, skipping
DROP INDEX
Time: 17.534 ms
CREATE INDEX
Time: 138.811 ms
```

- vpgn10k
```
mullstorage=# \i /Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgn10k_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgn10k_sqlprov.sql:1: NOTICE:  materialized view "vpgn10k_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.544 ms
SELECT 10000000
Time: 3898.893 ms (00:03.899)
CREATE INDEX
Time: 1871.854 ms (00:01.872)
CREATE INDEX
Time: 1710.114 ms (00:01.710)
CREATE INDEX
Time: 1731.836 ms (00:01.732)
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgn10k_sqlprov.sql:6: NOTICE:  materialized view "vpgn10k_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.136 ms
SELECT 10000000
Time: 9874.236 ms (00:09.874)
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgn10k_sqlprov.sql:13: NOTICE:  index "idx_vpgn10k_2_tuid" does not exist, skipping
DROP INDEX
Time: 146.250 ms
CREATE INDEX
Time: 1669.281 ms (00:01.669)
```

- vpgs100
```
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgs100_sqlprov.sql:1: NOTICE:  materialized view "vpgs100_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.536 ms
SELECT 100000
Time: 83.835 ms
CREATE INDEX
Time: 26.509 ms
CREATE INDEX
Time: 23.347 ms
CREATE INDEX
Time: 23.292 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgs100_sqlprov.sql:6: NOTICE:  materialized view "vpgs100_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.105 ms
SELECT 100000
Time: 97.318 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgs100_sqlprov.sql:13: NOTICE:  index "idx_vpgs100_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.291 ms
CREATE INDEX
Time: 19.830 ms
```

- vpgs1k
```
mullstorage=# \i /Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgs1k_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgs1k_sqlprov.sql:1: NOTICE:  materialized view "vpgs1k_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.576 ms
SELECT 1000000
Time: 440.814 ms
CREATE INDEX
Time: 187.864 ms
CREATE INDEX
Time: 180.765 ms
CREATE INDEX
Time: 184.714 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgs1k_sqlprov.sql:6: NOTICE:  materialized view "vpgs1k_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.129 ms
SELECT 1000000
Time: 993.109 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgs1k_sqlprov.sql:13: NOTICE:  index "idx_vpgs1k_2_tuid" does not exist, skipping
DROP INDEX
Time: 19.835 ms
CREATE INDEX
Time: 147.131 ms
```

- vpgs10k
```
mullstorage=# \i /Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgs10k_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgs10k_sqlprov.sql:1: NOTICE:  materialized view "vpgs10k_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.503 ms
SELECT 10000000
Time: 3937.356 ms (00:03.937)
CREATE INDEX
Time: 1977.086 ms (00:01.977)
CREATE INDEX
Time: 1857.451 ms (00:01.857)
CREATE INDEX
Time: 1857.465 ms (00:01.857)
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgs10k_sqlprov.sql:6: NOTICE:  materialized view "vpgs10k_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.128 ms
SELECT 10000000
Time: 9802.949 ms (00:09.803)
psql:/Users/uicdbgroup/pengyuan/exp/sf1/GenData/data/sf1/vpgs10k_sqlprov.sql:13: NOTICE:  index "idx_vpgs10k_2_tuid" does not exist, skipping
DROP INDEX
Time: 194.846 ms
CREATE INDEX
Time: 1676.054 ms (00:01.676)
```

- fp1
```
NOTICE:  materialized view "fp1_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 1.294 ms
SELECT 1000
Time: 4647.841 ms (00:04.648)
CREATE INDEX
Time: 0.972 ms
CREATE INDEX
Time: 0.486 ms
CREATE INDEX
Time: 0.479 ms
CREATE INDEX
Time: 0.455 ms
CREATE INDEX
Time: 0.437 ms
CREATE INDEX
Time: 0.434 ms
CREATE INDEX
Time: 0.458 ms
CREATE INDEX
Time: 0.472 ms
NOTICE:  materialized view "fp1_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.121 ms
SELECT 1000
Time: 2.655 ms
NOTICE:  index "idx_fp1_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.157 ms
CREATE INDEX
Time: 0.494 ms
```

- fp2
```
NOTICE:  materialized view "fp2_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.676 ms
SELECT 100000
Time: 4483.820 ms (00:04.484)
CREATE INDEX
Time: 21.081 ms
CREATE INDEX
Time: 11.253 ms
CREATE INDEX
Time: 11.363 ms
CREATE INDEX
Time: 17.515 ms
CREATE INDEX
Time: 11.493 ms
CREATE INDEX
Time: 11.652 ms
CREATE INDEX
Time: 11.821 ms
CREATE INDEX
Time: 11.956 ms
NOTICE:  materialized view "fp2_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.112 ms
SELECT 100000
Time: 173.124 ms
NOTICE:  index "idx_fp2_2_tuid" does not exist, skipping
DROP INDEX
Time: 2.312 ms
CREATE INDEX
Time: 27.570 ms
```

- fp3
```
NOTICE:  materialized view "fp3_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.638 ms
SELECT 2000000
Time: 5131.706 ms (00:05.132)
CREATE INDEX
Time: 337.018 ms
CREATE INDEX
Time: 210.226 ms
CREATE INDEX
Time: 205.740 ms
CREATE INDEX
Time: 309.359 ms
CREATE INDEX
Time: 212.294 ms
CREATE INDEX
Time: 213.150 ms
CREATE INDEX
Time: 224.196 ms
CREATE INDEX
Time: 215.671 ms
NOTICE:  materialized view "fp3_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.127 ms
SELECT 2000000
Time: 3464.691 ms (00:03.465)
NOTICE:  index "idx_fp3_2_tuid" does not exist, skipping
DROP INDEX
Time: 67.449 ms
CREATE INDEX
Time: 372.389 ms
```

- rcr (pairs)
```
NOTICE:  table "pairs_1" does not exist, skipping
DROP TABLE
Time: 0.365 ms
SELECT 100000
Time: 81.995 ms

Time: 0.660 ms
SELECT 100000
Time: 108.807 ms
ALTER TABLE
Time: 24.909 ms
```

### Size after added tables:
```
13325521379
```
## TPCH
### before:
```
2266862051
```

### adding:
```
DROP SEQUENCE
Time: 0.914 ms
CREATE SEQUENCE
Time: 2.732 ms
SELECT 5
Time: 4.082 ms
SELECT 25
Time: 2.427 ms
SELECT 200000
Time: 185.056 ms
SELECT 10000
Time: 10.453 ms
SELECT 800000
Time: 463.993 ms
SELECT 150000
Time: 123.437 ms
SELECT 1500000
Time: 929.420 ms
SELECT 6001215
Time: 4407.959 ms (00:04.408)
CREATE INDEX
Time: 0.686 ms
CREATE INDEX
Time: 0.379 ms
CREATE INDEX
Time: 47.284 ms
CREATE INDEX
Time: 2.172 ms
CREATE INDEX
Time: 227.920 ms
CREATE INDEX
Time: 41.630 ms
CREATE INDEX
Time: 311.456 ms
CREATE INDEX
Time: 1576.996 ms (00:01.577)
psql:/Users/uicdbgroup/pengyuan/exp/sqlprov/tpch-set-up.sql:42: NOTICE:  index "nation_fkey_region_1" does not exist, skipping
DROP INDEX
Time: 0.147 ms
psql:/Users/uicdbgroup/pengyuan/exp/sqlprov/tpch-set-up.sql:43: NOTICE:  index "supplier_fkey_nation_1" does not exist, skipping
DROP INDEX
Time: 0.113 ms
psql:/Users/uicdbgroup/pengyuan/exp/sqlprov/tpch-set-up.sql:44: NOTICE:  index "partsupp_fkey_part_1" does not exist, skipping
DROP INDEX
Time: 0.104 ms
psql:/Users/uicdbgroup/pengyuan/exp/sqlprov/tpch-set-up.sql:45: NOTICE:  index "partsupp_fkey_supplier_1" does not exist, skipping
DROP INDEX
Time: 0.088 ms
psql:/Users/uicdbgroup/pengyuan/exp/sqlprov/tpch-set-up.sql:46: NOTICE:  index "customer_fkey_nation_1" does not exist, skipping
DROP INDEX
Time: 0.086 ms
psql:/Users/uicdbgroup/pengyuan/exp/sqlprov/tpch-set-up.sql:47: NOTICE:  index "orders_fkey_customer_1" does not exist, skipping
DROP INDEX
Time: 0.076 ms
psql:/Users/uicdbgroup/pengyuan/exp/sqlprov/tpch-set-up.sql:48: NOTICE:  index "lineitem_fkey_partsupp_1" does not exist, skipping
DROP INDEX
Time: 0.085 ms
psql:/Users/uicdbgroup/pengyuan/exp/sqlprov/tpch-set-up.sql:49: NOTICE:  index "lineitem_fkey_orders_1" does not exist, skipping
DROP INDEX
Time: 0.080 ms
CREATE INDEX
Time: 0.403 ms
CREATE INDEX
Time: 5.117 ms
CREATE INDEX
Time: 192.981 ms
CREATE INDEX
Time: 251.533 ms
CREATE INDEX
Time: 88.768 ms
CREATE INDEX
Time: 430.141 ms
CREATE INDEX
Time: 2663.626 ms (00:02.664)
CREATE INDEX
Time: 1251.571 ms (00:01.252)
SELECT 5
Time: 0.996 ms
SELECT 25
Time: 0.703 ms
SELECT 200000
Time: 389.070 ms
SELECT 10000
Time: 21.909 ms
SELECT 800000
Time: 957.137 ms
SELECT 150000
Time: 282.694 ms
SELECT 1500000
Time: 2890.896 ms (00:02.891)
SELECT 6001215
Time: 19452.322 ms (00:19.452)
CREATE INDEX
Time: 346.529 ms
CREATE INDEX
Time: 0.762 ms
CREATE INDEX
Time: 39.497 ms
CREATE INDEX
Time: 1.928 ms
CREATE INDEX
Time: 124.926 ms
CREATE INDEX
Time: 30.983 ms
CREATE INDEX
Time: 247.274 ms
CREATE INDEX
Time: 1352.673 ms (00:01.353)
```

### after:
```
7867933199
```


# SF01
total size:         353513955

## sqlprov


```
DROP MATERIALIZED VIEW
Time: 11.062 ms
SELECT 1000
Time: 3.420 ms
CREATE INDEX
Time: 1.679 ms
CREATE INDEX
Time: 1.246 ms
CREATE INDEX
Time: 1.271 ms
CREATE INDEX
Time: 1.200 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/dj1_sqlprov.sql:7: NOTICE:  materialized view "dj1_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.092 ms
SELECT 1000
Time: 5.094 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/dj1_sqlprov.sql:15: NOTICE:  index "idx_dj1_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.176 ms
CREATE INDEX
Time: 1.510 ms


DROP MATERIALIZED VIEW
Time: 11.411 ms
SELECT 1000
Time: 3.928 ms
CREATE INDEX
Time: 1.669 ms
CREATE INDEX
Time: 1.352 ms
CREATE INDEX
Time: 1.280 ms
CREATE INDEX
Time: 1.192 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/dj2_sqlprov.sql:7: NOTICE:  materialized view "dj2_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.103 ms
SELECT 1000
Time: 5.906 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/dj2_sqlprov.sql:15: NOTICE:  index "idx_dj2_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.383 ms
CREATE INDEX
Time: 1.501 ms


DROP MATERIALIZED VIEW
Time: 35.054 ms
SELECT 1000000
Time: 450.151 ms
CREATE INDEX
Time: 124.065 ms
CREATE INDEX
Time: 190.269 ms
CREATE INDEX
Time: 165.741 ms
CREATE INDEX
Time: 190.777 ms
CREATE INDEX
Time: 193.255 ms
CREATE INDEX
Time: 190.986 ms
CREATE INDEX
Time: 191.159 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/fp_sqlprov.sql:10: NOTICE:  materialized view "fp_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.156 ms
SELECT 1000000
Time: 1721.626 ms (00:01.722)
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/fp_sqlprov.sql:21: NOTICE:  index "idx_fp_2_tuid" does not exist, skipping
DROP INDEX
Time: 36.154 ms
CREATE INDEX
Time: 151.021 ms

g10=# \i /Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/jc_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/jc_sqlprov.sql:1: NOTICE:  materialized view "jc_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.529 ms
SELECT 50000
Time: 54.207 ms
CREATE INDEX
Time: 17.094 ms
CREATE INDEX
Time: 12.729 ms
CREATE INDEX
Time: 12.201 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/jc_sqlprov.sql:6: NOTICE:  materialized view "jc_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.124 ms
SELECT 50000
Time: 48.657 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/jc_sqlprov.sql:13: NOTICE:  index "idx_jc_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.279 ms
CREATE INDEX
Time: 7.622 ms

g10=# \i /Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/jj_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/jj_sqlprov.sql:1: NOTICE:  materialized view "jj_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 1.069 ms
SELECT 10000
Time: 21.253 ms
CREATE INDEX
Time: 7.231 ms
CREATE INDEX
Time: 6.339 ms
CREATE INDEX
Time: 5.300 ms
CREATE INDEX
Time: 4.633 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/jj_sqlprov.sql:7: NOTICE:  materialized view "jj_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.145 ms
SELECT 10000
Time: 21.348 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/jj_sqlprov.sql:15: NOTICE:  index "idx_jj_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.254 ms
CREATE INDEX
Time: 2.471 ms

g10=# \i /Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/jjj_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/jjj_sqlprov.sql:1: NOTICE:  materialized view "jjj_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.465 ms
SELECT 10000
Time: 19.277 ms
CREATE INDEX
Time: 6.909 ms
CREATE INDEX
Time: 5.829 ms
CREATE INDEX
Time: 5.123 ms
CREATE INDEX
Time: 4.631 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/jjj_sqlprov.sql:7: NOTICE:  materialized view "jjj_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.140 ms
SELECT 10000
Time: 20.808 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/jjj_sqlprov.sql:15: NOTICE:  index "idx_jjj_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.289 ms
CREATE INDEX
Time: 2.499 ms

g10=# \i /Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgn100_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgn100_sqlprov.sql:1: NOTICE:  materialized view "vpgn100_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.514 ms
SELECT 10000
Time: 20.294 ms
CREATE INDEX
Time: 9.698 ms
CREATE INDEX
Time: 7.196 ms
CREATE INDEX
Time: 6.205 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgn100_sqlprov.sql:6: NOTICE:  materialized view "vpgn100_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.146 ms
SELECT 10000
Time: 18.064 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgn100_sqlprov.sql:13: NOTICE:  index "idx_vpgn100_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.282 ms
CREATE INDEX
Time: 3.661 ms

g10=# \i /Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgn1k_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgn1k_sqlprov.sql:1: NOTICE:  materialized view "vpgn1k_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.537 ms
SELECT 100000
Time: 81.159 ms
CREATE INDEX
Time: 30.741 ms
CREATE INDEX
Time: 26.937 ms
CREATE INDEX
Time: 28.012 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgn1k_sqlprov.sql:6: NOTICE:  materialized view "vpgn1k_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.112 ms
SELECT 100000
Time: 96.437 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgn1k_sqlprov.sql:13: NOTICE:  index "idx_vpgn1k_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.271 ms
CREATE INDEX
Time: 20.109 ms

g10=# \i /Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgn10k_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgn10k_sqlprov.sql:1: NOTICE:  materialized view "vpgn10k_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.686 ms
SELECT 1000000
Time: 429.788 ms
CREATE INDEX
Time: 197.826 ms
CREATE INDEX
Time: 177.812 ms
CREATE INDEX
Time: 182.059 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgn10k_sqlprov.sql:6: NOTICE:  materialized view "vpgn10k_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.162 ms
SELECT 1000000
Time: 995.742 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgn10k_sqlprov.sql:13: NOTICE:  index "idx_vpgn10k_2_tuid" does not exist, skipping
DROP INDEX
Time: 19.620 ms
CREATE INDEX
Time: 141.202 ms

g10=# \i /Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgs100_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgs100_sqlprov.sql:1: NOTICE:  materialized view "vpgs100_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.522 ms
SELECT 10000
Time: 19.927 ms
CREATE INDEX
Time: 6.963 ms
CREATE INDEX
Time: 6.352 ms
CREATE INDEX
Time: 5.321 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgs100_sqlprov.sql:6: NOTICE:  materialized view "vpgs100_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.180 ms
SELECT 10000
Time: 19.658 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgs100_sqlprov.sql:13: NOTICE:  index "idx_vpgs100_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.274 ms
CREATE INDEX
Time: 2.721 ms

g10=# \i /Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgs1k_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgs1k_sqlprov.sql:1: NOTICE:  materialized view "vpgs1k_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.491 ms
SELECT 100000
Time: 83.171 ms
CREATE INDEX
Time: 26.579 ms
CREATE INDEX
Time: 22.667 ms
CREATE INDEX
Time: 22.816 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgs1k_sqlprov.sql:6: NOTICE:  materialized view "vpgs1k_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.098 ms
SELECT 100000
Time: 95.204 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgs1k_sqlprov.sql:13: NOTICE:  index "idx_vpgs1k_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.253 ms
CREATE INDEX
Time: 20.093 ms

g10=# \i /Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgs10k_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgs10k_sqlprov.sql:1: NOTICE:  materialized view "vpgs10k_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.556 ms
SELECT 1000000
Time: 437.549 ms
CREATE INDEX
Time: 214.895 ms
CREATE INDEX
Time: 182.386 ms
CREATE INDEX
Time: 179.665 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgs10k_sqlprov.sql:6: NOTICE:  materialized view "vpgs10k_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.151 ms
SELECT 1000000
Time: 984.501 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/vpgs10k_sqlprov.sql:13: NOTICE:  index "idx_vpgs10k_2_tuid" does not exist, skipping
DROP INDEX
Time: 18.229 ms
CREATE INDEX
Time: 153.478 ms

Time: 12.852 ms
NOTICE:  table "pairs_1" does not exist, skipping
DROP TABLE
Time: 0.281 ms
SELECT 10000
Time: 16.579 ms
ERROR:  could not create unique index "pairs_1_pkey"
DETAIL:  Key (f, t)=(106, 898) is duplicated.
Time: 5.992 ms
NOTICE:  table "pairs_2" does not exist, skipping
DROP TABLE
Time: 0.282 ms
SELECT 10000
Time: 16.509 ms
ALTER TABLE
Time: 3.830 ms

NOTICE:  materialized view "fp1_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.995 ms
SELECT 100
Time: 459.708 ms
CREATE INDEX
Time: 1.389 ms
CREATE INDEX
Time: 0.491 ms
CREATE INDEX
Time: 0.338 ms
CREATE INDEX
Time: 0.362 ms
CREATE INDEX
Time: 0.325 ms
CREATE INDEX
Time: 0.328 ms
CREATE INDEX
Time: 0.316 ms
CREATE INDEX
Time: 0.306 ms
NOTICE:  materialized view "fp1_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.113 ms
SELECT 100
Time: 1.111 ms
NOTICE:  index "idx_fp1_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.137 ms
CREATE INDEX
Time: 0.312 ms
NOTICE:  materialized view "fp2_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.082 ms
SELECT 10000
Time: 407.104 ms
CREATE INDEX
Time: 2.551 ms
CREATE INDEX
Time: 1.464 ms
CREATE INDEX
Time: 1.412 ms
CREATE INDEX
Time: 2.034 ms
CREATE INDEX
Time: 1.416 ms
CREATE INDEX
Time: 1.422 ms
CREATE INDEX
Time: 1.451 ms
CREATE INDEX
Time: 1.441 ms
NOTICE:  materialized view "fp2_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.087 ms
SELECT 10000
Time: 17.637 ms
NOTICE:  index "idx_fp2_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.169 ms
CREATE INDEX
Time: 2.191 ms
NOTICE:  materialized view "fp3_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.086 ms
SELECT 200000
Time: 477.320 ms
CREATE INDEX
Time: 44.956 ms
CREATE INDEX
Time: 29.162 ms
CREATE INDEX
Time: 28.980 ms
CREATE INDEX
Time: 43.203 ms
CREATE INDEX
Time: 29.573 ms
CREATE INDEX
Time: 29.489 ms
CREATE INDEX
Time: 29.541 ms
CREATE INDEX
Time: 29.386 ms
NOTICE:  materialized view "fp3_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.113 ms
SELECT 200000
Time: 349.480 ms
NOTICE:  index "idx_fp3_2_tuid" does not exist, skipping
DROP INDEX
Time: 14.922 ms
CREATE INDEX
Time: 43.988 ms
ANALYZE
Time: 701.808 ms


DROP T\i /Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/js_sqlprov.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/js_sqlprov.sql:1: NOTICE:  materialized view "js_1" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.761 ms
SELECT 25000
Time: 36.931 ms
CREATE INDEX
Time: 12.794 ms
CREATE INDEX
Time: 8.814 ms
CREATE INDEX
Time: 7.494 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/js_sqlprov.sql:6: NOTICE:  materialized view "js_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.124 ms
SELECT 25000
Time: 29.607 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/GenData/data/sf0_1/js_sqlprov.sql:13: NOTICE:  index "idx_js_2_tuid" does not exist, skipping
DROP INDEX
Time: 0.240 ms
CREATE INDEX
Time: 3.908 ms

```
# after: 7586319
## provsql

```
-rw-------   1 uicdbgroup  staff    65552 Mar 30 18:34 provsql_extra.mmap
-rw-------   1 uicdbgroup  staff  3145744 Mar 30 18:34 provsql_gates.mmap
-rw-------   1 uicdbgroup  staff  1572888 Mar 30 18:34 provsql_mapping.mmap
-rw-------   1 uicdbgroup  staff  1048592 Mar 30 18:34 provsql_wires.mmap
```


### timing
```
p10=# select add_provenance('dj1');
 add_provenance
----------------

(1 row)

Time: 34.097 ms

p10=# select add_provenance('dj2');
 add_provenance
----------------

(1 row)

Time: 29.812 ms

p10=# select add_provenance('fp');
 add_provenance
----------------

(1 row)

Time: 3837.643 ms (00:03.838)

p10=# select add_provenance('fp1');
 add_provenance
----------------

(1 row)

Time: 20.368 ms

p10=# select add_provenance('fp2');
 add_provenance
----------------

(1 row)

Time: 29.285 ms

p10=# select add_provenance('fp3');
 add_provenance
----------------

(1 row)

Time: 128.743 ms

p10=# select add_provenance('jc');
 add_provenance
----------------

(1 row)

Time: 242.756 ms

p10=# select add_provenance('jj');
 add_provenance
----------------

(1 row)

Time: 84.042 ms

p10=# select add_provenance('jjj');
 add_provenance
----------------

(1 row)

Time: 80.016 ms

p10=# select add_provenance('vpgn100');
 add_provenance
----------------

(1 row)

Time: 74.337 ms

p10=# select add_provenance('vpgn1k');
 add_provenance
----------------

(1 row)

Time: 411.461 ms

p10=# select add_provenance('vpgn10k');
 add_provenance
----------------

(1 row)

Time: 3281.753 ms (00:03.282)

p10=# select add_provenance('vpgs100');
 add_provenance
----------------

(1 row)

Time: 84.121 ms

p10=# select add_provenance('vpgs1k');
 add_provenance
----------------

(1 row)

Time: 409.036 ms

p10=# select add_provenance('vpgs10k');
 add_provenance
----------------

(1 row)

Time: 3219.143 ms (00:03.219)

p10=# select add_provenance('js');
 add_provenance
----------------

(1 row)

Time: 146.682 ms
```

### after: 517079567

```
-rw-------   1 uicdbgroup  staff      65552 Mar 30 18:34 provsql_extra.mmap
-rw-------   1 uicdbgroup  staff  201326608 Mar 30 19:11 provsql_gates.mmap
-rw-------   1 uicdbgroup  staff  201326616 Mar 30 19:10 provsql_mapping.mmap
-rw-------   1 uicdbgroup  staff    1048592 Mar 30 18:34 provsql_wires.mmap
```
## TPCH:
234934755
### SQLPROV
- after `799539727`
- timing
```
gtpch01=# \i /Users/uicdbgroup/pengyuan/exp/sf01/tpchsf01/setup-tpc-h.sql
psql:/Users/uicdbgroup/pengyuan/exp/sf01/tpchsf01/setup-tpc-h.sql:1: NOTICE:  drop cascades to 16 other objects
DETAIL:  drop cascades to materialized view region_1
drop cascades to materialized view nation_1
drop cascades to materialized view part_1
drop cascades to materialized view supplier_1
drop cascades to materialized view partsupp_1
drop cascades to materialized view customer_1
drop cascades to materialized view orders_1
drop cascades to materialized view lineitem_1
drop cascades to materialized view region_2
drop cascades to materialized view nation_2
drop cascades to materialized view part_2
drop cascades to materialized view supplier_2
drop cascades to materialized view partsupp_2
drop cascades to materialized view customer_2
drop cascades to materialized view orders_2
drop cascades to materialized view lineitem_2
DROP SEQUENCE
Time: 59.494 ms
CREATE SEQUENCE
Time: 1.359 ms
SELECT 5
Time: 1.169 ms
SELECT 25
Time: 0.711 ms
SELECT 20000
Time: 17.448 ms
SELECT 1000
Time: 1.423 ms
SELECT 80000
Time: 50.718 ms
SELECT 15000
Time: 15.581 ms
SELECT 150000
Time: 98.647 ms
SELECT 600572
Time: 491.380 ms
CREATE INDEX
Time: 15.755 ms
CREATE INDEX
Time: 0.420 ms
CREATE INDEX
Time: 3.471 ms
CREATE INDEX
Time: 0.457 ms
CREATE INDEX
Time: 27.685 ms
CREATE INDEX
Time: 2.997 ms
CREATE INDEX
Time: 30.610 ms
CREATE INDEX
Time: 166.555 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/tpchsf01/setup-tpc-h.sql:42: NOTICE:  index "nation_fkey_region_1" does not exist, skipping
DROP INDEX
Time: 0.152 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/tpchsf01/setup-tpc-h.sql:43: NOTICE:  index "supplier_fkey_nation_1" does not exist, skipping
DROP INDEX
Time: 0.120 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/tpchsf01/setup-tpc-h.sql:44: NOTICE:  index "partsupp_fkey_part_1" does not exist, skipping
DROP INDEX
Time: 0.102 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/tpchsf01/setup-tpc-h.sql:45: NOTICE:  index "partsupp_fkey_supplier_1" does not exist, skipping
DROP INDEX
Time: 0.104 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/tpchsf01/setup-tpc-h.sql:46: NOTICE:  index "customer_fkey_nation_1" does not exist, skipping
DROP INDEX
Time: 0.117 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/tpchsf01/setup-tpc-h.sql:47: NOTICE:  index "orders_fkey_customer_1" does not exist, skipping
DROP INDEX
Time: 0.097 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/tpchsf01/setup-tpc-h.sql:48: NOTICE:  index "lineitem_fkey_partsupp_1" does not exist, skipping
DROP INDEX
Time: 0.093 ms
psql:/Users/uicdbgroup/pengyuan/exp/sf01/tpchsf01/setup-tpc-h.sql:49: NOTICE:  index "lineitem_fkey_orders_1" does not exist, skipping
DROP INDEX
Time: 0.091 ms
CREATE INDEX
Time: 0.376 ms
CREATE INDEX
Time: 0.709 ms
CREATE INDEX
Time: 19.603 ms
CREATE INDEX
Time: 27.119 ms
CREATE INDEX
Time: 7.538 ms
CREATE INDEX
Time: 45.505 ms
CREATE INDEX
Time: 246.763 ms
CREATE INDEX
Time: 126.438 ms
SELECT 5
Time: 0.788 ms
SELECT 25
Time: 0.670 ms
SELECT 20000
Time: 44.920 ms
SELECT 1000
Time: 2.868 ms
SELECT 80000
Time: 93.784 ms
SELECT 15000
Time: 26.032 ms
SELECT 150000
Time: 316.900 ms
SELECT 600572
Time: 2017.190 ms (00:02.017)
CREATE INDEX
Time: 43.525 ms
CREATE INDEX
Time: 0.395 ms
CREATE INDEX
Time: 3.369 ms
CREATE INDEX
Time: 0.469 ms
CREATE INDEX
Time: 12.860 ms
CREATE INDEX
Time: 2.502 ms
CREATE INDEX
Time: 22.628 ms
CREATE INDEX
Time: 103.305 ms
ANALYZE
Time: 3955.359 ms (00:03.955)
```
### PROVSQL
after ptpch01=# select pg_database_size('ptpch01');
 pg_database_size
------------------
        276996623


```
-rw-------   1 uicdbgroup  staff    65552 Mar 30 18:36 provsql_extra.mmap
-rw-------   1 uicdbgroup  staff  3145744 Mar 30 18:36 provsql_gates.mmap
-rw-------   1 uicdbgroup  staff  1572888 Mar 30 18:36 provsql_mapping.mmap
-rw-------   1 uicdbgroup  staff  1048592 Mar 30 18:36 provsql_wires.mmap
```

#### after
```
-rw-------   1 uicdbgroup  staff     65552 Mar 30 18:36 provsql_extra.mmap
-rw-------   1 uicdbgroup  staff  50331664 Apr  5 21:36 provsql_gates.mmap
-rw-------   1 uicdbgroup  staff  50331672 Apr  5 21:36 provsql_mapping.mmap
-rw-------   1 uicdbgroup  staff   1048592 Mar 30 18:36 provsql_wires.mmap
```
- timing
```
Timing is on.
ptpch01=# select add_provenance('lineitem');
 add_provenance
----------------

(1 row)

Time: 2660.374 ms (00:02.660)
ptpch01=# select add_provenance('orders');
 add_provenance
----------------

(1 row)

Time: 544.557 ms
ptpch01=# select add_provenance('part');
 add_provenance
----------------

(1 row)

Time: 100.922 ms
ptpch01=# select add_provenance('partsupp');
 add_provenance
----------------

(1 row)

Time: 339.985 ms
ptpch01=# select add_provenance('region');
 add_provenance
----------------

(1 row)

Time: 11.471 ms
ptpch01=# select add_provenance('supplier');
 add_provenance
----------------

(1 row)

Time: 21.420 ms
```
# SF10
- 23010472419
## sqlprov

- after '78967243279'
```
psql:/Users/uicdbgroup/pengyuan/exp/sf01/tpchsf01/setup-tpc-h.sql:1: NOTICE:  sequence "prov_ids" does not exist, skipping
DROP SEQUENCE
Time: 0.442 ms
CREATE SEQUENCE
Time: 1.619 ms
SELECT 5
Time: 4.854 ms
SELECT 25
Time: 3.444 ms
SELECT 2000000
Time: 1426.350 ms (00:01.426)
SELECT 100000
Time: 110.509 ms
SELECT 8000000
Time: 4742.694 ms (00:04.743)
SELECT 1500000
Time: 1229.551 ms (00:01.230)
SELECT 15000000
Time: 9384.898 ms (00:09.385)
SELECT 59986052
Time: 43394.302 ms (00:43.394)
CREATE INDEX
Time: 113.300 ms
CREATE INDEX
Time: 0.450 ms
CREATE INDEX
Time: 398.961 ms
CREATE INDEX
Time: 27.300 ms
CREATE INDEX
Time: 3447.329 ms (00:03.447)
CREATE INDEX
Time: 337.824 ms
CREATE INDEX
Time: 3625.958 ms (00:03.626)
CREATE INDEX
Time: 19546.953 ms (00:19.547)
psql:/Users/uicdbgroup/pengyuan/exp/sf01/tpchsf01/setup-tpc-h.sql:42: NOTICE:  index "nation_fkey_region_1" does not exist, skipping
DROP INDEX
Time: 0.284 ms

CREATE INDEX
Time: 74.296 ms
CREATE INDEX
Time: 2764.103 ms (00:02.764)
CREATE INDEX
Time: 2198.585 ms (00:02.199)
CREATE INDEX
Time: 1704.593 ms (00:01.705)
CREATE INDEX
Time: 5339.612 ms (00:05.340)
CREATE INDEX
Time: 28139.701 ms (00:28.140)
CREATE INDEX
Time: 13293.622 ms (00:13.294)
SELECT 5
Time: 1.170 ms
SELECT 25
Time: 0.742 ms
SELECT 2000000
Time: 3897.303 ms (00:03.897)
SELECT 100000
Time: 229.842 ms
SELECT 8000000
Time: 9635.243 ms (00:09.635)
SELECT 1500000
Time: 2801.767 ms (00:02.802)
SELECT 15000000
Time: 28956.513 ms (00:28.957)
SELECT 59986052
Time: 194560.056 ms (03:14.560)
CREATE INDEX
Time: 562.101 ms
CREATE INDEX
Time: 0.733 ms
CREATE INDEX
Time: 808.585 ms
CREATE INDEX
Time: 36.973 ms
CREATE INDEX
Time: 2578.583 ms (00:02.579)
CREATE INDEX
Time: 726.132 ms
CREATE INDEX
Time: 10560.623 ms (00:10.561)
CREATE INDEX
Time: 27711.493 ms (00:27.711)
ANALYZE
Time: 25992.555 ms (00:25.993)
```

## provsql
- 27162595811
- timing
```
ptpch10=# \i /Users/uicdbgroup/pengyuan/exp/sf10/tpchdata/addprov.sql
 add_provenance
----------------

(1 row)

Time: 5422.668 ms (00:05.423)
 add_provenance
----------------

(1 row)

Time: 274531.171 ms (04:34.531)
 add_provenance
----------------

(1 row)

Time: 3.206 ms
 add_provenance
----------------

(1 row)

Time: 52299.039 ms (00:52.299)
 add_provenance
----------------

(1 row)

Time: 5893.100 ms (00:05.893)
 add_provenance
----------------

(1 row)

Time: 31363.802 ms (00:31.364)
 add_provenance
----------------

(1 row)

Time: 10.368 ms
 add_provenance
----------------

(1 row)

Time: 382.252 ms
```

- mmaps
```
-rw-------   1 uicdbgroup  staff       65552 Apr  5 22:37 provsql_extra.mmap
-rw-------   1 uicdbgroup  staff  6442450960 Apr  5 23:16 provsql_gates.mmap
-rw-------   1 uicdbgroup  staff  6442450968 Apr  5 23:14 provsql_mapping.mmap
-rw-------   1 uicdbgroup  staff     1048592 Apr  5 22:37 provsql_wires.mmap
```