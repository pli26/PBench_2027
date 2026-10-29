
import os
import json
import argparse
import pandas as pd
import random
from buildProv import buildSQLProv, buildProvSQL, buildProvMapping, buildDDL
def GenJC(sf = 1, tname = 'jc'):

    GenData(sf, tname)

    SSF = sf
    if sf == 0.1:
        SSF = '0_1'
    buildDDL(SSF, tname, ['jid', 'c1to1', 'c1to10', 'c1to50'], 'id')


    cfgs = pd.read_json(f'{os.getcwd()}/cfgs.cfg')
    db = cfgs['provsql']['db']
    buildProvSQL(SSF, tname)
    buildProvMapping(SSF, f'mapping_{tname}', tname, 'id')
    buildSQLProv(SSF, tname, ['jid', 'c1to1', 'c1to10', 'c1to50'])


def GenData(sf = 1, tname = 'default'):
    SF = 1
    if sf != 10:
        SF = 1
    else:
        SF = sf
    Size = int(1000 * SF * 50)

    gn = 1000 * SF
    c1to1 = 1
    c1to10 = 10
    c1to50 = 50

    max = Size * 10

    data = {
        "c1to1": [val for val in range(1, gn + 1) for _ in range(c1to1)] + [val for val in range(max, max + Size - gn * c1to1) for _ in range(1)],
        "c1to10": [val for val in range(1, gn + 1) for _ in range(c1to10)] + [val for val in range(max, max + Size - gn * c1to10) for _ in range(1)],
        "c1to50": [val for val in range(1, gn + 1) for _ in range(c1to50)] + [val for val in range(max, max + Size - gn * c1to50) for _ in range(1)]
    }

    print(len(data['c1to1'] ), len(data['c1to10']), len(data['c1to50']))

    df = pd.DataFrame(data)
    df = df.sample(frac = 1, random_state=random.randint(0, 99999)).reset_index(drop = True)
    df.insert(0, 'id', range(1, len(df) + 1))
    if sf == 0.1:
        os.makedirs(f'{os.getcwd()}/data/sf0_1', exist_ok = True)
        df.to_csv(f'{os.getcwd()}/data/sf0_1/{tname}.csv', index = False)
    else:
        os.makedirs(f'{os.getcwd()}/data/sf{sf}', exist_ok = True)
        df.to_csv(f'{os.getcwd()}/data/sf{sf}/{tname}.csv', index = False)


