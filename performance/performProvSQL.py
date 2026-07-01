import sys
import os
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), './', 'utils'))
import queryUtils as q_util
import fileUtils as f_util
import dbUtils as db_util

# METADATA_PATH = '/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf1'
# METADATA_PATH = '/Users/pengyuanli/ProvBench/DBs/pg16Install/data'

CREATE_EXTENSION = 'CREATE EXTENSION IF NOT EXISTS provsql cascade;'
ALTER_SEARCH_PATH = f'ALTER database DATABASE SET search_path TO public, provsql;'
DROP_EXTENSION = 'DROP EXTENSION IF EXISTS provsql cascade;'



EXTRA = 'provsql_extra'
GATES = 'provsql_gates'
MAPPING = 'provsql_mapping'
WIRES = 'provsql_wires'
TABLES = 'provsql_table_info'
restoreM = [
    'cat METADATA_PATH/EXTRA_bk.mmap > METADATA_PATH/EXTRA.mmap',
    'cat METADATA_PATH/GATES_bk.mmap > METADATA_PATH/GATES.mmap',
    'cat METADATA_PATH/MAPPING_bk.mmap > METADATA_PATH/MAPPING.mmap',
    'cat METADATA_PATH/WIRES_bk.mmap > METADATA_PATH/WIRES.mmap',
    'cat METADATA_PATH/TABLES_bk.mmap > METADATA_PATH/TABLES.mmap'
]

def restoreMeta(mmappath):

    for cmd in restoreM:
        cmdT = cmd
        cmdT = cmdT.replace('METADATA_PATH', mmappath).replace('EXTRA', EXTRA).replace('GATES', GATES).replace('MAPPING', MAPPING).replace('WIRES', WIRES).replace('TABLES', TABLES)
        print(f'restore metadata Running cmd: {cmdT}')
        process = subprocess.run(cmdT, shell=True, stdout= subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if process.returncode:
            print(f"Error running command [{process.returncode}]: \n{process.stderr}\n{process.stdout}")
            exit()

def getMetaSize(outfile, mmappath):
    string = f'ls -l {mmappath}/provsql_*'
    process = subprocess.run(string, shell=True, stdout= subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if process.returncode:
        print(f"Error running command [{process.returncode}]: \n{process.stderr}\n{process.stdout}")
        exit()
    with open(outfile, 'w') as f:
        f.write(process.stdout)

def provsql_time(psqlcmd, infile, outfile, repeat, qNo, microbenchmark, mmappath, restoreAfter, dbName):

    cmd = (psqlcmd + ['-f', infile])
    dbsizecmd = (psqlcmd + ['-c', f"select pg_database_size('{dbName}');"])
    # print(f'dbsize query: \n\t\t{dbsizecmd}')
    with open(outfile, 'w') as f:
        for i in range(repeat):
            print(f'the {(i+1)}-th execution of command')
            # restore prov_*.mmap
            if i % restoreAfter == 0:
                restoreMeta(mmappath)

            # get the prov_* size before execution
            outSize = f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}{i}_metaSizeBefore.txt'
            getMetaSize(outSize, mmappath)

            # get current dbsize before provsql running
            (rt, out, err) = db_util.get_shell_command_results(dbsizecmd)
            if rt:
                print(f"Error running command in postgresql [{rt}]: \n{err}\n{out}")
                exit(rt)

            f.write(f"########## DBSIZE BEFORE {i}:\n")
            f.write(out)
            f.write('\n')

            # execute the query using provsql
            (rt, out, err) = db_util.get_shell_command_results(cmd)
            if rt:
                print(f"Error running command in postgresql [{rt}]: \n{err}\n{out}")
                exit(rt)

            f.write("########## EXECUTION TIME:\n")
            f.write(out)
            f.write('\n')

            # get current dbsize after provsql running
            (rt, out, err) = db_util.get_shell_command_results(dbsizecmd)
            if rt:
                print(f"Error running command in postgresql [{rt}]: \n{err}\n{out}")
                exit(rt)

            f.write(f"########## DBSIZE AFTER {i}:\n")
            f.write(out)
            f.write('\n\n')

            # get the prov_* size after execution
            outSize = f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}{i}_metaSizeAfter.txt'
            getMetaSize(outSize, mmappath)

