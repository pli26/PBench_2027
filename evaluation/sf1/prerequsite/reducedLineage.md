## get reduced data PostgreSQL
```sql
-- mininal
drop table if exists fp1 cascade;
create table fp1 (id, ga, gb, gc, hv, va, vb, vc) as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 1;
NOTICE:  table "fp1" does not exist, skipping
DROP TABLE
Time: 0.442 ms
SELECT 1000
Time: 4230.460 ms (00:04.230)

-- 1%
create table fp2 (id, ga, gb, gc, hv, va, vb, vc) as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 100;
SELECT 100000
Time: 4291.625 ms (00:04.292)
-- 20%
drop table if exists fp3 cascade;
create table fp3 (id, ga, gb, gc, hv, va, vb, vc) as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 2000;
NOTICE:  table "fp3" does not exist, skipping
DROP TABLE
Time: 0.547 ms
SELECT 2000000
Time: 4909.354 ms (00:04.909)
```
## get reduced data Duckdb:
```sql
-- minimal
create table fp1 as
  select id, ga, gb, gc, hv, va, vb, vc
  from (
      select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
      from fp
  ) t
  where t.rn <= 1;
Run Time (s): real 0.218 user 1.879280 sys 0.166573
-- 1%
create table fp2 as
  select id, ga, gb, gc, hv, va, vb, vc
  from (
      select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
      from fp
  ) t
  where t.rn <= 100;
Run Time (s): real 0.220 user 1.994800 sys 0.149107
-- 20%
create table fp3 as
  select id, ga, gb, gc, hv, va, vb, vc
  from (
      select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
      from fp
  ) t
  where t.rn <= 2000;
Run Time (s): real 0.260 user 2.365160 sys 0.146893
```

## SQLProv build:
```sql
-- minimal
DROP MATERIALIZED VIEW
Time: 1.004 ms
SELECT 1000
Time: 7.648 ms
CREATE INDEX
Time: 2.389 ms
CREATE INDEX
Time: 1.852 ms
CREATE INDEX
Time: 1.450 ms
CREATE INDEX
Time: 1.180 ms
CREATE INDEX
Time: 1.155 ms
CREATE INDEX
Time: 1.076 ms
CREATE INDEX
Time: 1.095 ms
NOTICE:  materialized view "fp1_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.088 ms
SELECT 1000
Time: 7.253 ms
DROP INDEX
Time: 0.661 ms
CREATE INDEX
Time: 4.073 ms
-- 1%
DROP MATERIALIZED VIEW
Time: 0.449 ms
SELECT 100000
Time: 85.144 ms
CREATE INDEX
Time: 14.267 ms
CREATE INDEX
Time: 11.262 ms
CREATE INDEX
Time: 17.236 ms
CREATE INDEX
Time: 11.530 ms
CREATE INDEX
Time: 11.604 ms
CREATE INDEX
Time: 11.701 ms
CREATE INDEX
Time: 11.835 ms
NOTICE:  materialized view "fp2_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.089 ms
SELECT 100000
Time: 171.350 ms
NOTICE:  index "idx_fp_2_tuid" does not exist, skipping
DROP INDEX
Time: 1.967 ms
CREATE INDEX
Time: 21.625 ms
--20%
DROP MATERIALIZED VIEW
Time: 43.066 ms
SELECT 2000000
Time: 851.355 ms
CREATE INDEX
Time: 240.853 ms
CREATE INDEX
Time: 207.327 ms
CREATE INDEX
Time: 302.354 ms
CREATE INDEX
Time: 209.018 ms
CREATE INDEX
Time: 214.094 ms
CREATE INDEX
Time: 214.638 ms
CREATE INDEX
Time: 214.630 ms
NOTICE:  materialized view "fp3_2" does not exist, skipping
DROP MATERIALIZED VIEW
Time: 0.125 ms
SELECT 2000000
Time: 3430.815 ms (00:03.431)
NOTICE:  index "idx_fp_3_tuid" does not exist, skipping
DROP INDEX
Time: 73.039 ms
CREATE INDEX
Time: 239.417 ms
```

## ProvSQL build:
```sql
select add_provenance('fp1');
 add_provenance
----------------

(1 row)

Time: 14.223 ms

select create_provenance_mapping('mfp1', 'fp1', 'id');
 create_provenance_mapping
---------------------------

(1 row)

Time: 19.147 ms
--
select add_provenance('fp2');
 add_provenance
----------------

(1 row)

Time: 201.362 ms
select create_provenance_mapping('mfp2', 'fp2', 'id');
 create_provenance_mapping
---------------------------

(1 row)

Time: 106.521 ms
--
select add_provenance('fp3');
 add_provenance
----------------

(1 row)

Time: 3007.337 ms (00:03.007)

select create_provenance_mapping('mfp3', 'fp3', 'id');
 create_provenance_mapping
---------------------------

(1 row)

Time: 1152.255 ms (00:01.152)
```