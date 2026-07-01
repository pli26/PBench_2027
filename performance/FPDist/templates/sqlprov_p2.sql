select ft.tuid as tuid, r2.tuid as prov
from fp_2 as r2 (tuid, id, ga, gb, gc, hv, va, vb, vc),
    lateral readfilter(1, r2.tuid) as ft(tuid);