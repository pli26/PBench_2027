drop view if exists revenue0;
create view revenue0 (supplier_no, total_revenue) as
	select
		l_suppkey as l_suppkey,
		sum(l_extendedprice * (1 - l_discount)) as sum
	from
        (
            select
                l_suppkey as l_suppkey,
                l_extendedprice as l_extendedprice,
                l_discount as l_discount
            from
        		lineitem l
        	where
        		l_shipdate >= date '1996-01-01'
        		and l_shipdate < date '1996-01-01' + interval '3' month
        ) as _t
	group by
		l_suppkey
    having true;