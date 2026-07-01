import pandas as pd
import random
import os

from buildProv import buildSQLProv, buildProvSQL, buildProvMapping, buildDDL
def GenFP(sf = 1):
    GenData(sf)
    cfgs = pd.read_json(f'{os.getcwd()}/cfgs.cfg')
    db = cfgs['provsql']['db']

    SSF = sf
    if sf == 0.1:
        SSF = '0_1'
    buildDDL(SSF, 'fp', ['id', 'ga', 'gb', 'gc', 'hv', 'va', 'vb', 'vc'], 'id')
    buildProvSQL(SSF, 'fp')
    buildProvMapping(SSF, 'mapping_fp', 'fp', 'id')
    buildSQLProv(SSF, 'fp', ['id', 'ga', 'gb', 'gc', 'hv', 'va', 'vb', 'vc'])




def GenData(sf = 1):

    print(f'Generating data for scale factor {sf} for fix provenance\n')
    Size = (int) (10000000 * sf)

    ga = list(range(1, Size // 1000000 + 1))
    gb = list(range(1, Size // 10000 + 1))
    gc = list(range(1, Size // 10 + 1))

    print(f'distinct val: {len(ga)}')
    print(f'distinct val: {len(gb)}')
    print(f'distinct val: {len(gc)}')


    data = {"ga": [val for val in ga for _ in range(Size // len(ga))],
            "gb": [val for val in gb for _ in range(Size // len(gb))],
            "gc": [val for val in gc for _ in range(Size // len(gc))],
            "hv": [val for val in gb for _ in range(Size // len(gb))],
            "va": [val for val in gb for _ in range(Size // len(gb))],
            "vb": [val for val in gb for _ in range(Size // len(gb))],
            "vc": [val for val in gb for _ in range(Size // len(gb))]}
    df = pd.DataFrame(data)
    df = df.sample(frac = 1, random_state=random.randint(0, 99999)).reset_index(drop = True)
    df.insert(0, 'id', range(1, len(df) + 1))

    if sf == 0.1:
        os.makedirs(f'{os.getcwd()}/data/sf0_1', exist_ok = True)
        df.to_csv(f'{os.getcwd()}/data/sf0_1/fp.csv', index = False)
    else:
        os.makedirs(f'{os.getcwd()}/data/sf{sf}', exist_ok = True)
        df.to_csv(f'{os.getcwd()}/data/sf{sf}/fp.csv', index = False)

