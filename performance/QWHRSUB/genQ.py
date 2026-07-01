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

THIS_BENCHMARK = 'QWHRSUB'
CURR_PATH = os.getcwd()

def run():
    CFGs = f_util.loadJsonConfig(f'{os.getcwd()}/systems.config')

    qid = 1
    while qid < 4:
        QTemplate = f_util.readTemplate(f'{CURR_PATH}/templates/q{qid}.sql')
        GQL = s_util.buildSQLFromTemplate(QTemplate, ['vpgn100', 'jc', 'js'], ['vpgn100 use provenance(id)', 'jc use provenance(jid)', 'js use provenance(jid)'])
        s_util.writeStrToFile(f'provenance of({GQL});', f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}.sql')
        # rewrite
        q_util.gprom_rewrite(f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql', isDuckDBBackend=False)
        q_util.gprom_rewrite(f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql', isDuckDBBackend=True)
        # ------------ make executable
        q_util.make_executable_gprom_capture(f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}.sql', isDuckDBBackend=False)
        q_util.make_executable_gprom_capture(f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}.sql', isDuckDBBackend=True)

        q_util.make_executable_gprom_capture_res_row_cnt(f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}Cnt.sql', f'FPVPSPT_{qid}', isDuckDBBackend=False)
        q_util.make_executable_gprom_capture_res_row_cnt(f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}Cnt.sql', f'FPVPSDT_{qid}', isDuckDBBackend=True)


        QTemplate1 = f_util.readTemplate(f'{CURR_PATH}/templates/sp{qid}_p1.sql')
        QTemplate2 = f_util.readTemplate(f'{CURR_PATH}/templates/sp{qid}_p2.sql')

    # --------- sqlprov
        f_util.SQLProvPreFile(THIS_BENCHMARK)
        f_util.SQLProvLogSizeFile(THIS_BENCHMARK, ['logaggregation', 'logjoin'])


        spSQL1 = QTemplate1
        spSQL2 = QTemplate2
        s_util.writeStrToFile(f'{spSQL1};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql')
        s_util.writeStrToFile(f'{spSQL2};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql')

        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p1.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)
        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p2.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)
    #-------------SMD

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


        # QTemplate = f_util.readTemplate(f'{CURR_PATH}/templates/q.sql')
    # ----------- postgresql
        s_util.writeStrToFile(f'{QTemplate};', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql')
        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/capPq{qid}.sql', f_util.SYS_PostgreSQL, isDuckDBBackend=False)

        # ----------- duckdb
        s_util.writeStrToFile(f'{QTemplate};', f'{CURR_PATH}/{f_util.SYS_DuckDB}/q{qid}.sql')
        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_DuckDB}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_DuckDB}/capDq{qid}.sql', f_util.SYS_DuckDB, isDuckDBBackend=True)
        qid += 1

    existsConditions = ['exists(select 1 from jc j1 where F0_0.ga = j1.c1to10)',
                        'exists(select 1 from jc j1 where F0_0.ga = j1.c1to10) and exists(select 1 from jc j2 where F0_0.ga = j2.c1to10)',
                        'exists(select 1 from jc j1 where F0_0.ga = j1.c1to10) and exists(select 1 from jc j2 where F0_0.ga = j2.c1to10) and exists(select 1 from jc j3 where F0_0.ga = j3.c1to10)']
    
    SpecialTMP = f_util.readTemplate(f'{CURR_PATH}/templates/GProMSpecial.sql')
    specialId = qid 
    for condIdx in range(len(existsConditions)):
        # specialId = qid + condIdx 
        cond = existsConditions[condIdx]
        GSSQL = SpecialTMP.replace('EXISTS_CONDITIONS', cond)
        s_util.writeStrToFile(f'{GSSQL}', f'{CURR_PATH}/{f_util.SYS_GProM}/q{specialId}.sql')
        q_util.make_executable_gprom_capture(f'{CURR_PATH}/{f_util.SYS_GProM}/q{specialId}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{specialId}.sql', isDuckDBBackend=False)
        q_util.make_executable_gprom_capture(f'{CURR_PATH}/{f_util.SYS_GProM}/q{specialId}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{specialId}.sql', isDuckDBBackend=True)
        q_util.make_executable_gprom_capture_res_row_cnt(f'{CURR_PATH}/{f_util.SYS_GProM}/q{specialId}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{specialId}Cnt.sql', f'FPVPSPT_{specialId}', isDuckDBBackend=False)
        q_util.make_executable_gprom_capture_res_row_cnt(f'{CURR_PATH}/{f_util.SYS_GProM}/q{specialId}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{specialId}Cnt.sql', f'FPVPSDT_{specialId}', isDuckDBBackend=True)
        specialId += 1



       
     
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_SQLProv, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_PostgreSQL, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_DuckDB, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_SmokedDuck, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_GProM, 1, specialId - 1)
if __name__ == "__main__":
    f_util.lodConfig(THIS_BENCHMARK)

    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_SQLProv)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_PostgreSQL)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_DuckDB)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_GProM)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_SmokedDuck)


    run()
