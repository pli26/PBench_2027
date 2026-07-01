WITH temp_view_1 AS (
SELECT /*+ materialize */ F0_0."AGGR_0" AS "AGGR_0", F0_0.ga AS "GROUP_0", F0_0."prov_vpgn100_id" AS "prov_vpgn100_id", dense_rank() OVER ( ORDER BY F0_0.ga) AS _result_tid, row_number() OVER (PARTITION BY F0_0.ga ORDER BY F0_0.ga) AS _setprov_dup_count
FROM (
SELECT F0_0.id AS id, F0_0.ga AS ga, F0_0.va AS va, F0_0.vb AS vb, F0_0.id AS "prov_vpgn100_id", (F0_0.id)::int8 AS _result_tid, 1 AS _setprov_dup_count, avg(F0_0.va) OVER (PARTITION BY F0_0.ga) AS "AGGR_0"
FROM "vpgn100" F0_0
WHERE EXISTS_CONDITIONS) F0_0),
temp_view_0 AS (
SELECT /*+ materialize */ F0_0."GROUP_0" AS ga, F0_0."AGGR_0" AS "avg(va)", F0_0."prov_vpgn100_id" AS "prov_vpgn100_id", F0_0._result_tid AS _result_tid, F0_0._setprov_dup_count AS _setprov_dup_count
FROM (SELECT * FROM temp_view_1) F0_0)
SELECT F0_0.ga AS ga, F0_0."avg(va)" AS "avg(va)", F0_0."prov_vpgn100_id" AS "prov_vpgn100_id"
FROM (SELECT * FROM temp_view_0) F0_0;
