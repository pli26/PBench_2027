import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), './', 'utils'))
import queryUtils as q_util
import fileUtils as f_util
import dbUtils as db_util


def run_gprom_duckdb(duckdb_bin, db_path, microbenchmark, repeat:int, QList:list):
    duckdbCMD = [ duckdb_bin, db_path ]
    for qNo in QList:
        print(f'Running GProM DuckDB for {microbenchmark} q{qNo}...')
        if microbenchmark in ['PMRLIN2']:
            print(f'Running GProM DuckDB for {microbenchmark} q{qNo} (data provenance)...')
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capDq{qNo}_p1.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capDq{qNo}_p1_res.txt'
            db_util.duckdb_run(duckdbCMD, infile, outfile, repeat=repeat)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capDq{qNo}_p2.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capDq{qNo}_p2_res.txt'
            db_util.duckdb_run(duckdbCMD, infile, outfile, repeat=1)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capDq{qNo}_p3.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capDq{qNo}_p3_res.txt'
            db_util.duckdb_run(duckdbCMD, infile, outfile, repeat=repeat)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capDq{qNo}_p4.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capDq{qNo}_p4_res.txt'
            db_util.duckdb_run(duckdbCMD, infile, outfile, repeat=1)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capDq{qNo}_p5.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capDq{qNo}_p5_res.txt'
            db_util.duckdb_run(duckdbCMD, infile, outfile, repeat=repeat)
        elif microbenchmark in ['PMRLIN', 'PMBD', 'PMFD', 'PMFD2', 'PMFD3']:
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capDq{qNo}_dt.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capDq{qNo}_dt_res.txt'
            db_util.duckdb_run(duckdbCMD, infile, outfile, repeat=repeat)
            if microbenchmark not in ['PMBD', 'PMFD', 'PMFD2', 'PMFD3']:
                infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capDq{qNo}_id.sql'
                outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capDq{qNo}_id_res.txt'
                db_util.duckdb_run(duckdbCMD, infile, outfile, repeat=repeat)

        else:
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capDq{qNo}.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capDq{qNo}_res.txt'
            db_util.duckdb_run(duckdbCMD, infile, outfile, repeat=repeat)

            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capDq{qNo}_RCnt.txt'
            db_util.duckdb_run(duckdbCMD, infile, outfile, repeat=1)

def run_gprom_postgresql(db_bin, db_host, db_name, db_port, db_user, db_password, microbenchmark, repeat, QList):
    postgresqlCMD = [db_bin, '-h', db_host, '-d', db_name, '-p', db_port, '-U', db_user]
    for qNo in QList:
        print(f'Running GProM PostgreSQL for {microbenchmark} q{qNo}...')
        if microbenchmark in ['PMRLIN2']:
            print(f'Running GProM PostgreSQL for {microbenchmark} q{qNo} (data provenance)...')
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capPq{qNo}_p1.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capPq{qNo}_p1_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capPq{qNo}_p2.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capPq{qNo}_p2_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=1)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capPq{qNo}_p3.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capPq{qNo}_p3_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capPq{qNo}_p4.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capPq{qNo}_p4_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=1)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capPq{qNo}_p5.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capPq{qNo}_p5_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat)


        elif microbenchmark in ['PMRLIN', 'PMBD', 'PMFD', 'PMFD2', 'PMFD3']:
            print(f'Running GProM PostgreSQL for {microbenchmark} q{qNo} (data provenance)...')
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capPq{qNo}_dt.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capPq{qNo}_dt_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat)
            if microbenchmark not in ['PMBD', 'PMFD', 'PMFD2', 'PMFD3']:
                infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capPq{qNo}_id.sql'
                outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capPq{qNo}_id_res.txt'
                db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat)
        else:
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capPq{qNo}.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capPq{qNo}_res.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=repeat)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_GProM}/capPq{qNo}Cnt.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/gprom_capPq{qNo}_RCnt.txt'
            db_util.psql_time(postgresqlCMD, infile, outfile, repeat=1)
