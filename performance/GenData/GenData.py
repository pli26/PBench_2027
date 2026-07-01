import os
import json
import argparse
from FP import GenFP as genFP
from VPGN import GenVPGN as genVPGN
from VPGS import GenVPGS as genVPGS
from JC import GenJC as genJC
from JS import GenJS as genJS
from DJ import GenDD as genDD
from JJ import GenJJ as genJJ
from JJJ import GenJJ as genJJJ
allowed_scale_factors = [0.1 , 1, 10]


reduced = """
drop table if exists fp1 cascade;
create table fp1 as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 1;

-- reduced to 1%
drop table if exists fp2 cascade;
create table fp2 as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 100;

-- reduced to 20%
drop table if exists fp3 cascade;
create table fp3 as
select id, ga, gb, gc, hv, va, vb, vc
from (
    select id, ga, gb, gc, hv, va, vb, vc, row_number() over (partition by gb order by id) as rn
    from fp
) t
where t.rn <= 2000;

analyze;
"""

pairs = """
CREATE TABLE IF NOT EXISTS pairs (
    f INT,
    t INT
);
INSERT INTO pairs (f, t)
SELECT
    (random() * 1000 * SSFF)::int AS f,
    (random() * 1000 * SSFF)::int AS t
FROM generate_series(1, 100000 * SSFF) s(i);

-- Optional: Add an index to make the recursive join fast
CREATE INDEX idx_pair_iddx ON pairs(f);
"""

def gen(sf):
#     genFP(sf)
# 
#     genVPGN(sf, group_num = 100, tname = f'vpgn100')
#     genVPGN(sf, group_num = 1000, tname = f'vpgn1k')
#     genVPGN(sf, group_num = 10000, tname = f'vpgn10k')
# 
#     genVPGS(sf, group_size = 100, tname = f'vpgs100')
#     genVPGS(sf, group_size = 1000, tname = f'vpgs1k')
#     genVPGS(sf, group_size = 10000, tname = f'vpgs10k')
# 
    genJC(sf, tname = f'jc')
    genJS(sf, tname = f'js')
    genDD(sf, tname = f'dj1')
    genDD(sf, tname = f'dj2')
    genJJ(sf, tname = f'jj')
    genJJJ(sf, tname = f'jjj')

    SF = sf
    if sf == 0.1:
        SF = '0_1'
    with open(f'{os.getcwd()}/data/sf{SF}/reducedLin.sql', 'w') as ff:
        ff.write(f'{reduced}')
    with open(f'{os.getcwd()}/data/sf{SF}/pairs.sql', 'w') as ff:
        ff.write(f'{pairs.replace("SSFF", str(sf))}')

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Generate data for performance')
    ap.add_argument('--SF', type = int, help = "Scale factor for  data generation", required = False, default = 10)

    args = ap.parse_args()

    sf = args.SF
    if sf == 0:
        sf = 0.1
    # sf = 0.1
    if sf not in allowed_scale_factors:
        print(f"Scale factor {sf} is not allowed. Allowed scale factors are: {allowed_scale_factors}\nUse the following: \n \t --SF 0 for scale factor 0.1\n \t --SF 1 for scale factor 1, and\n \t --SF 10 for scale factor 10")
        exit()
    print(f"Scale Factor: {sf}")
    gen(sf)
