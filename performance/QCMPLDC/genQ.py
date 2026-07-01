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

THIS_BENCHMARK = 'QCMPLDC'
CURR_PATH = os.getcwd()

def run():
    CFGs = f_util.loadJsonConfig(f'{os.getcwd()}/systems.config')
    qid = 1

    # for qid in range(1, 4):
    while qid <= 3:
        QTemplate = f_util.readTemplate(f'{CURR_PATH}/templates/q{qid}.sql')
        QTemplate1 = f_util.readTemplate(f'{CURR_PATH}/templates/sp{qid}_p1.sql')
        QTemplate2 = f_util.readTemplate(f'{CURR_PATH}/templates/sp{qid}_p2.sql')

        # -- gprom
        gSQL = s_util.buildSQLFromTemplate(QTemplate, ['vpgn1k', 'jc'], [f'vpgn1k use provenance(id)', 'jc use provenance(jid)'])

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
        sSQL = QTemplate
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
        # --------- provsql
        pSQL = QTemplate
        s_util.writeStrToFile(f'{pSQL};', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}.sql')
        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}.sql', f_util.SYS_ProvSQL, isDuckDBBackend=False)

        # --------- sqlprov
        f_util.SQLProvPreFile(THIS_BENCHMARK)
        f_util.SQLProvLogSizeFile(THIS_BENCHMARK, ['logaggregation', 'logjoin'])


        spSQL1 = QTemplate1
        spSQL2 = QTemplate2
        s_util.writeStrToFile(f'{spSQL1};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql')
        s_util.writeStrToFile(f'{spSQL2};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql')

        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p1.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)
        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p2.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)

        # ----------- postgresql
        pgSQL = QTemplate
        s_util.writeStrToFile(f'{pgSQL};', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql')
        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/capPq{qid}.sql', f_util.SYS_PostgreSQL, isDuckDBBackend=False)

        # ----------- duckdb
        dSQL = QTemplate
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