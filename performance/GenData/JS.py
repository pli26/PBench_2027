
import os
import json
import argparse
import pandas as pd
import random
from buildProv import buildSQLProv, buildProvSQL, buildProvMapping, buildDDL
def GenJS(sf = 1, tname = 'js'):

    GenData(sf, tname)
    SSF = sf
    if sf == 0.1:
        SSF = '0_1'
    buildDDL(SSF, tname, ['jid', 'p1', 'p10', 'p50'], 'jid')


    cfgs = pd.read_json(f'{os.getcwd()}/cfgs.cfg')
    db = cfgs['provsql']['db']
    buildProvSQL(SSF, tname)
    buildProvMapping(SSF, f'mapping_{tname}', tname, 'jid')
    buildSQLProv(SSF, tname, ['jid', 'p1', 'p10', 'p50'])


def GenData(sf = 1, tname = 'default'):
    SF = sf
    if sf < 1:
        SF = 1
    Size = int(1000 * SF * 50 // 2)
    print(f"JS size: {Size}")

    gn = 1000 * SF

    p1 = 10 * SF
    p10 = 100 * SF
    p50 = 500 * SF

    print(f"P1: {p1}, p10: {p10}, p50 {p50}")
    max = Size * 10

    p1  =  [val for val in range(1, p1 + 1) for _ in range(10)]
    p10 =  [val for val in range(1, p10 + 1) for _ in range(10)]
    p50 =  [val for val in range(1, p50 + 1) for _ in range(10)]

    data = {
        "p1": p1 + [val for val in range(max, max + Size - len(p1)) for _ in range(1)],
        "p10": p10 + [val for val in range(max, max + Size - len(p10)) for _ in range(1)],
        "p50": p50 + [val for val in range(max, max + Size - len(p50)) for _ in range(1)]
    }
    print(len(data['p1'] ), len(data['p10']), len(data['p50']))

    df = pd.DataFrame(data)
    df = df.sample(frac = 1, random_state=random.randint(0, 99999)).reset_index(drop = True)
    df.insert(0, 'id', range(1, len(df) + 1))

    if sf == 0.1:
        os.makedirs(f'{os.getcwd()}/data/sf0_1', exist_ok = True)
        df.to_csv(f'{os.getcwd()}/data/sf0_1/{tname}.csv', index = False)
    else:
        os.makedirs(f'{os.getcwd()}/data/sf{sf}', exist_ok = True)
        df.to_csv(f'{os.getcwd()}/data/sf{sf}/{tname}.csv', index = False)


