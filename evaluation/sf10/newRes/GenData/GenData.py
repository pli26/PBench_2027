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
allowed_scale_factors = [0.1, 1, 10]

def gen(sf = 1):
    genFP(sf)

    genVPGN(sf, group_num = 100, tname = f'vpgn100')
    genVPGN(sf, group_num = 1000, tname = f'vpgn1k')
    genVPGN(sf, group_num = 10000, tname = f'vpgn10k')

    genVPGS(sf, group_size = 100, tname = f'vpgs100')
    genVPGS(sf, group_size = 1000, tname = f'vpgs1k')
    genVPGS(sf, group_size = 10000, tname = f'vpgs10k')

    genJC(sf, tname = f'jc')
    genJS(sf, tname = f'js')
    genDD(sf, tname = f'dj1')
    genDD(sf, tname = f'dj2')
    genJJ(sf, tname = f'jj')
    genJJJ(sf, tname = f'jjj')

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='Generate data for performance')
    ap.add_argument('--SF', type = int, help = "Scale factor for  data generation", required = False, default = 1)

    args = ap.parse_args()

    sf = args.SF
    if sf == 0:
        sf = 0.1
    # sf = 0.1
    if sf not in allowed_scale_factors:
        print(f"Scale factor {sf} is not allowed. Allowed scale factors are: {allowed_scale_factors}")
        exit()
    gen(sf)