import os
import argparse
import re
import sys
import subprocess
from dataclasses import dataclass
from typing import List
from math import ceil
import json
from datetime import datetime

import performGProM as gpromRunner
# import performProvSQL as provsqlRunner
import performSmokedDuck as smokedDuckRunner
# import performLinks as linksRunner
import performSQLProv as sqlprovRunner
import performProvSQL as provsqlRunner
import performPostgreSQL as postgresqlRunner
import performDuckDB as duckdbRunner


sys.path.append(os.path.join(os.path.dirname(__file__), './', 'utils'))
import queryUtils as q_util
import fileUtils as f_util
import dbUtils as db_util



ROOT = os.path.dirname(__file__)

################################################################################
def run_links(microbenchmark, repeat, QList):
    jsons = f_util.loadJsonConfig(f'{os.getcwd()}/{microbenchmark}/systems.config')
    configs = jsons["links"]
    benchmarkCfg = f_util.loadJsonConfig(f'{ROOT}/utils/benchmarks.cfg')
    postgresqlCMD = db_util.getPostgresqlCmdFromJson(configs)
    benchmarkPath = f'{os.getcwd()}/{microbenchmark}'

    if microbenchmark in benchmarkCfg["regular"]:
        for qNo in QList:
            print(f'Links Run For {microbenchmark} --> q{qNo}')
            infile = f'{benchmarkPath}/links/execq{qNo}.sql'
            outfile = f'{benchmarkPath}/results/links_q{qNo}.csv'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat)
################################################################################
def run(args):
    global options
    options = args

    if options.microbenchmark is None:
        print('ERROR: please indicate which micro benchmark to run, e.g., --microbenchmark=\'Agg_GroupSize\'')
        exit()
    allowedBenchs = ['Agg_GroupSize', 'Agg_HavingSel', 'Agg_MultiLevel', 'TopK', 'UC_Rpd', 'UC_DebugB']
    # TODO: add more benchmarks and checking for input

    # --------------------------------------------------------------------------
    # Checking Systems
    # --------------------------------------------------------------------------
    if options.systems is None:
        print('ERROR: please indicate which systems to run, e.g., --systems=\'gprom,provsql,smokeduck\'')
        exit()

    allowedSystems = ['gprom', 'provsql', 'smokedduck', 'links', 'sqlprov', 'duckdb', 'postgresql']
    inputSystems = options.systems.strip().split(',')
    for system in inputSystems:
        if system not in allowedSystems:
            print(f'ERROR: system {system} is not supported. Supported systems include: {allowedSystems}')
            exit()

    microbenchmark = f'{options.microbenchmark}'
    os.makedirs(f'{os.getcwd()}/{microbenchmark}/results', exist_ok=True)

    jsonConfigs = f_util.loadJsonConfig(f'{os.getcwd()}/{microbenchmark}/systems.config')

    db_bin = options.db_bin
    db_host = options.db_host
    db_path = options.db_path
    db_port = options.db_port
    db_user = options.db_user
    db_password = options.db_password
    db_name = options.db_name

    for system in inputSystems:
        # --- ProvSQL
        if system == f_util.SYS_ProvSQL:
            if options.provsqlmmap is None:
                print('ERROR: please indicate the memory map file for ProvSQL, e.g., --provsqlmmap=\'/path/to/mmapfile\'')
                exit()
            # -- create a log file
            QList = f_util.getQList(options.qstart, options.qend, options.querylist, jsonConfigs, f_util.SYS_ProvSQL)
            f_util.createFile(f'./log_{f_util.SYS_ProvSQL}', f_util.APPEND, f'ProvSQL Run Log for {microbenchmark}\n')
            provsqlRunner.run_provsql(db_bin, db_host, db_name, db_port, db_user, db_password, f'{microbenchmark}', options.runrepeat, QList, options.provsqlmmap, options.provsqlRestoreAfter)

        # --- GProM
        elif system == f_util.SYS_GProM:
            # --- create a log file
            QList = f_util.getQList(options.qstart, options.qend, options.querylist, jsonConfigs, f_util.SYS_GProM)
            f_util.createFile(f'./log_{f_util.SYS_GProM}', f_util.APPEND, f'GProM Run Log for {microbenchmark}\n')
            backend = options.gprombackend
            if backend not in ['postgresql', 'duckdb']:
                print(f"ERROR: GProM backend {options.gprombackend} is not supported!\n")
                print("Please use --gprombackend to set the backend, \'postgresql\', or \'duckdb\'\n")
                exit()
            if backend == 'duckdb':
                gpromRunner.run_gprom_duckdb(db_bin, db_path, f'{microbenchmark}', options.runrepeat, QList)
            elif backend == 'postgresql':
                gpromRunner.run_gprom_postgresql(db_bin, db_host, db_name, db_port, db_user, db_password, f'{microbenchmark}', options.runrepeat, QList)

        # --- Links
        elif system == f_util.SYS_Links:
            QList = f_util.getQList(options.qstart, options.qend, options.querylist, jsonConfigs, f_util.SYS_Links)
            # -- create a log file
            f_util.createFile(f'./log_{f_util.SYS_Links}', f_util.APPEND, f'Links Run Log for {microbenchmark}\n')
            run_links(f'{microbenchmark}', options.runrepeat, QList)

        # --- SmokedDuck
        elif system == f_util.SYS_SmokedDuck:
            QList = f_util.getQList(options.qstart, options.qend, options.querylist, jsonConfigs, f_util.SYS_SmokedDuck)
            # -- create a log file
            f_util.createFile(f'./log_{f_util.SYS_SmokedDuck}', f_util.APPEND, f'SmokedDuck Run Log for {microbenchmark}\n')
            db_bin_storage = options.db_bin_storage
            db_path_storage = options.db_path_storage
            smokedDuckRunner.run_smokedduck(db_bin_storage, db_path_storage, db_bin, db_path, f'{microbenchmark}', options.runrepeat, QList)

        # --- SQLProv
        elif system == f_util.SYS_SQLProv:
            QList = f_util.getQList(options.qstart, options.qend, options.querylist, jsonConfigs, f_util.SYS_SQLProv)
            # -- create a log file
            f_util.createFile(f'./log_{f_util.SYS_SQLProv}', f_util.APPEND, f'SQLProv Run Log for {microbenchmark}\n')
            sqlprovRunner.run_sqlprov(db_bin, db_host, db_name, db_port, db_user, db_password, f'{microbenchmark}', options.runrepeat, QList)

        # --- PostgreSQL
        elif system == f_util.SYS_PostgreSQL:
            QList = f_util.getQList(options.qstart, options.qend, options.querylist, jsonConfigs, f_util.SYS_PostgreSQL)
            # -- create a log file
            f_util.createFile(f'./log_{f_util.SYS_PostgreSQL}', f_util.APPEND, f'PostgreSQL Run Log for {microbenchmark}\n')
            postgresqlRunner.run_postgresql(db_bin, db_host, db_name, db_port, db_user, db_password, f'{microbenchmark}', options.runrepeat, QList)
        # --- DuckDb
        elif system == f_util.SYS_DuckDB:
            QList = f_util.getQList(options.qstart, options.qend, options.querylist, jsonConfigs, f_util.SYS_DuckDB)
            # -- create a log file
            f_util.createFile(f'./log_{f_util.SYS_DuckDB}', f_util.APPEND, f'DuckDB Run Log for {microbenchmark}\n')
            duckdbRunner.run_duckdb(db_bin, db_path, f'{microbenchmark}', options.runrepeat, QList)

