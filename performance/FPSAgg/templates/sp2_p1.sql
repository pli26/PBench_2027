select writeaggregation(4, array_agg(subbb.tuid)) as tuid, subbb.gb as gb, sum(subbb.sva) / sum(subbb.cntva) as avgva, sum(subbb.svb) / sum(subbb.cntvb) as avgvb
from (
    select writejoin(3, subb.tuid, s1.tuid) as tuid, subb.gb as gb, subb.sva as sva, subb.svb as svb, subb.cntva as cntva, subb.cntvb as cntvb
    from (
        select writeaggregation(2, array_agg(sub.tuid)) as tuid, sub.gb as gb, sum(sub.va) as sva, sum(sub.vb) as svb, count(sub.va) as cntva, count(sub.vb) as cntvb
        from(
            select writejoin(1, r1.tuid) as tuid, r1.GBATTR as gb, r1.va, r1.vb
            from fp_1 as r1 (tuid, id, ga, gb, gc, hv, va, vb, vc)
        ) as sub
        group by sub.gb
    ) subb, jc_1 as s1 (tuid, jid, c1to1, c1to10, c1to50)
    where subb.gb = c1to10
) subbb
group by subbb.gb;
