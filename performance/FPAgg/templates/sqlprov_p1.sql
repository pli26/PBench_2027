select writeaggregation(2, array_agg(r1.tuid)) as tuid, avg(r1.va) as ava, avg(r1.vb) as avb, r1.GROUP_BY_ATTRIBUTE as GROUP_BY_ATTRIBUTE
from FROM_TABLE as r1 (tuid, ATTRIBUTES)
group by GROUP_BY_ATTRIBUTE;