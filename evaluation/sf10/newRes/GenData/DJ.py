
import os
import json
import argparse
import pandas as pd
import random
from buildProv import buildSQLProv, buildProvSQL, buildProvMapping, buildDDL
def GenDD(sf = 1, tname = 'dj'):

    GenData(sf, tname)
    SSF = sf
    if sf == 0.1:
        SSF = '0_1'
    buildDDL(SSF, tname, ['id', 'da', 'db', 'dc', 'hv'], 'id')


    cfgs = pd.read_json(f'{os.getcwd()}/cfgs.cfg')
    db = cfgs['provsql']['db']
    buildProvSQL(SSF, tname)
    buildProvMapping(SSF, f'mapping_{tname}', tname, 'id')
    buildSQLProv(SSF, tname, ['id', 'da', 'db', 'dc', 'hv'])


def GenData(sf = 1, tname = 'default'):

    Size = int(10000 * sf)

    da = 1
    db = 50
    dc = 1000
    max = Size * 10

    data = {
        "da": [val for val in range(1, da + 1) for _ in range(Size // da)],
        "db": [val for val in range(1, db + 1) for _ in range(Size // db)],
        "dc": [val for val in range(1, dc + 1) for _ in range(Size // dc)],
        "hv": [val for val in range(1, dc + 1) for _ in range(Size // dc)]
    }

    print(len(data['da'] ), len(data['db']), len(data['dc']))

    df = pd.DataFrame(data)
    df = df.sample(frac = 1, random_state=random.randint(0, 99999)).reset_index(drop = True)
    df.insert(0, 'id', range(1, len(df) + 1))
    if sf == 0.1:
        os.makedirs(f'{os.getcwd()}/data/sf0_1', exist_ok = True)
        df.to_csv(f'{os.getcwd()}/data/sf0_1/{tname}.csv', index = False)
    else:
        os.makedirs(f'{os.getcwd()}/data/sf{sf}', exist_ok = True)
        df.to_csv(f'{os.getcwd()}/data/sf{sf}/{tname}.csv', index = False)


