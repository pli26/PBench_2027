select
    s_name,
    numwait
from (
    select
        s_name,
        count(*) as numwait
    from (
        select
            s_name
        from
            supplier,
            lineitem l1,
            orders,
            nation
        where
            s_suppkey = l1.l_suppkey
            and o_orderkey = l1.l_orderkey
            and o_orderstatus = 'F'
            and l1.l_receiptdate > l1.l_commitdate
            and exists (
                select 1
                from (
                    select
                        *
                    from
                        lineitem l2
                    where
                        l2.l_orderkey = l1.l_orderkey
                        and l2.l_suppkey <> l1.l_suppkey
                ) as _t
            )
            and not exists (
                select 1
                from (
                    select
                        *
                    from
                        lineitem l3
                    where
                        l3.l_orderkey = l1.l_orderkey
                        and l3.l_suppkey <> l1.l_suppkey
                        and l3.l_receiptdate > l3.l_commitdate
                ) as _t
            )
            and s_nationkey = n_nationkey
            and n_name = 'SAUDI ARABIA'
    ) as _t
    group by
        s_name
    having true
) as _t
order by
    numwait desc,
    s_name
limit all