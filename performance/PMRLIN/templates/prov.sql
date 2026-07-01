select unnest(string_to_array(regexp_replace(provs.provone, '[{{}}]','', 'g'), ','))::bigint as provone,
    unnest(string_to_array(regexp_replace(provs.provtwo, '[{{}}]','', 'g'), ','))::bigint as provtwo
from (
    select sr_why(provenance(), 'mapping_{tableName}') as provone,
        sr_why(provenance(), 'mapping_{joinedTable}') as provtwo
    from (
        select distinct gb from {tableName} join {joinedTable} on (gb = c1to10)
    ) tt
) provs;