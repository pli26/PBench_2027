select ga, avg(va) from vpgn100 v where exists (select 1 from jc j1 where v.ga = j1.c1to10) group by ga
