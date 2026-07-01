WITH RECURSIVE
rview_2(tuid, node) AS (
    SELECT v.tuid AS tuid, empty()::bigint[]
    FROM   (VALUES (readOne(4))) AS v(tuid)

    UNION ALL

    SELECT l.tuid, t.n
    FROM (SELECT l.tuid AS tuid, (s2.t)::bigint[] AS n
          FROM rview_2 AS r2, rcr_2 AS s2,
               readLog(2, r2.tuid, s2.tuid) AS l(tuid)
          ) AS t, readLog(1, t.tuid) AS l(tuid)
)
SELECT l.tuid,
       dd(h.node) AS node
FROM rview_2 AS h, readLog(3, h.tuid) AS l(tuid);