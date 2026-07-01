import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), './', 'utils'))
import queryUtils as q_util
import fileUtils as f_util
import dbUtils as db_util

# SPECIFIED_DUCK_BIN = '/Users/uicdbgroup/pengyuan/duckdb/duckdb'


# def run_smokedduck(db_bin, db_path, microbenchmark, repeat:int, QList:list, isPreDuckdb = False):
def run_smokedduck(db_bin_storage, db_path_storage, db_bin, db_path, microbenchmark, repeat:int, QList:list, isPreDuckdb = False):

    for qNo in QList:
        print(f'Running SmokedDuck for {microbenchmark} q{qNo}...')

        # --- phase I
        # q_util.rmSMDLineageTables(db_bin_storage, db_path_storage)
        print("PHASE I")
        infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SmokedDuck}/capDq{qNo}_p1.sql'
        outfile = f'{os.getcwd()}/{microbenchmark}/results/smd_capDq{qNo}_p1_res.txt'
        db_util.duckdb_run([db_bin, db_path], infile, outfile, repeat)

        # -- export table
        # -- acquire the inform from v5
        infile = ''
        outfile = ''
        print("EXPORTING TABLE...")
        infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SmokedDuck}/capDq{qNo}_export.sql'
        outfile = f'{os.getcwd()}/{microbenchmark}/results/smd_capDq{qNo}_export_res.txt'
        db_util.duckdb_run([db_bin_storage, db_path_storage], infile, outfile, 1)

        # -- import table
        infile = ''
        outfile = ''
        print("IMPORTING TABLE...")
        infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SmokedDuck}/capDq{qNo}_import.sql'
        outfile = f'{os.getcwd()}/{microbenchmark}/results/smd_capDq{qNo}_import_res.txt'
        db_util.duckdb_run([db_bin, db_path], infile, outfile, 1)

        # -- phase II
        infile = ''
        outfile = ''
        print("PHASE II")
        infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SmokedDuck}/capDq{qNo}_p2.sql'
        outfile = f'{os.getcwd()}/{microbenchmark}/results/smd_capDq{qNo}_p2_res.txt'
        if microbenchmark in ['PMPP']:
            db_util.duckdb_run([db_bin_storage, db_path_storage], infile, outfile, repeat, cleanLineageTable=True)
        else:
            db_util.duckdb_run([db_bin, db_path], infile, outfile, repeat, cleanLineageTable=False)

        if microbenchmark in ['PMRLIN2', 'PMBD', 'PMFD', 'PMFD2', 'PMFD3']:
            # -- phase III
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SmokedDuck}/capDq{qNo}_p3.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/smd_capDq{qNo}_p3_res.txt'
            db_util.duckdb_run([db_bin, db_path], infile, outfile, repeat, cleanLineageTable=False)
            # -- phase IV
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SmokedDuck}/capDq{qNo}_p4.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/smd_capDq{qNo}_p4_res.txt'
            db_util.duckdb_run([db_bin, db_path], infile, outfile, repeat, cleanLineageTable=False)

            # -- phase V
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SmokedDuck}/capDq{qNo}_p5.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/smd_capDq{qNo}_p5_res.txt'
            db_util.duckdb_run([db_bin, db_path], infile, outfile, repeat, cleanLineageTable=False)

            # -- phase VI
            infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SmokedDuck}/capDq{qNo}_p6.sql'
            outfile = f'{os.getcwd()}/{microbenchmark}/results/smd_capDq{qNo}_p6_res.txt'
            db_util.duckdb_run([db_bin, db_path], infile, outfile, repeat, cleanLineageTable=False)


        # -- clean up lineage tables
        infile = ''
        outfile = ''
        print("CLEANING UP LINEAGE TABLES...")
        # infile = f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SmokedDuck}/capDq{qNo}_rmtable.sql'
        # outfile = f'{os.getcwd()}/{microbenchmark}/results/smd_capDq{qNo}_rmtable_res.txt'
        # db_util.duckdb_run([db_bin, db_path], infile, outfile, 1)
        q_util.rmSMDLineageTables(db_bin, db_path)

        print("CLEANING UP LINEAGE TABLES ON DISK...")
        files = os.listdir(f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SmokedDuck}')
        for file in files:
            if file.startswith(f'LINEAGE_') and file.endswith('.parquet'):
                print(f"removing lineage table on disk: {file}...")
                os.remove(f'{os.getcwd()}/{microbenchmark}/{f_util.SYS_SmokedDuck}/{file}')

