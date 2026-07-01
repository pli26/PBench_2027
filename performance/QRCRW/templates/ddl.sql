-- Ensure the table uses integers
CREATE TABLE IF NOT EXISTS pairs (
    f INT,
    t INT
);
INSERT INTO pairs (f, t)
SELECT
    (random() * 1000)::int AS f,
    (random() * 1000)::int AS t
FROM generate_series(1, 100000) s(i);

-- Optional: Add an index to make the recursive join fast
CREATE INDEX idx_pair_iddx ON pairs(f);


-- sf0.1
-- Ensure the table uses integers
drop table if exists pairs cascade;
CREATE TABLE IF NOT EXISTS pairs (
    f INT,
    t INT
);
INSERT INTO pairs (f, t)
SELECT
    (random() * 100)::int AS f,
    (random() * 100)::int AS t
FROM generate_series(1, 10000) s(i);

-- Optional: Add an index to make the recursive join fast
CREATE INDEX idx_pair_iddx ON pairs(f);

DROP TABLE IF EXISTS pairs_1 CASCADE;
CREATE TABLE pairs_1 AS
    SELECT nextval('prov_ids')::tuid_t AS tuid, *
    FROM pairs;

CREATE INDEX idx_pair1_iddx ON pairs_1(f);
DROP TABLE IF EXISTS pairs_2 CASCADE;
CREATE TABLE pairs_2 AS
  SELECT p.tuid,
         ARRAY[nextval('prov_ids')::int] AS f,
         ARRAY[nextval('prov_ids')::int] AS t
    FROM pairs_1 as p ;
ALTER TABLE pairs_2 ADD PRIMARY KEY (tuid);
















drop table if exists pairs cascade;
create table pairs (f int, t int);
insert into pairs values
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (4, 2),
    (4, 1),
    (5, 6),
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (12, 13),
    (13, 14),
    (14, 15),
    (15, 16),
    (12, 10),
    (16, 14);
alter table pairs add primary key (f, t);
DROP TABLE IF EXISTS pairs_1 CASCADE;
CREATE TABLE pairs_1 AS
    SELECT nextval('prov_ids')::tuid_t AS tuid, *
    FROM pairs;

ALTER TABLE pairs_1 ADD PRIMARY KEY (f, t);

DROP TABLE IF EXISTS pairs_2 CASCADE;
CREATE TABLE pairs_2 AS
  SELECT p.tuid,
         ARRAY[nextval('prov_ids')::int] AS f,
         ARRAY[nextval('prov_ids')::int] AS t
    FROM pairs_1 as p ;
ALTER TABLE pairs_2 ADD PRIMARY KEY (tuid);


WITH RECURSIVE
rcr_1(tuid, v) AS (

    SELECT v.tuid::same AS tuid, 1
    FROM   (VALUES (writeLog(4))) AS v(tuid)

    UNION DISTINCT

    SELECT writeLog(1, sub.tuid)::same AS tuid, sub.t
    FROM   (SELECT writeLog(2, r.tuid, p.tuid) AS tuid, p.t as t
            FROM rcr_1 AS r, pairs_1 AS p
            WHERE r.v=p.f) sub
)
SELECT writeLog(3, r.tuid) AS tuid, r.v AS node
FROM  rcr_1 AS r ;

WITH RECURSIVE
rcr_2(tuid, node) AS (
    SELECT v.tuid AS tuid, empty()::bigint[]
    FROM   (VALUES (readOne(4))) AS v(tuid)

    UNION ALL

    SELECT l.tuid, t.n
    FROM (SELECT l.tuid AS tuid, (e.t)::bigint[] AS n
          FROM rcr_2 AS h, pairs_2 AS e,
               readLog(2, h.tuid, e.tuid) AS l(tuid)
          ) AS t, readLog(1, t.tuid) AS l(tuid)
)
SELECT l.tuid,
       dd(h.node) AS node
FROM rcr_2 AS h, readLog(3, h.tuid) AS l(tuid) ;
