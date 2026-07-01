import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), './', 'utils'))
import queryUtils as q_util
import fileUtils as f_util
import dbUtils as db_util


def run_postgresql(db_bin, db_host, db_name, db_port, db_user, db_password, microbenchmark, repeat, QList):
    postgresqlCMD = [db_bin, '-h', db_host, '-d', db_name, '-p', db_port, '-U', db_user]
    for qNo in QList:
        infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_PostgreSQL}/capPq{qNo}.sql'
        outfile = f'{os.getcwd()}/{microbenchmark}/results/{f_util.SYS_PostgreSQL}_capPq{qNo}_res.txt'
        db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat)