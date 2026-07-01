import pandas as pd
import string
import random
import os
import json
import sys
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
import queryUtils as q_util
import fileUtils as f_util
import stringUtils as s_util

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

THIS_BENCHMARK = 'QTPCH'
CURR_PATH = os.getcwd()



gplist = ['Pq1.sql', 'Pq3.sql', 'Pq5.sql', 'Pq6.sql', 'Pq7.sql', 'Pq8.sql', 'Pq9.sql', 'Pq10.sql', 'Pq12.sql', 'Pq13.sql', 'Pq14.sql', 'Pq19.sql']
gdlist = ['Dq1.sql', 'Dq3.sql', 'Dq5.sql', 'Dq6.sql', 'Dq7.sql', 'Dq8.sql', 'Dq9.sql', 'Dq10.sql', 'Dq12.sql', 'Dq13.sql', 'Dq14.sql', 'Dq19.sql']

smdlist = ['q1.sql', 'q2.sql', 'q3.sql', 'q4.sql', 'q5.sql', 'q7.sql', 'q8.sql', 'q9.sql', 'q10.sql', 'q12.sql', 'q13.sql', 'q16.sql', 'q18.sql', 'q20.sql', 'q21.sql']
provlist = ['q1.sql', 'q6.sql', 'q7.sql', 'q9.sql', 'q12.sql', 'q19.sql']

splist = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q9', 'q10', 'q11', 'q13', 'q15', 'q16', 'q17', 'q18', 'q19', 'q21', 'q22']

def gprom_rewrite(infile, outfile, isDuckDBBackend=False, isUseProvComposable=False):
    with open(f'{os.getcwd()}/systems.config', 'r') as jsonFile:
        jsons = json.load(jsonFile)
    configs = jsons["gprom"]
    gpromCMD = q_util.getGProMCmdFromJson(configs, isDuckDB = isDuckDBBackend)
    if isUseProvComposable:
        gpromCMD += ['-prov_use_composable', 'TRUE', '-heuristic_opt', 'TRUE', '-Opullup_prov_projections', 'FALSE', '-Oselection_move_around', 'FALSE']

    cmd = (gpromCMD + ['-queryFile', f'{infile}' ])
    print(cmd)
    try:
        with open(outfile, 'w') as out:
            process = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
            rt = process.returncode
            if rt != 0:
                q_util.LOG(f"Error rewriting sql {process.stderr}", True)
                return(rt, process.stderr)
            q_util.LOG(process.stdout)
            out.write(process.stdout)
    except Exception as e:
        q_util.LOG(f'ERROR in gprom rewrite {e}\n', True)



def run():
    CFGs = f_util.loadJsonConfig(f'{os.getcwd()}/systems.config')
    for gpq in gplist:
        # QTemplate = f_util.readTemplate(f'{CURR_PATH}/templates/gprom/{gpq}')
        if gpq in ['Pq3.sql', 'Pq10.sql']:
            gprom_rewrite(f'{CURR_PATH}/templates/gprom/{gpq}', f'{CURR_PATH}/{f_util.SYS_GProM}/rw{gpq}', isDuckDBBackend=False, isUseProvComposable=True)
        else:
            gprom_rewrite(f'{CURR_PATH}/templates/gprom/{gpq}', f'{CURR_PATH}/{f_util.SYS_GProM}/rw{gpq}', isDuckDBBackend=False, isUseProvComposable=False)
        q_util.make_executable_gprom_capture(f'{CURR_PATH}/{f_util.SYS_GProM}/rw{gpq}', f'{CURR_PATH}/{f_util.SYS_GProM}/cap{gpq}', isDuckDBBackend=False)
        q_util.make_executable_gprom_capture_res_row_cnt(f'{CURR_PATH}/{f_util.SYS_GProM}/rw{gpq}', f'{CURR_PATH}/{f_util.SYS_GProM}/cap{gpq.split(".")[0]}Cnt.sql', 'TPCHRESCNTGPROM', isDuckDBBackend=False)
    for gdq in gdlist:
        # QTemplate = f_util.readTemplate(f'{CURR_PATH}/templates/gprom/{gdq}')
        if gdq in ['Dq3.sql', 'Dq10.sql']:
            gprom_rewrite(f'{CURR_PATH}/templates/gprom/{gdq}', f'{CURR_PATH}/{f_util.SYS_GProM}/rw{gdq}', isDuckDBBackend=True, isUseProvComposable=True)
        else:
            gprom_rewrite(f'{CURR_PATH}/templates/gprom/{gdq}', f'{CURR_PATH}/{f_util.SYS_GProM}/rw{gdq}', isDuckDBBackend=True, isUseProvComposable=False)
        q_util.make_executable_gprom_capture(f'{CURR_PATH}/{f_util.SYS_GProM}/rw{gdq}', f'{CURR_PATH}/{f_util.SYS_GProM}/cap{gdq}', isDuckDBBackend=True)
        q_util.make_executable_gprom_capture_res_row_cnt(f'{CURR_PATH}/{f_util.SYS_GProM}/rw{gdq}', f'{CURR_PATH}/{f_util.SYS_GProM}/cap{gdq.split(".")[0]}Cnt.sql', 'TPCHRESCNTGPROM',isDuckDBBackend=True)
        # ---------smd

        smdCFG = f_util.loadJsonConfig(f'{os.getcwd()}/systems.config')
        duckdbCMD = smdCFG["smokedduckpre"]
    for smdq in smdlist:
        smdfname = smdq.split('.')[0]
        sSQL = f_util.readTemplate(f'{CURR_PATH}/templates/smokedduck/{smdq}')
        s_util.writeStrToFile(f'{sSQL};', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/{smdfname}.sql')
        # -- Phase I
        q_util.make_executable_smd_p1(sSQL, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capD{smdfname}_p1.sql')
        # -- export table
        tableList = q_util.duckdbGetAllLineageTables(duckdbCMD["duckdb_bin"], duckdbCMD["database_path"], sSQL)
        q_util.make_executable_smd_export(tableList, sSQL, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capD{smdfname}_export.sql', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}')
        # -- import
        q_util.make_executable_smd_import(tableList, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capD{smdfname}_import.sql', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}')
        # -- Phase II
        LINQ = q_util.duckdbGetLineageQuery(duckdbCMD["duckdb_bin"], duckdbCMD["database_path"], sSQL)
        q_util.make_executable_smd_p2(LINQ, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capD{smdfname}_p2.sql')
        # --------- provsql
    for provq in provlist:
        q_util.make_executable(f'{CURR_PATH}/templates/{f_util.SYS_ProvSQL}/{provq}', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capP{provq}', f_util.SYS_ProvSQL, isDuckDBBackend=False)

        # --------- sqlprov
        f_util.SQLProvPreFile(THIS_BENCHMARK)
        f_util.SQLProvLogSizeFile(THIS_BENCHMARK, ['logaggregation', 'logjoin', 'logorderby', 'logfilter'])
    for spq in splist:
        spqname = spq.split('.')[0]
        q_util.make_executable(f'{CURR_PATH}/templates/{f_util.SYS_SQLProv}/{spqname}-p1.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capP{spqname}_p1.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)
        q_util.make_executable(f'{CURR_PATH}/templates/{f_util.SYS_SQLProv}/{spqname}-p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capP{spqname}_p2.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)

if __name__ == "__main__":
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_GProM)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_SmokedDuck)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_ProvSQL)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_SQLProv)
    run()
