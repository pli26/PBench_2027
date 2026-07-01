select ga, avg(va) over(
    partition by ga
    order by id) as rkava
from fp;