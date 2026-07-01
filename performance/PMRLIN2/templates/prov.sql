select unnest(provone::integer[])::bigint as provone,
    unnest(provtwo::integer[])::bigint as provtwo
from (
    select sr_which(provenance(), 'mapping_{tableName}') as provone,
        sr_which(provenance(), 'mapping_{joinedTable}') as provtwo
    from (
        select gb, min(va) as minva from {tableName} join {joinedTable} on (gb = c1to10) group by gb
    ) tt
) provs;