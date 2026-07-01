import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), './', 'utils'))
import queryUtils as q_util
import fileUtils as f_util
import dbUtils as db_util


def run_duckdb(duckdb_bin, db_path, microbenchmark, repeat:int, QList:list):
    duckdbCMD = [ duckdb_bin, db_path ]
    for qNo in QList:
        infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_DuckDB}/capDq{qNo}.sql'
        outfile = f'{os.getcwd()}/{microbenchmark}/results/{f_util.SYS_DuckDB}_capDq{qNo}_res.txt'
        db_util.duckdb_run(duckdbCMD, infile, outfile, repeat=repeat)