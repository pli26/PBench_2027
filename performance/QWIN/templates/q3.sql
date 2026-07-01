select ga, avg(va) over(
    partition by gb
    order by id) as rkava
from fp;