select max(va) as maxava, max(vb) as maxvb from (select gb, avg(va) as va, avg(vb) as vb from fp group by gb) sub group by null
