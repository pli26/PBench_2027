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

THIS_BENCHMARK = 'VPJJJ'
CURR_PATH = os.getcwd()





def run():
    CFGs = f_util.loadJsonConfig(f'{os.getcwd()}/systems.config')
    gbAttr = 'ga'
    selectClause = 'avg(va) as ava, avg(vb) as avb'
    table = 'vpgn1k'
    joinedtable = 'jc'
    joinC = 'ga = p10'
    jjoinC = 'ga = c5'
    qid = 1
    QTemplate = f_util.readTemplate(f'{CURR_PATH}/templates/q.sql')
    selectC = f'{gbAttr}, ' + selectClause
    # ------------
    # gprom
    # ------------
    gSQL = s_util.buildSQLFromTemplate(QTemplate,
        ['FROM_TABLE', 'J1', "JJ2", 'JJJ3'],
        [f'vpgn1k use provenance(id)', f'js use provenance(jid)', 'jj use provenance(jjid)', 'jjj use provenance(jjjid)'])

    s_util.writeStrToFile(f'provenance of ({gSQL});', f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}.sql')
    # ------------ rewrite
    q_util.gprom_rewrite(f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql', isDuckDBBackend=False)
    q_util.gprom_rewrite(f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql', isDuckDBBackend=True)

    # ------------ make executable
    q_util.make_executable_gprom_capture(f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}.sql', isDuckDBBackend=False)
    q_util.make_executable_gprom_capture(f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}.sql', isDuckDBBackend=True)

    q_util.make_executable_gprom_capture_res_row_cnt(f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}Cnt.sql', f'FPVPSPT_{qid}', isDuckDBBackend=False)
    q_util.make_executable_gprom_capture_res_row_cnt(f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}Cnt.sql', f'FPVPSDT_{qid}', isDuckDBBackend=True)

    # --------------
    # provsql
    # --------------
    f_util.ProvSQLExt(THIS_BENCHMARK, CFGs[f_util.SYS_ProvSQL])
    pSQL = s_util.buildSQLFromTemplate(QTemplate,
        ['FROM_TABLE', 'J1', 'JJ2', 'JJJ3'],
        [f'vpgn1k', f'js', 'jj', 'jjj'])
    s_util.writeStrToFile(f'{pSQL};', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}.sql')
    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}.sql', f_util.SYS_ProvSQL, isDuckDBBackend=False)

    # --------------
    # smokedduck
    # --------------
    sSQL = s_util.buildSQLFromTemplate(QTemplate,
        ['FROM_TABLE', 'J1', 'JJ2', 'JJJ3'],
        [f'vpgn1k', f'js', 'jj', 'jjj'])
    s_util.writeStrToFile(f'{sSQL};', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/q{qid}.sql')
    # -- phase I
    q_util.make_executable_smd_p1(f'{sSQL};', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p1.sql')
    # -- export table
    tableList = q_util.duckdbGetAllLineageTables(CFGs[f_util.SYS_SmokedDuck + 'pre']['duckdb_bin'], CFGs[f_util.SYS_SmokedDuck + 'pre']['database_path'], sSQL + ";")
    q_util.make_executable_smd_export(tableList, sSQL, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_export.sql', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}')
    # -- import table
    q_util.make_executable_smd_import(tableList, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_import.sql', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}')
    # -- Phase II
    LINQ = q_util.duckdbGetLineageQuery(CFGs[f_util.SYS_SmokedDuck + 'pre']['duckdb_bin'], CFGs[f_util.SYS_SmokedDuck + 'pre']['database_path'], sSQL + ";")
    q_util.make_executable_smd_p2(f'{LINQ};', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p2.sql')
    # ------------
    # sqlprov
    # ------------
    f_util.SQLProvPreFile(THIS_BENCHMARK)
    f_util.SQLProvLogSizeFile(THIS_BENCHMARK, ['logjoin', 'logaggregation'])

    QTemplate1 = f_util.readTemplate(f'{CURR_PATH}/templates/sqlprov_p1.sql')
    QTemplate2 = f_util.readTemplate(f'{CURR_PATH}/templates/sqlprov_p2.sql')

    spSQL1 = QTemplate1
    spSQL2 = QTemplate2
    s_util.writeStrToFile(f'{spSQL1};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql')
    s_util.writeStrToFile(f'{spSQL2};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql')

    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p1.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)
    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p2.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)

    # --------------
    # postgreSQL
    # --------------
    pgSQL = s_util.buildSQLFromTemplate(QTemplate,
        ['FROM_TABLE', 'J1', 'JJ2', 'JJJ3'],
        [f'vpgn1k', f'js', 'jj', 'jjj'])
    s_util.writeStrToFile(f'{pgSQL};', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql')
    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/capPq{qid}.sql', f_util.SYS_PostgreSQL, isDuckDBBackend=False)

    # --------------
    # duckdb
    # --------------
    duckSQL = s_util.buildSQLFromTemplate(QTemplate,
        ['FROM_TABLE', 'J1', 'JJ2', 'JJJ3'],
        [f'vpgn1k', f'js', 'jj', 'jjj'])
    s_util.writeStrToFile(f'{duckSQL};', f'{CURR_PATH}/{f_util.SYS_DuckDB}/q{qid}.sql')
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