
----------------
-- gprom
----------------
-- reduced to MIN
drop table if exists fp1 cascade;
create table fp1 (id, ga, gb, gc, hv, va, vb, vc) as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 1;
ALTER TABLE fp1 ADD PRIMARY KEY (id);
ALTER TABLE fp1 ALTER COLUMN ga SET NOT NULL;
ALTER TABLE fp1 ALTER COLUMN gb SET NOT NULL;
ALTER TABLE fp1 ALTER COLUMN gc SET NOT NULL;
ALTER TABLE fp1 ALTER COLUMN hv SET NOT NULL;
ALTER TABLE fp1 ALTER COLUMN va SET NOT NULL;
ALTER TABLE fp1 ALTER COLUMN vb SET NOT NULL;
ALTER TABLE fp1 ALTER COLUMN vc SET NOT NULL;
create index idx_fp1_ga on fp1 (ga);
create index idx_fp1_gb on fp1 (gb);
create index idx_fp1_gc on fp1 (gc);
create index idx_fp1_hv on fp1 (hv);
create index idx_fp1_va on fp1 (va);
create index idx_fp1_vb on fp1 (vb);
create index idx_fp1_vc on fp1 (vc);

-- reduced to 1%
drop table if exists fp2 cascade;
create table fp2 (id, ga, gb, gc, hv, va, vb, vc) as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 100;
ALTER TABLE fp2 ADD PRIMARY KEY (id);
ALTER TABLE fp2 ALTER COLUMN ga SET NOT NULL;
ALTER TABLE fp2 ALTER COLUMN gb SET NOT NULL;
ALTER TABLE fp2 ALTER COLUMN gc SET NOT NULL;
ALTER TABLE fp2 ALTER COLUMN hv SET NOT NULL;
ALTER TABLE fp2 ALTER COLUMN va SET NOT NULL;
ALTER TABLE fp2 ALTER COLUMN vb SET NOT NULL;
ALTER TABLE fp2 ALTER COLUMN vc SET NOT NULL;
create index idx_fp2_ga on fp2 (ga);
create index idx_fp2_gb on fp2 (gb);
create index idx_fp2_gc on fp2 (gc);
create index idx_fp2_hv on fp2 (hv);
create index idx_fp2_va on fp2 (va);
create index idx_fp2_vb on fp2 (vb);
create index idx_fp2_vc on fp2 (vc);

-- reduced to 20%
drop table if exists fp3 cascade;
create table fp3 (id, ga, gb, gc, hv, va, vb, vc) as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 2000;
ALTER TABLE fp3 ADD PRIMARY KEY (id);
ALTER TABLE fp3 ALTER COLUMN ga SET NOT NULL;
ALTER TABLE fp3 ALTER COLUMN gb SET NOT NULL;
ALTER TABLE fp3 ALTER COLUMN gc SET NOT NULL;
ALTER TABLE fp3 ALTER COLUMN hv SET NOT NULL;
ALTER TABLE fp3 ALTER COLUMN va SET NOT NULL;
ALTER TABLE fp3 ALTER COLUMN vb SET NOT NULL;
ALTER TABLE fp3 ALTER COLUMN vc SET NOT NULL;
create index idx_fp3_ga on fp3 (ga);
create index idx_fp3_gb on fp3 (gb);
create index idx_fp3_gc on fp3 (gc);
create index idx_fp3_hv on fp3 (hv);
create index idx_fp3_va on fp3 (va);
create index idx_fp3_vb on fp3 (vb);
create index idx_fp3_vc on fp3 (vc);


--------------------------
-- sqlprov
--------------------------
-- reduced to MIN
drop materialized view if exists fp1_1 cascade;
create materialized view fp1_1 (tuid, id, ga, gb, gc, hv, va, vb, vc) as
select tuid, id, ga, gb, gc, hv, va, vb, vc
from (
    select tuid, id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp_1
) t
where t.rn <= 1;

