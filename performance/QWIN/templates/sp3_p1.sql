select writewindow(1, r1.tuid, first_value(r1.tuid) over (partition by r1.gb order by r1.id asc range unbounded preceding),
    rank() over (partition by r1.gb order by r1.id asc range unbounded preceding)) as tuid, r1.gb, avg(r1.va) over(partition by r1.gb order by r1.id asc range unbounded preceding) as ava
from fp_1 as r1;