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

THIS_BENCHMARK = 'FPSDist'
CURR_PATH = os.getcwd()

def run():
    CFGs = f_util.loadJsonConfig(f'{os.getcwd()}/systems.config')
    SMDCFG = CFGs[f_util.SYS_SmokedDuck + 'pre']
    qid = 1

    D1s = ['da', 'db', 'dc']
    D2s = ['da', 'db', 'dc']
    for qtmpid in ['1', '2']:

        QTemplate = f_util.readTemplate(f'{CURR_PATH}/templates/q{qtmpid}.sql')
        QTemplate1 = f_util.readTemplate(f'{CURR_PATH}/templates/sp{qtmpid}_p1.sql')
        QTemplate2 = f_util.readTemplate(f'{CURR_PATH}/templates/sp{qtmpid}_p2.sql')

        for d1 in D1s:
            for d2 in D2s:
                gSQL = s_util.buildSQLFromTemplate(QTemplate, ['TBL1', 'TBL2', 'DISTINCT_ATTRIBUTE_A', 'DISTINCT_ATTRIBUTE_B',], [f'dj1 use provenance(id)', f'dj2 use provenance(id)', f'{d1}', f'{d2}'])

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
                # sSQL = s_util.buildSQLFromTemplate(QTemplate, ['TBL1', 'TBL2', 'DISTINCT_ATTRIBUTE_A', 'DISTINCT_ATTRIBUTE_B'], ['dj1', 'dj2',f'{d1}', f'{d2}'])
                # s_util.writeStrToFile(f'{sSQL};', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/q{qid}.sql')
                # q_util.make_executable_smd_pO1(sSQL, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p1.sql')
                # print(SMDCFG["duckdb_bin"] + f'--> {SMDCFG["database_path"]}' + f'--> {sSQL}')
                # q_util.make_executable_smd_pO2(SMDCFG["duckdb_bin"], SMDCFG["database_path"], sSQL, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p2.sql')

                # --------- provsql
                pSQL = s_util.buildSQLFromTemplate(QTemplate, ['TBL1', 'TBL2', 'DISTINCT_ATTRIBUTE_A', 'DISTINCT_ATTRIBUTE_B'], ['dj1', 'dj2', f'{d1}', f'{d2}'])
                s_util.writeStrToFile(f'{pSQL};', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}.sql')
                q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}.sql', f_util.SYS_ProvSQL, isDuckDBBackend=False)

                # --------- sqlprov
                f_util.SQLProvPreFile(THIS_BENCHMARK)
                f_util.SQLProvLogSizeFile(THIS_BENCHMARK, ['logaggregation', 'logjoin', 'logfilter'])


                spSQL1 = s_util.buildSQLFromTemplate(QTemplate1, ['DISTINCT_ATTRIBUTE_A', 'DISTINCT_ATTRIBUTE_B'], [f'{d1}', f'{d2}'])
                spSQL2 = s_util.buildSQLFromTemplate(QTemplate2, ['DISTINCT_ATTRIBUTE_A', 'DISTINCT_ATTRIBUTE_B'], [f'{d1}', f'{d2}'])
                s_util.writeStrToFile(f'{spSQL1};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql')
                s_util.writeStrToFile(f'{spSQL2};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql')

                q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p1.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)
                q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p2.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)

                # ------------ postgresql
                pgSQL = s_util.buildSQLFromTemplate(QTemplate, ['TBL1', 'TBL2', 'DISTINCT_ATTRIBUTE_A', 'DISTINCT_ATTRIBUTE_B'], ['dj1', 'dj2', f'{d1}', f'{d2}'])
                s_util.writeStrToFile(f'{pgSQL};', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql')
                q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/capPq{qid}.sql', f_util.SYS_PostgreSQL, isDuckDBBackend=False)

                # ------------ duckdb
                dSQL = s_util.buildSQLFromTemplate(QTemplate, ['TBL1', 'TBL2', 'DISTINCT_ATTRIBUTE_A', 'DISTINCT_ATTRIBUTE_B'], ['dj1', 'dj2', f'{d1}', f'{d2}'])
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
    run()