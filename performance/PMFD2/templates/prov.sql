select ()
from (
    select *, sr_which(provenance(), 'mapping_{tableName}') as provone,
        sr_which(provenance(), 'mapping_{joinedTable}') as provtwo
    from (
        select ga, avg(va) as ava, avg(vb) as avb from {tableName}, {joinedTable} WHERE ga = c1to10 AND WHERECONDITION group by ga
    ) tt
) provs;