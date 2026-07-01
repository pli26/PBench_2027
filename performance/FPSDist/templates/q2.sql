select distinct t1.DISTINCT_ATTRIBUTE_A
from (select distinct DISTINCT_ATTRIBUTE_A from TBL1) as t1
    join
    (select distinct DISTINCT_ATTRIBUTE_B from TBL2) as t2
on t1.DISTINCT_ATTRIBUTE_A = t2.DISTINCT_ATTRIBUTE_B