if __name__ == '__main__':
    config = f_util.loadJsonConfig(f'{os.getcwd()}/utils/{f_util.SYS_ConfigGeneral}')
    SF = config["scale_factor"]

    ap = argparse.ArgumentParser(description = 'Provenance Benchmarks')

    # database utils
    ap.add_argument('--db_bin', type=str, default='duckdb', help='the database binary to run the queries, e.g., duckdb, psql, or /path/to/duckdb, /path/to/psql')
    ap.add_argument('--db_host', type=str, default=None, help='the host to connect to the postgresql database, e.g., localhost')
    ap.add_argument('--db_path', type=str, default=None, help='NOTE: the path to the DUCKDB database file, e.g., /path/to/duckdb.db')
    ap.add_argument('--db_port', type=str, default=None, help='the port to connect to the postgresql database, e.g., 5432')
    ap.add_argument('--db_user', type=str, default=None, help='the user to connect to the postgresql database, e.g., postgres')
    ap.add_argument('--db_password', type=str, default=None, help='the password to connect to the postgresql database, e.g., postgres')
    ap.add_argument('--db_name', type=str, default=None, help='the database name to connect to the postgresql database, e.g., provbench')

    # benchmark and query settings
    ap.add_argument("--microbenchmark", type=str, help="Select a benchmark to run the queries: e.g. VPGN or FPAgg")
    ap.add_argument('--systems', type=str, default=None, help="Specify the systems to run, separated by comma, e.g., gprom,provsql,smokeduck,links,sqlprov")
    ap.add_argument('--runrepeat', type=int, default=6, help="Repeated time of a query runing")
    ap.add_argument('--qstart', type=int, default= -1, help= "Start index of a series queries in a benchmark")
    ap.add_argument('--qend', type=int, default= -1, help = 'End index of a series queries in a benchmark')
    ap.add_argument('--querylist', type=str, default=None, help="Specify the list of queries to run, separated by comma, e.g., '1,3,5'")
    ap.add_argument('--scale_factor', type=str, default=SF, help='Specify the scale factor otherwise use the setting in systems.cfg')
    ap.add_argument('--gprombackend', type=str, default='postgresql', help='Specify the backend for GProM: duckdb or postgresql')
    ap.add_argument('--provsqlmmap', type=str, default=None, help='Specify the the memory map file for ProvSQL.')
    ap.add_argument('--provsqlRestoreAfter', type=int, default=6, help='Specify after how many repetion of running to restore memory map file for ProvSQL.')
    ap.add_argument('--db_bin_storage', type=str, default=None, help='the duckdb binary to run the original queries for smokedduck, e.g., /path/to/duckdb')
    ap.add_argument('--db_path_storage', type=str, default=None, help='the path to the duckdb database file for smokedduck, e.g., /path/to/duckdb.db')



    args = ap.parse_args()
    run(args)
