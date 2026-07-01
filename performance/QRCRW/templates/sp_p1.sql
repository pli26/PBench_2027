WITH RECURSIVE
rview_1(tuid, v) AS (

    SELECT v.tuid::same AS tuid, 1::int as v -- start from 1
    FROM   (VALUES (writeLog(4))) AS v(tuid)

    UNION DISTINCT

    SELECT writeLog(1, sub.tuid)::same AS tuid, sub.t
    FROM   (SELECT writeLog(2, r.tuid, p.tuid) AS tuid, p.t as t
            FROM rview_1 AS r, rcr_1 AS p
            WHERE r.v=p.f) sub
)
SELECT writeLog(3, r.tuid) AS tuid, r.v AS node
FROM  rview_1 AS r ;