create index idx_fp1_1_id on fp1_1 (id);
create index idx_fp1_1_ga on fp1_1 (ga);
create index idx_fp1_1_gb on fp1_1 (gb);
create index idx_fp1_1_gc on fp1_1 (gc);
create index idx_fp1_1_hv on fp1_1 (hv);
create index idx_fp1_1_va on fp1_1 (va);
create index idx_fp1_1_vb on fp1_1 (vb);
create index idx_fp1_1_vc on fp1_1 (vc);

drop materialized view if exists fp1_2;
create materialized view fp1_2 as select tuid
,  array[nextval('prov_ids')::int] id
,  array[nextval('prov_ids')::int] ga
,  array[nextval('prov_ids')::int] gb
,  array[nextval('prov_ids')::int] gc
,  array[nextval('prov_ids')::int] hv
,  array[nextval('prov_ids')::int] va
,  array[nextval('prov_ids')::int] vb
,  array[nextval('prov_ids')::int] vc
from fp1_1;
drop index if exists idx_fp1_2_tuid;
create index idx_fp1_2_tuid on fp1_2 (tuid);

-- reduced to 1%
drop materialized view if exists fp2_1 cascade;
create materialized view fp2_1 (tuid, id, ga, gb, gc, hv, va, vb, vc) as
select tuid, id, ga, gb, gc, hv, va, vb, vc
from (
    select tuid, id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp_1
) t
where t.rn <= 100;

create index idx_fp2_1_id on fp2_1 (id);
create index idx_fp2_1_ga on fp2_1 (ga);
create index idx_fp2_1_gb on fp2_1 (gb);
create index idx_fp2_1_gc on fp2_1 (gc);
create index idx_fp2_1_hv on fp2_1 (hv);
create index idx_fp2_1_va on fp2_1 (va);
create index idx_fp2_1_vb on fp2_1 (vb);
create index idx_fp2_1_vc on fp2_1 (vc);

drop materialized view if exists fp2_2;
create materialized view fp2_2 as select tuid
,  array[nextval('prov_ids')::int] id
,  array[nextval('prov_ids')::int] ga
,  array[nextval('prov_ids')::int] gb
,  array[nextval('prov_ids')::int] gc
,  array[nextval('prov_ids')::int] hv
,  array[nextval('prov_ids')::int] va
,  array[nextval('prov_ids')::int] vb
,  array[nextval('prov_ids')::int] vc
from fp2_1;
drop index if exists idx_fp2_2_tuid;
create index idx_fp2_2_tuid on fp2_2 (tuid);



-- reduced to 20%
drop materialized view if exists fp3_1 cascade;
create materialized view fp3_1 (tuid, id, ga, gb, gc, hv, va, vb, vc) as
select tuid, id, ga, gb, gc, hv, va, vb, vc
from (
    select tuid, id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp_1
) t
where t.rn <= 2000;

create index idx_fp3_1_id on fp3_1 (id);
create index idx_fp3_1_ga on fp3_1 (ga);
create index idx_fp3_1_gb on fp3_1 (gb);
create index idx_fp3_1_gc on fp3_1 (gc);
create index idx_fp3_1_hv on fp3_1 (hv);
create index idx_fp3_1_va on fp3_1 (va);
create index idx_fp3_1_vb on fp3_1 (vb);
create index idx_fp3_1_vc on fp3_1 (vc);

drop materialized view if exists fp3_2;
create materialized view fp3_2 as select tuid
,  array[nextval('prov_ids')::int] id
,  array[nextval('prov_ids')::int] ga
,  array[nextval('prov_ids')::int] gb
,  array[nextval('prov_ids')::int] gc
,  array[nextval('prov_ids')::int] hv
,  array[nextval('prov_ids')::int] va
,  array[nextval('prov_ids')::int] vb
,  array[nextval('prov_ids')::int] vc
from fp3_1;
drop index if exists idx_fp3_2_tuid;
create index idx_fp3_2_tuid on fp3_2 (tuid);



analyze;







----------------
-- provsql
----------------

-- select id, ga, gb, gc, hv, va, vb, vc
-- from (
--     select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
--     from fp
-- ) t
-- where t.rn <= {REDUCTION_FACTOR}
