
import os
import json
import argparse
import pandas as pd
import random
from buildProv import buildSQLProv, buildProvSQL, buildProvMapping, buildDDL
def GenJJ(sf = 1, tname = 'jjj', idx = 'jjjid'):

    GenData(sf, tname)
    SSF = sf
    if sf == 0.1:
        SSF = '0_1'
    buildDDL(SSF, tname, [idx, 'cc1', 'cc2', 'cc5', 'cc10'], idx)


    cfgs = pd.read_json(f'{os.getcwd()}/cfgs.cfg')
    db = cfgs['provsql']['db']
    buildProvSQL(SSF, tname)
    buildProvMapping(SSF, f'mapping_{tname}', tname, idx)
    buildSQLProv(SSF, tname, [idx, 'cc1', 'cc2', 'cc5', 'cc10'])


def GenData(sf = 1, tname = 'default'):
    SF = sf
    if sf < 1:
        SF = 1
    Size = int(1000 * SF * 10)




    gn = 1000 * SF
    c1 = 1
    c2 = 2
    c5 = 5
    c10 = 10

    max = Size * 10

    p1  =  [val for val in range(1, gn + 1) for _ in range(c1)]
    p2 =    [val for val in range(1, gn + 1) for _ in range(c2)]
    p10 =  [val for val in range(1, gn + 1) for _ in range(c5)]
    p50 =  [val for val in range(1, gn + 1) for _ in range(c10)]

    data = {
        "c1": p1 + [val for val in range(max, max + Size - len(p1)) for _ in range(1)],
        "c2": p2 + [val for val in range(max, max + Size - len(p2)) for _ in range(1)],
        "c5": p10 + [val for val in range(max, max + Size - len(p10)) for _ in range(1)],
        "c10": p50 + [val for val in range(max, max + Size - len(p50)) for _ in range(1)]
    }
    print(len(data['c1'] ), len(data['c2']), len(data['c5']), len(data['c10']))

    df = pd.DataFrame(data)
    df = df.sample(frac = 1, random_state=random.randint(0, 99999)).reset_index(drop = True)
    df.insert(0, 'jjid', range(1, len(df) + 1))
    if sf == 0.1:
        os.makedirs(f'{os.getcwd()}/data/sf0_1', exist_ok = True)
        df.to_csv(f'{os.getcwd()}/data/sf0_1/{tname}.csv', index = False)
    else:
        os.makedirs(f'{os.getcwd()}/data/sf{sf}', exist_ok = True)
        df.to_csv(f'{os.getcwd()}/data/sf{sf}/{tname}.csv', index = False)