def run_provsql(db_bin, db_host, db_name, db_port, db_user, db_password, microbenchmark, repeat:int, QList:list, mmappath, RestoreAfter: int):
    postgresqlCMD = [db_bin, '-h', db_host, '-d', db_name, '-p', db_port, '-U', db_user]
    for qNo in QList:
        print(f'Running ProvSQL PostgreSQL for {microbenchmark} q{qNo}...')
        if microbenchmark in ['PMRLIN', 'PMRLIN2', 'PMBD', 'PMFD', 'PMFD2', 'PMFD3']:
            db_util.psql_dashC(postgresqlCMD, CREATE_EXTENSION, f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_createExt.txt')
            db_util.psql_dashC(postgresqlCMD, ALTER_SEARCH_PATH.replace('DATABASE', db_name), f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_alterSearchPath.txt')

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_ProvSQL}/capPq{qNo}_p1.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_p1_res.txt'
            provsql_time(postgresqlCMD, infile, outfile, repeat=repeat, qNo=qNo, microbenchmark=microbenchmark, mmappath=mmappath, restoreAfter=RestoreAfter, dbName=db_name)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_ProvSQL}/capPq{qNo}_p2.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_p2_res.txt'
            provsql_time(postgresqlCMD, infile, outfile, repeat=repeat, qNo=qNo, microbenchmark=microbenchmark, mmappath=mmappath, restoreAfter=RestoreAfter, dbName=db_name)

            # if microbenchmark == 'PMFD2' or microbenchmark == 'PMFD3':
                # db_util.psql_dashC(postgresqlCMD, DROP_EXTENSION, f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_dropExt.txt')

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_ProvSQL}/capPq{qNo}_p3.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_p3_res.txt'
            provsql_time(postgresqlCMD, infile, outfile, repeat=1, qNo=qNo, microbenchmark=microbenchmark, mmappath=mmappath, restoreAfter=RestoreAfter, dbName=db_name)


        #     # -- disable extension after execution to avoid affecting other queries
            db_util.psql_dashC(postgresqlCMD, DROP_EXTENSION, f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_dropExt.txt')

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_ProvSQL}/capPq{qNo}_p4.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_p4_res.txt'
            provsql_time(postgresqlCMD, infile, outfile, repeat=repeat, qNo=qNo, microbenchmark=microbenchmark, mmappath=mmappath, restoreAfter=RestoreAfter, dbName=db_name)


            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_ProvSQL}/capPq{qNo}_p5.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_p5_res.txt'
            provsql_time(postgresqlCMD, infile, outfile, repeat=1, qNo=qNo, microbenchmark=microbenchmark, mmappath=mmappath, restoreAfter=RestoreAfter, dbName=db_name)

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_ProvSQL}/capPq{qNo}_p6.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_p6_res.txt'
            provsql_time(postgresqlCMD, infile, outfile, repeat=repeat, qNo=qNo, microbenchmark=microbenchmark, mmappath=mmappath, restoreAfter=RestoreAfter, dbName=db_name)

        else:
        # if True:
            db_util.psql_dashC(postgresqlCMD, CREATE_EXTENSION, f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_createExt.txt')
            db_util.psql_dashC(postgresqlCMD, ALTER_SEARCH_PATH.replace('DATABASE', db_name), f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_alterSearchPath.txt')

            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_ProvSQL}/capPq{qNo}.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/provsql_capPq{qNo}_res.txt'
            provsql_time(postgresqlCMD, infile, outfile, repeat=repeat, qNo=qNo, microbenchmark=microbenchmark, mmappath=mmappath, restoreAfter= RestoreAfter, dbName= db_name)
