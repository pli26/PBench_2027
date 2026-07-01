import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), './', 'utils'))
import queryUtils as q_util
import fileUtils as f_util
import dbUtils as db_util


def run_sqlprov(db_bin, db_host, db_name, db_port, db_user, db_password, microbenchmark, repeat:int, QList:list):
    # jsonFile = f_util.loadJsonConfig(f'{os.getcwd()}/{microbenchmark}/systems.config')
    # configs = jsonFile["sqlprov"]
    postgresqlCMD = [db_bin, '-h', db_host, '-d', db_name, '-p', db_port, '-U', db_user]
    for qNo in QList:
        if microbenchmark in ['PMRLIN', 'PMRLIN2', 'PMBD', 'PMFD', 'PMFD2', 'PMFD3']:
            print(f'Running SQLProv PostgreSQL for {microbenchmark} q{qNo}...')
            # ---- pre, truncate log tables + Phase I
            infile = ''
            outfile = ''
            pre = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/pre.sql'
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/capPq{qNo}_p1.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/sp_capPq{qNo}_p1_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat, prepare=pre)

            # ----- analyze DB
            infile = ''
            infile = f'{os.getcwd()}/utils/analyzeDB.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/analyzeDB_q{qNo}.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=1)

            # ------ get log table size
            infile = ''
            outfile = ''
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/logSize.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/logSize_q{qNo}.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=1)

            # ------- run phase II
            infile = ''
            outfile = ''
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/capPq{qNo}_p2.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/sp_capPq{qNo}_p2_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/capPq{qNo}_p3.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/sp_capPq{qNo}_p3_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=1)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/capPq{qNo}_p4.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/sp_capPq{qNo}_p4_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/capPq{qNo}_p5.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/sp_capPq{qNo}_p5_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=1)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/capPq{qNo}_p6.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/sp_capPq{qNo}_p6_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat)
        else:
            infile = ''
            outfile = ''
            pre = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/pre.sql'
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/capPq{qNo}_p1.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/sp_capPq{qNo}_p1_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat, prepare=pre)

            # ----- analyze DB
            infile = ''
            infile = f'{os.getcwd()}/utils/analyzeDB.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/analyzeDB_q{qNo}.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=1)

            # ------ get log table size
            infile = ''
            outfile = ''
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/logSize.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/logSize_q{qNo}.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=1)

            # ------- run phase II
            infile = ''
            outfile = ''
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SQLProv}/capPq{qNo}_p2.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/sp_capPq{qNo}_p2_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat)



