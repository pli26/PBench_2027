select win.tuid as tuid, r2.tuid as prov
from fp_2 as r2, lateral readwindow(1, r2.tuid) as win(tuid, part, rank);