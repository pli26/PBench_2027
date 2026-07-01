import pandas as pd
import string
import random
import os
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
import queryUtils as q_util
import fileUtils as f_util
import stringUtils as s_util

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

THIS_BENCHMARK = 'QRCRW'
CURR_PATH = os.getcwd()
p1 = """
with recursive rcr_1(tuid, f, t, d) as (
    select writelog(1, p.tuid) as tuid, p.f, p.t, 1 as d
    from pairs_1 as p
    where p.f <= {RANGE}

    union all

    select writelog(2, r.tuid, p.tuid) as tuid, p.f as f, p.t as t, r.d + 1 as d
    from rcr_1 as r, pairs_1 as p
    where r.t = p.f and r.d < {DEPTH}
)
select writelog(3, r.tuid) as tuid, r.f, r.t, r.d
from rcr_1 as r;
"""
p2 = """
WITH RECURSIVE rcr_2(tuid, prov, f, t, d) as (
     select pp.tuid as tuid, p.tuid as prov, p.f, p.t, 1 as d
     from pairs_2 as p, readlog(1, p.tuid) as pp(tuid)
     union all
     select pp.tuid as tuid, p.tuid as prov, r.t as f, p.f as t, r.d + 1 as d
     from rcr_2 as r, pairs_2 as p, readlog(2, r.tuid, p.tuid) as pp(tuid)
)
select r.prov
from rcr_2 as r, readlog(3, r.tuid) as l(tuid);
"""
post = """
with recursive rcr as (
    select f, t, 1 as d
    from pairs
    where f <= {RANGE}

    union all

    select p.f as f, p.t as t, r.d + 1 as d
    from rcr as r , pairs as p
    where r.t = p.f and r.d < {DEPTH}
)
select * from rcr;
"""

def run(SF = 1):

    qid = 1
    # --------- sqlprov
    f_util.SQLProvPreFile(THIS_BENCHMARK)
    f_util.SQLProvLogSizeFile(THIS_BENCHMARK, ['logaggregation', 'logjoin', 'log0', 'log1', 'log2', 'log3', 'log4'])
    sp1 = p1
    s_util.writeStrToFile(sp1.format(DEPTH=2, RANGE = (int)(10 * SF)), f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql')
    s_util.writeStrToFile(p2, f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql')

    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p1.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)
    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p2.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)

    pos1 = post

    s_util.writeStrToFile(pos1.format(DEPTH=2, RANGE = (int)(10 * SF)), f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql')
    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/capPq{qid}.sql', f_util.SYS_PostgreSQL, isDuckDBBackend=False)
    qid += 1

    sp2 = p1
    s_util.writeStrToFile(sp2.format(DEPTH=3, RANGE = (int)(10 * SF)), f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql')
    s_util.writeStrToFile(p2, f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql')
    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p1.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)
    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p2.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)

    post2 = post
    s_util.writeStrToFile(post2.format(DEPTH=3, RANGE = (int)(10 * SF)), f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql')
    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/capPq{qid}.sql', f_util.SYS_PostgreSQL, isDuckDBBackend=False)


    qid += 1

    sp3 = p1
    s_util.writeStrToFile(sp3.format(DEPTH=4, RANGE = (int)(10 * SF)), f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql')
    s_util.writeStrToFile(p2, f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql')
    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p1.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)
    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p2.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)

    post3 = post
    s_util.writeStrToFile(post3.format(DEPTH=4, RANGE = (int)(10 * SF)), f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql')
    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/capPq{qid}.sql', f_util.SYS_PostgreSQL, isDuckDBBackend=False)

    qid += 1

    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_SQLProv, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_PostgreSQL, 1, qid-1)

if __name__ == "__main__":
    f_util.lodConfig(THIS_BENCHMARK)

    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_SQLProv)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_PostgreSQL)
    SF = 1

    run()