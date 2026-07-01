select unnest(provone::integer[])::bigint as provone,
    unnest(provtwo::integer[])::bigint as provtwo
from (
    select sr_which(provenance(), 'mapping_{tableName}') as provone,
        sr_which(provenance(), 'mapping_{joinedTable}') as provtwo
    from (
        select ga, avg(va) as ava, avg(vb) as avb from {tableName} join {joinedTable} on (ga = c1to10) group by ga
    ) tt
) provs;