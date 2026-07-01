import pandas as pd
import string
import random
import os
import json
import sys
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
import queryUtils as q_util
import fileUtils as f_util
import stringUtils as s_util

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

THIS_BENCHMARK = 'FPSAgg'
CURR_PATH = os.getcwd()





def run(sf = 1):
    CFGs = f_util.loadJsonConfig(f'{os.getcwd()}/systems.config')

    # havings = ['100', '500', '1000']
    # havings = [str(int(int(h) * sf)) for h in havings]
    GBATTRS = ['ga', 'gb']
    # print(f'Generating queries for scale factor {sf} with having values {havings}\n')

    qid = 1

    for qtmpid in ['1', '2']:
        QTemplate = f_util.readTemplate(f'{CURR_PATH}/templates/q{qtmpid}.sql')
        QTemplate1 = f_util.readTemplate(f'{CURR_PATH}/templates/sp{qtmpid}_p1.sql')
        QTemplate2 = f_util.readTemplate(f'{CURR_PATH}/templates/sp{qtmpid}_p2.sql')
        having = ''
        for gbAttr in GBATTRS:
            gSQL = s_util.buildSQLFromTemplate(QTemplate, ['fp', 'jc', 'HAVING_VALUE', 'GBATTR'], [f'fp use provenance(id)', f'jc use provenance(jid)', f'{having}', gbAttr])

            s_util.writeStrToFile(f'provenance of ({gSQL});', f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}.sql')
            # ------------ rewrite
            q_util.gprom_rewrite(f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql', isDuckDBBackend=False)
            q_util.gprom_rewrite(f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql', isDuckDBBackend=True)

            # ------------ make executable
            q_util.make_executable_gprom_capture(f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}.sql', isDuckDBBackend=False)
            q_util.make_executable_gprom_capture(f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}.sql', isDuckDBBackend=True)

            q_util.make_executable_gprom_capture_res_row_cnt(f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}Cnt.sql', f'FPVPSPT_{qid}', isDuckDBBackend=False)
            q_util.make_executable_gprom_capture_res_row_cnt(f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}Cnt.sql', f'FPVPSDT_{qid}', isDuckDBBackend=True)

            # ---------smd
            sSQL = s_util.buildSQLFromTemplate(QTemplate, ['HAVING_VALUE', 'GBATTR'], [f'{having}', gbAttr])
            s_util.writeStrToFile(f'{sSQL};', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/q{qid}.sql')
            # -- Phase I
            q_util.make_executable_smd_p1(sSQL, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p1.sql')
            # -- export table
            tableList = q_util.duckdbGetAllLineageTables(CFGs[f_util.SYS_SmokedDuck + 'pre']['duckdb_bin'], CFGs[f_util.SYS_SmokedDuck + 'pre']['database_path'], sSQL + ";")
            q_util.make_executable_smd_export(tableList, sSQL, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_export.sql', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}')
            # -- import
            q_util.make_executable_smd_import(tableList, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_import.sql', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}')
            # -- Phase II
            LINQ = q_util.duckdbGetLineageQuery(CFGs[f_util.SYS_SmokedDuck + 'pre']['duckdb_bin'], CFGs[f_util.SYS_SmokedDuck + 'pre']['database_path'], sSQL + ";")
            q_util.make_executable_smd_p2(LINQ, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p2.sql')


            #--------- provsql
            pSQL = s_util.buildSQLFromTemplate(QTemplate, ['HAVING_VALUE', 'GBATTR'], [ f'{having}', gbAttr])
            s_util.writeStrToFile(f'{pSQL};', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}.sql')
            q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}.sql', f_util.SYS_ProvSQL, isDuckDBBackend=False)

            # --------- sqlprov
            f_util.SQLProvPreFile(THIS_BENCHMARK)
            f_util.SQLProvLogSizeFile(THIS_BENCHMARK, ['logaggregation', 'logjoin', 'logfilter'])


            spSQL1 = s_util.buildSQLFromTemplate(QTemplate1, ['HAVING_VALUE', 'GBATTR'], [f'{having}', gbAttr])
            spSQL2 = s_util.buildSQLFromTemplate(QTemplate2, ['HAVING_VALUE', 'GBATTR'], [f'{having}', gbAttr])
            s_util.writeStrToFile(f'{spSQL1};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql')
            s_util.writeStrToFile(f'{spSQL2};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql')

            q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p1.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)
            q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p2.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)

            # ------------ postgresql
            pgSQL = s_util.buildSQLFromTemplate(QTemplate, ['HAVING_VALUE', 'GBATTR'], [f'{having}', gbAttr])
            s_util.writeStrToFile(f'{pgSQL};', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql')
            q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/capPq{qid}.sql', f_util.SYS_PostgreSQL, isDuckDBBackend=False)

            # ------------ duckdb
            dSQL = s_util.buildSQLFromTemplate(QTemplate, ['HAVING_VALUE', 'GBATTR'], [f'{having}', gbAttr])
            s_util.writeStrToFile(f'{dSQL};', f'{CURR_PATH}/{f_util.SYS_DuckDB}/q{qid}.sql')
            q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_DuckDB}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_DuckDB}/capDq{qid}.sql', f_util.SYS_DuckDB, isDuckDBBackend=True)

            qid += 1

    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_GProM, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_ProvSQL, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_SmokedDuck, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_SQLProv, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_PostgreSQL, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_DuckDB, 1, qid-1)









if __name__ == "__main__":
    f_util.lodConfig(THIS_BENCHMARK)

    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_GProM)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_ProvSQL)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_SmokedDuck)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_SQLProv)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_PostgreSQL)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_DuckDB)
    sf = 1
    ap = argparse.ArgumentParser(description = 'Provenance Benchmarks')
    ap.add_argument('--sf', type=str, default=1.0, help='Scale factor: 0_1(0.1), 1, or 10')
    args = ap.parse_args()
    if args.sf == '0_1':
        sf = 0.1
    else:
        sf = int(args.sf)
    run(sf)
