import os
import json
import argparse
import pandas as pd
import random
from buildProv import buildSQLProv, buildProvSQL, buildProvMapping, buildDDL
def GenRCR(sf = 1, tname = 'rcr'):

    GenData(sf, tname)
    buildDDL(tname, ['id', 'f', 't'], 'id')


    cfgs = pd.read_json(f'{os.getcwd()}/cfgs.cfg')
    buildSQLProv(tname, ['id', 'f', 't'])


def GenData(sf = 1, tname = 'default'):
    # work as a foreign key,
    sf = 1
    SIZE = 1000000 * sf
    # SIZE = 10
    f = []
    t = []

    val = 1
    for i in range(SIZE // 2):
        f.append(val)
        t.append(val + 1)
        val += 1


    for i in range(SIZE // 2):
        f.append(val)
        t.append(val - 1)
        val -= 1
    data = {
        "f": f,
        "t": t
    }
    print(f)
    print(t)
    for id in range(len(f)):
        if id < len(f) // 2:
            if f[id] != t[id] - 1:
                print(f'id {id} has different f and t value {f[id]} and {t[id]}')
        else:
            if f[id] != t[id] + 1:
                print(f'id {id} has different f and t value {f[id]} and {t[id]}')
    print(len(data['f'] ), len(data['t']))

    df = pd.DataFrame(data)
    df = df.sample(frac = 1, random_state=random.randint(0, 99999)).reset_index(drop = True)
    df.insert(0, 'id', range(1, len(df) + 1))
    os.makedirs(f'{os.getcwd()}/data/sf{sf}', exist_ok = True)
    df.to_csv(f'{os.getcwd()}/data/sf{sf}/{tname}.csv', index = False)

if __name__ == "__main__":
    GenRCR()