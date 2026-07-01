select GBATTR, avg(va) as ava, avg(vb) as avb from fp join jc on GBATTR = c1to10 group by GBATTR 
