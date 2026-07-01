-----------------
-- duckdb
-----------------
-- min
drop table if exists fp1 cascade;
create table fp1 as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 1;

-- reduced to 1%
drop table if exists fp2 cascade;
create table fp2 as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 100;

-- reduced to 20%
drop table if exists fp3 cascade;
create table fp3 as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 2000;

analyze;
