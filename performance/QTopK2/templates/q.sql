select gc, min(va) as ava, min(vc) as avc from fp group by gc order by ava limit LIMIT_VALUE
