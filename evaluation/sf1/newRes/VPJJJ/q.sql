select ga, avg(va) as ava, avg(vb) as avb
from FROM_TABLE
    join J1 on ga = p10
    join JJ2 ON ga = c5
    join JJJ3 on ga = cc2 group by ga