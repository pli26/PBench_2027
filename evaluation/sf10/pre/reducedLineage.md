## get reduced data PostgreSQL
```sql
-- mininal
create table fp1 as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 1;
NOTICE:  table "fp1" does not exist, skipping
DROP TABLE
Time: 0.476 ms
SELECT 10000
Time: 154222.078 ms (02:34.222)
-- 1%
create table fp2 as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 100;
NOTICE:  table "fp2" does not exist, skipping
DROP TABLE
Time: 1.079 ms
SELECT 1000000
Time: 155216.087 ms (02:35.216)

-- 20 %
create table fp3 as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 2000;
NOTICE:  table "fp3" does not exist, skipping
DROP TABLE
Time: 0.676 ms
SELECT 20000000
Time: 161230.318 ms (02:41.230)
```
## get reduced data Duckdb:
```sql
-- minimal
D create table fp1 as
    select id, ga, gb, gc, hv, va, vb, vc
    from (
        select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
        from fp
    ) t
    where t.rn <= 1;
100% ▕████████████████████████████████████████████████████████████▏
Run Time (s): real 2.447 user 24.811372 sys 1.406377
-- 1%
create table fp2 as
    select id, ga, gb, gc, hv, va, vb, vc
    from (
        select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
        from fp
    ) t
    where t.rn <= 100;
100% ▕████████████████████████████████████████████████████████████▏
Run Time (s): real 2.593 user 24.190316 sys 1.861187
-- 20%
create table fp3 as
    select id, ga, gb, gc, hv, va, vb, vc
    from (
        select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
        from fp
    ) t
    where t.rn <= 2000;
100% ▕████████████████████████████████████████████████████████████▏
Run Time (s): real 2.690 user 27.340402 sys 1.725552
```

## SQLProv build:
```sql
-- minimal
DROP MATERIALIZED VIEW
Time: 20.173 ms
SELECT 10000
Time: 13.968 ms
CREATE INDEX
Time: 4.302 ms
CREATE INDEX
Time: 3.298 ms
CREATE INDEX
Time: 3.417 ms
CREATE INDEX
Time: 3.061 ms
CREATE INDEX
Time: 2.853 ms
CREATE INDEX
Time: 2.832 ms
CREATE INDEX
Time: 2.842 ms
NOTICE:  materialized view "fp1_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.122 ms
SELECT 10000
Time: 24.858 ms
NOTICE:  index "idx_fp_1_tuid" does not exist, skipping
DROP INDEX
Time: 0.191 ms
CREATE INDEX
Time: 2.230 ms
-- 1%
DROP MATERIALIZED VIEW
Time: 0.873 ms
SELECT 1000000
Time: 483.021 ms
CREATE INDEX
Time: 119.977 ms
CREATE INDEX
Time: 99.344 ms
CREATE INDEX
Time: 140.266 ms
CREATE INDEX
Time: 100.231 ms
CREATE INDEX
Time: 101.284 ms
CREATE INDEX
Time: 101.555 ms
CREATE INDEX
Time: 101.135 ms
NOTICE:  materialized view "fp2_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.130 ms
SELECT 1000000
Time: 1731.609 ms (00:01.732)
NOTICE:  index "idx_fp_2_tuid" does not exist, skipping
DROP INDEX
Time: 32.209 ms
CREATE INDEX
Time: 154.830 ms
--20%
DROP MATERIALIZED VIEW
Time: 0.652 ms
SELECT 20000000
Time: 8617.274 ms (00:08.617)
CREATE INDEX
Time: 2150.436 ms (00:02.150)
CREATE INDEX
Time: 2094.823 ms (00:02.095)
CREATE INDEX
Time: 2879.763 ms (00:02.880)
CREATE INDEX
Time: 1911.714 ms (00:01.912)
CREATE INDEX
Time: 1920.835 ms (00:01.921)
CREATE INDEX
Time: 1934.922 ms (00:01.935)
CREATE INDEX
Time: 1944.625 ms (00:01.945)
NOTICE:  materialized view "fp3_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.134 ms
SELECT 20000000
Time: 34110.151 ms (00:34.110)
NOTICE:  index "idx_fp_3_tuid" does not exist, skipping
DROP INDEX
Time: 153.954 ms
CREATE INDEX
Time: 2273.140 ms (00:02.273)
```

## ProvSQL build:
```sql

sizes=# select add_provenance('fp1');
 add_provenance
----------------

(1 row)
---------------------------------------------------------
Time: 54.373 ms
sizes=# select add_provenance('fp2');
 add_provenance
----------------

(1 row)

Time: 1541.646 ms (00:01.542)

--------------------------------------------------------

elect add_provenance('fp3');
 add_provenance
----------------

(1 row)

Time: 30850.326 ms (00:30.850)
```