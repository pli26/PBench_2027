select ga, avg(va) over(order by id) as rkava from fp;
