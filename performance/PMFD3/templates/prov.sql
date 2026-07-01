select ()
from (
    select *, sr_why(provenance(), 'mapping_{tableName}') as provone,
        sr_why(provenance(), 'mapping_{joinedTable}') as provtwo
    from (
        select ga, va, vb from {tableName}, {joinedTable} WHERE ga = c1to10 AND WHERECONDITION
    ) tt
) provs;