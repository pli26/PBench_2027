import pandas as pd
import random
import os








from buildProv import buildSQLProv, buildProvSQL, buildProvMapping, buildDDL
def GenVPGN(sf = 1, group_num = 10, tname = 'vpgn10'):
    SSF = sf
    if sf == 0.1:
        SSF = '0_1'

    GenData(sf, group_num, tname)
    buildDDL(SSF, tname, ['id', 'ga', 'va', 'vb'], 'id')
    cfgs = pd.read_json(f'{os.getcwd()}/cfgs.cfg')
    db = cfgs['provsql']['db']
    buildProvSQL(SSF, tname)
    buildProvMapping(SSF, f'mapping_{tname}', tname, 'id')
    buildSQLProv(SSF, tname, ['id', 'ga', 'va', 'vb'])


def GenData(sf = 1, group_num = 10, tname = 'default'):

    Size = int(1000 * sf * group_num)
    gs = int(1000 * sf)

    print(f'Generating data for scale factor {sf} for vary prov  group number {group_num}, group size {gs} \n')

    gn = list(range(1, Size // gs + 1))


    data = {"ga": [val for val in gn for _ in range(Size // len(gn))],
            "va": [val for val in gn for _ in range(Size // len(gn))],
            "vb": [val for val in gn for _ in range(Size // len(gn))]}
    df = pd.DataFrame(data)
    df = df.sample(frac = 1, random_state=random.randint(0, 99999)).reset_index(drop = True)
    df.insert(0, 'id', range(1, len(df) + 1))
    if sf == 0.1:
        os.makedirs(f'{os.getcwd()}/data/sf0_1', exist_ok = True)
        df.to_csv(f'{os.getcwd()}/data/sf0_1/{tname}.csv', index = False)
    else:
        os.makedirs(f'{os.getcwd()}/data/sf{sf}', exist_ok = True)

        df.to_csv(f'{os.getcwd()}/data/sf{sf}/{tname}.csv', index = False)


