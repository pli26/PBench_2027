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

THIS_BENCHMARK = 'PMAP'
CURR_PATH = os.getcwd()

def getGProMCmdFromJson(jsonFile, isDuckDB=False):
    gpromCMD = [jsonFile["gprom_bin"]]
    if isDuckDB:
        gpromDuckDB = jsonFile["duckdb"]
        gpromCMD += [
            '-backend', gpromDuckDB["backend"],
            '-Pmetadata', gpromDuckDB["Pmetadata"],
            '-db', gpromDuckDB["db"],
            '-Pexecutor', gpromDuckDB["Pexecutor"],
            '-loglevel', gpromDuckDB["loglevel"]
        ]
    else:
        gpromPostgresql = jsonFile["postgresql"]
        gpromCMD += [
            '-backend', gpromPostgresql["backend"],
            '-host',  gpromPostgresql["host"],
            '-user',  gpromPostgresql["user"],
            '-passwd', gpromPostgresql['passwd'],
            '-port', gpromPostgresql['port'],
            '-db', gpromPostgresql["db"],
            '-loglevel', gpromPostgresql["loglevel"],
            '-Pexecutor', gpromPostgresql["Pexecutor"],
            '-ps_binary_search', 'TRUE'
        ]
        # '-prov_use_composable', 'TRUE']

    return gpromCMD


def gprom_rewrite(infile, outfile, isDuckDBBackend=False):
    with open(f'{os.getcwd()}/systems.config', 'r') as jsonFile:
        jsons = json.load(jsonFile)
    configs = jsons["gprom"]
    gpromCMD = getGProMCmdFromJson(configs, isDuckDB=isDuckDBBackend)
    cmd = (gpromCMD + ['-queryFile', f'{infile}'])
    print(cmd)
    try:
        with open(outfile, 'w') as out:
            process = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            rt = process.returncode
            if rt != 0:
                print(f"Error rewriting sql {process.stderr}", True)
                return (rt, process.stderr)
            print(process.stdout)
            out.write(process.stdout)
    except Exception as e:
        print(f'ERROR in gprom rewrite {e}\n', True)

def run():
    qid = 1

    pg = f_util.readTemplate(f'{CURR_PATH}/templates/p.sql')
    s_util.writeStrToFile(f'{pg};', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql')
    q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_PostgreSQL}/capPq{qid}.sql', f_util.SYS_PostgreSQL, isDuckDBBackend=False)


    for tmpId in [1, 2, 3]:
        gprom_rewrite(f'{CURR_PATH}/templates/q{tmpId}.sql', f'{CURR_PATH}/gprom/rwPq{tmpId}.sql', isDuckDBBackend=False)
        q_util.make_executable_gprom_capture(f'{CURR_PATH}/gprom/rwPq{tmpId}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{tmpId}.sql', isDuckDBBackend=False)
        q_util.make_executable_gprom_capture_res_row_cnt(f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{tmpId}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{tmpId}Cnt.sql', f'AP_{tmpId}', isDuckDBBackend=True)

        qid += 1
    for tmpId in [4, 5, 6]:
        gp = f_util.readTemplate(f'{CURR_PATH}/templates/q{tmpId}.sql')
        s_util.writeStrToFile(f'{gp};', f'{CURR_PATH}/{f_util.SYS_GProM}/q{tmpId}.sql')
        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_GProM}/q{tmpId}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{tmpId}.sql', f_util.SYS_GProM, isDuckDBBackend=False)
        q_util.make_executable_gprom_capture_res_row_cnt(f'{CURR_PATH}/{f_util.SYS_GProM}/q{tmpId}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{tmpId}Cnt.sql', f'AP_{tmpId}', isDuckDBBackend=False)
        qid += 1

    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_PostgreSQL, 1, 1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_GProM, 1, qid - 1)









if __name__ == "__main__":
    f_util.lodConfig(THIS_BENCHMARK)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_GProM)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_PostgreSQL)

    run()