select writeaggregation(2, array_agg(sub.tuid)) as tuid, avg(sub.va) as ava, avg(sub.vb) as avb, sub.GROUP_BY_ATTRIBUTE as GROUP_BY_ATTRIBUTE
    from FROM_TABLE as sub (tuid, ATTRIBUTES)
group by GROUP_BY_ATTRIBUTE;