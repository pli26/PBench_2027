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

THIS_BENCHMARK = 'PMFD2'
CURR_PATH = os.getcwd()

checktemplate = 'select exists (select 1 from JT1, JT2 where JOINCOND and CHECKCOND);'

cconditions = [
                'ga = 900',
                'ga >= 900 and ga <= 903',
                'ga >= 900 and ga <= 915',
               ]




def run():
    CFGs = f_util.loadJsonConfig(f'{os.getcwd()}/systems.config')
    SMDCFG = CFGs[f_util.SYS_SmokedDuck + 'pre']

    jointable = 'jc'
    table = 'vpgn1k'
    conditions = ['ga >= 667 and ga <= 1000']
    TableAndAttr = f_util.loadJsonConfig(f'{ROOT}/utils/tables.cfg')
    tableAttr = TableAndAttr['vpgn1k']
    jointableAttr = TableAndAttr['jc']

    qid = 1

    for cond in conditions:
        QTemplate = f_util.readTemplate(f'{CURR_PATH}/templates/q.sql')
        gTMP = s_util.buildSQLFromTemplate(QTemplate, ['WHERECONDITION'], [cond])
        s_util.writeStrToFile(f'provenance of ({gTMP});', f'{CURR_PATH}/gprom/q{qid}.sql')
        q_util.gprom_rewrite(f'{CURR_PATH}/gprom/q{qid}.sql', f'{CURR_PATH}/gprom/rwPq{qid}.sql', isDuckDBBackend=False)
        q_util.gprom_rewrite(f'{CURR_PATH}/gprom/q{qid}.sql', f'{CURR_PATH}/gprom/rwDq{qid}.sql', isDuckDBBackend=True)

        gStoredTable = f'{THIS_BENCHMARK}_gprom_dt_{qid}'
        rpdQList = []
        for ccond in cconditions:
            checkQ = f' select ga, ava, avb from lineages where {ccond};\n\n'
            rpdQList.append(checkQ)

        for ccond in cconditions:
            checkQQ = f' select * from lineages where {ccond};\n\n'
            rpdQList.append(checkQQ)

        q_util.make_executable_gprom_rpd_dt(
            f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql',
            f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}_dt.sql',
            rpdQList,
            f'{THIS_BENCHMARK}_gprom_dt_{qid}',
            isDuckDBBackend=False,
            isRPDList=True)
        q_util.make_executable_gprom_rpd_dt(
            f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql',
            f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}_dt.sql',
            rpdQList,
            f'{THIS_BENCHMARK}_gprom_dt_{qid}',
            isDuckDBBackend=True,
            isRPDList=True)


        # ----- sqlprov
        f_util.SQLProvPreFile(THIS_BENCHMARK)
        f_util.SQLProvLogSizeFile(THIS_BENCHMARK, ['logjoin', 'logfilter', 'logaggregation'])
        spTemplate1 = f_util.readTemplate(f'{CURR_PATH}/templates/sp_p1.sql')
        spSQL1 = s_util.buildSQLFromTemplate(spTemplate1, ['TABLE', 'JOINED_TBL', 'WHERECONDITION'], [f'{table}', f'{jointable}', cond])
        s_util.writeStrToFile(f'{spSQL1};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql')
        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p1.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)
        # -- p1
        with open (f'{CURR_PATH}/sqlprov/capPq{qid}_p1.sql', 'w') as f:
            f.write(f'explain (analyze, timing off) \n {spSQL1};\n')


        spTemplate2 = f_util.readTemplate(f'{CURR_PATH}/templates/sp_p2.sql')
        spSQL2 = s_util.buildSQLFromTemplate(spTemplate2, ['TABLE', 'JOINED_TBL'], [f'{table}', f'{jointable}'])

        s_util.writeStrToFile(f'{spSQL2};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql')
        with open(f'{CURR_PATH}/sqlprov/capPq{qid}_p2.sql', 'w') as f:
            f.write(f'explain (analyze, timing off) \n {spSQL2};\n')

        with open(f'{CURR_PATH}/sqlprov/capPq{qid}_p3.sql', 'w') as f:
            f.write(f'drop table if exists {THIS_BENCHMARK}_sqlprov_{qid}_p1;\n')
            f.write(f'explain (analyze, timing off) create table {THIS_BENCHMARK}_sqlprov_{qid}_p1 as \n {spSQL1};\n')
            f.write(f'select pg_relation_size(\'{THIS_BENCHMARK}_sqlprov_{qid}_p1\') ;\n')
            f.write(f'drop table if exists {THIS_BENCHMARK}_sqlprov_{qid}_p2;\n')
            f.write(f'explain (analyze, timing off) create table {THIS_BENCHMARK}_sqlprov_{qid}_p2 as \n {spSQL2};\n')
            f.write(f'select pg_relation_size(\'{THIS_BENCHMARK}_sqlprov_{qid}_p2\') ;\n')

        # p4
        with open(f'{CURR_PATH}/sqlprov/capPq{qid}_p4.sql', 'w') as f:
            queryQ = """
            explain (analyze, timing off)
            select ga, ava, avb, {THIS_BENCHMARK}_sqlprov_{qid}_p2.provone as provone, {THIS_BENCHMARK}_sqlprov_{qid}_p2.provtwo as provtwo
            from {THIS_BENCHMARK}_sqlprov_{qid}_p1 join  {THIS_BENCHMARK}_sqlprov_{qid}_p2 on ({THIS_BENCHMARK}_sqlprov_{qid}_p1.tuid = {THIS_BENCHMARK}_sqlprov_{qid}_p2.tuid);
            """
            f.write(queryQ.format(THIS_BENCHMARK=THIS_BENCHMARK, qid=qid))
        # p5
        with open(f'{CURR_PATH}/sqlprov/capPq{qid}_p5.sql', 'w') as f:
            queryQ = f"""
            drop table if exists {THIS_BENCHMARK}_sqlprov_{qid}_p5;
            explain (analyze, timing off)  create table {THIS_BENCHMARK}_sqlprov_{qid}_p5 as
            select ga, ava, avb, {THIS_BENCHMARK}_sqlprov_{qid}_p2.provone as provone, {THIS_BENCHMARK}_sqlprov_{qid}_p2.provtwo as provtwo
            from {THIS_BENCHMARK}_sqlprov_{qid}_p1 join  {THIS_BENCHMARK}_sqlprov_{qid}_p2 on ({THIS_BENCHMARK}_sqlprov_{qid}_p1.tuid = {THIS_BENCHMARK}_sqlprov_{qid}_p2.tuid);
            """
            f.write(queryQ.format(THIS_BENCHMARK=THIS_BENCHMARK, qid=qid))

        # p6
        with open(f'{CURR_PATH}/sqlprov/capPq{qid}_p6.sql', 'w') as f:
            CQ = """
            explain (analyze, timing off)
            select ga, ava, avb
            From {THIS_BENCHMARK}_sqlprov_{qid}_p5
            where exists (select 1 from vpgn1k_1 where {CCOND} and vpgn1k_1.tuid = any({THIS_BENCHMARK}_sqlprov_{qid}_p5.provone));
            """
            for ccond in cconditions:
                f.write(CQ.format(THIS_BENCHMARK=THIS_BENCHMARK, qid=qid, CCOND=ccond))
        with open(f'{CURR_PATH}/sqlprov/capPq{qid}_p6.sql', 'a') as f:

            allQ = """
            explain (analyze, timing off)
            with  origg as (
                select vpgn1k_1.tuid as tuid1, vpgn1k_1.ga as ga,  vpgn1k_1.id as id, vpgn1k_1.vb as vb,
                    jc_1.tuid as tuid2, jc_1.c1to10 as c1to10, jc_1.c1to1 as c1to1, jc_1.c1to50 as c1to50, jc_1.jid as jid
                from (select * from vpgn1k_1 where {COND} and {CCOND}) as vpgn1k_1
                join jc_1 on vpgn1k_1.ga = jc_1.c1to10
            )
            select *
            from {THIS_BENCHMARK}_sqlprov_{qid}_p5 joinedd, origg
            where origg.tuid1 = any(joinedd.provone) and origg.tuid2 = any(joinedd.provtwo);
            """
            for ccond in cconditions:
                f.write(allQ.format(THIS_BENCHMARK=THIS_BENCHMARK, qid=qid, COND=cond, CCOND=ccond))







        # ---------- provsql
        pSQL = s_util.buildSQLFromTemplate(QTemplate, ['TABLE', 'JOINED_TBL', 'WHERECONDITION'], [f'{table}', f'{jointable}', cond])
#
        s_util.writeStrToFile(f'{pSQL};', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}.sql')
        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p1.sql', f_util.SYS_ProvSQL, isDuckDBBackend=False)

        Q2 = """
        explain (analyze, timing off)
        select *, sr_which(provenance(), 'mapping_vpgn1k') as provone, sr_which(provenance(), 'mapping_jc') as provtwo
        from (
            select ga, avg(va) as ava, avg(vb) as avb from vpgn1k, jc WHERE ga = c1to10 AND {WHERECONDITION} group by ga
        ) provs;

        """
        with open(f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p2.sql', 'w') as f:
            f.write(Q2.format(THIS_BENCHMARK=THIS_BENCHMARK, qid=qid, tableName=table, joinedTable=jointable, WHERECONDITION=cond))

        Q3 = """
        drop table if exists {THIS_BENCHMARK}_provsql_{qid}_p3;
        set max_parallel_workers_per_gather = 0;
        explain (analyze, timing off) create table {THIS_BENCHMARK}_provsql_{qid}_p3 as
        select *, sr_which(provenance(), 'mapping_vpgn1k') as provone, sr_which(provenance(), 'mapping_jc') as provtwo
        from (
            select ga, avg(va) as ava, avg(vb) as avb from vpgn1k, jc WHERE ga = c1to10 AND {WHERECONDITION} group by ga
        ) provs;

        select pg_relation_size('{THIS_BENCHMARK}_provsql_{qid}_p3') ;
        """
        with open(f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p3.sql', 'w') as f:
            f.write(Q3.format(THIS_BENCHMARK=THIS_BENCHMARK, qid=qid, tableName=table, joinedTable=jointable, WHERECONDITION=cond))

        # q4: query the needed data.
        Q4 = """
        explain (analyze, timing off)
        select ss.ga as ga, tt.ava as ava, tt.avb as avb,  provone,  provtwo
        from {THIS_BENCHMARK}_provsql_{qid}_p3 ss,
            (select ga, avg(va) as ava, avg(vb) as avb from vpgn1k join jc on (ga = c1to10) group by ga) tt
        where ss.ga = tt.ga;
        """
        with open(f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p4.sql', 'w') as f:
            f.write(Q4.format(THIS_BENCHMARK=THIS_BENCHMARK, qid=qid))

        # q5: query the needed data and write into table.
        Q5 = """
        drop table if exists {THIS_BENCHMARK}_provsql_{qid}_p5;
        explain (analyze, timing off) create table {THIS_BENCHMARK}_provsql_{qid}_p5 as
        select ss.ga as ga, tt.ava as ava, tt.avb as avb,  provone,  provtwo
        from {THIS_BENCHMARK}_provsql_{qid}_p3 ss,
            (select ga, avg(va) as ava, avg(vb) as avb from vpgn1k join jc on (ga = c1to10) group by ga) tt
        where ss.ga = tt.ga;

        select pg_relation_size('{THIS_BENCHMARK}_provsql_{qid}_p5') ;
        """
        with open(f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p5.sql', 'w') as f:
            f.write(Q5.format(THIS_BENCHMARK=THIS_BENCHMARK, qid=qid))

        with open (f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p6.sql', 'w') as f:
            Q6 = """
            explain (analyze, timing off)
            select ga, ava, avb
            from {THIS_BENCHMARK}_provsql_{qid}_p5
            where exists (select 1 from vpgn1k where {ccond} and vpgn1k.id = any({THIS_BENCHMARK}_provsql_{qid}_p5.provone::integer[]));
            """
            for ccond in cconditions:
                f.write(Q6.format(THIS_BENCHMARK=THIS_BENCHMARK, qid=qid, ccond=ccond))

        with open (f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p6.sql', 'a') as f:
            Q5 ="""
            explain (analyze, timing off)
            with joinedd as (
                select ga, ava, avb, provone, provtwo
                from {THIS_BENCHMARK}_provsql_{qid}_p5
            ),
            origg as (
                select * from (select * from vpgn1k where {COND} and {CCOND}) join jc on (ga = c1to10)
            )
            select *
            from joinedd, origg
            where origg.id = any(joinedd.provone::integer[]) and origg.jid = any(joinedd.provtwo::integer[]);
            """
            for ccond in cconditions:
                f.write(Q5.format(THIS_BENCHMARK=THIS_BENCHMARK, qid=qid, COND=cond, CCOND=ccond))

        # ---- smd
        sSQL = s_util.buildSQLFromTemplate(QTemplate, ['TABLE', 'JOINED_TBL', 'WHERECONDITION'], [f'{table}', f'{jointable}', cond])
        s_util.writeStrToFile(f'{sSQL};', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/q{qid}.sql')
        # --- phase I
        q_util.make_executable_smd_p1(sSQL, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p1.sql')
        # --- export table
        tableList = q_util.duckdbGetAllLineageTables(SMDCFG["duckdb_bin"], SMDCFG["database_path"], sSQL + ";")
        q_util.make_executable_smd_export(tableList, sSQL, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_export.sql', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}')
        # -- import table
        q_util.make_executable_smd_import(tableList, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_import.sql', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}')
        # -- phase II
        LINQ = q_util.duckdbGetLineageQuery(SMDCFG["duckdb_bin"], SMDCFG["database_path"], sSQL + ";")
        q_util.make_executable_smd_p2(LINQ + ";", f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p2.sql')
        # -- phase III
        q_util.make_executable_smd_p3(LINQ + ";", f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p3.sql', f'{THIS_BENCHMARK}_smd_{qid}')
        # --- phase IV
        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p4.sql', f_util.SYS_SmokedDuck, True)
        # --- phase V 
        q_util.make_executable_smd_p3(sSQL, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p5.sql', f'{THIS_BENCHMARK}_smd_{qid}_p5')

        # -- phase IV

        smdConditions = [
                'vpgn1k.ga = 900',
                'vpgn1k.ga >= 900 and vpgn1k.ga <= 903',
                'vpgn1k.ga >= 900 and vpgn1k.ga <= 915',
               ]


        with open (f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p6.sql', 'w') as f:
            f.write('.timer on\n set threads to 1;')
            SELECT = """
            explain analyze 
            select distinct PMFD2_smd_{qid}_p5.ga, PMFD2_smd_{qid}_p5.ava, PMFD2_smd_{qid}_p5.avb from PMFD2_smd_{qid}, PMFD2_smd_{qid}_p5, vpgn1k where PMFD2_smd_{qid}.out_index = PMFD2_smd_{qid}_p5.rowid and vpgn1k.rowid = PMFD2_smd_{qid}.vpgn1k and {WHERECONDITION};
            """
            for ccond in smdConditions:
                f.write(SELECT.format(THIS_BENCHMARK=THIS_BENCHMARK, qid=qid, WHERECONDITION=ccond))
        
        with open (f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p6.sql', 'a') as f:
            SELECT = """
            explain analyze
            select distinct PMFD2_smd_{qid}_p5.ga, PMFD2_smd_{qid}_p5.ava, PMFD2_smd_{qid}_p5.avb, vpgn1k.id, vpgn1k.ga, vpgn1k.va, vpgn1k.vb, jc.jid, jc.c1to10, jc.c1to1, jc.c1to50 from PMFD2_smd_{qid}, PMFD2_smd_{qid}_p5, vpgn1k, jc where PMFD2_smd_{qid}.out_index = PMFD2_smd_{qid}_p5.rowid and vpgn1k.rowid = PMFD2_smd_{qid}.vpgn1k and jc.rowid = PMFD2_smd_{qid}.jc and {WHERECONDITION};
            """
            for ccond in smdConditions:
                f.write(SELECT.format(THIS_BENCHMARK=THIS_BENCHMARK, qid=qid, WHERECONDITION=ccond))
        
        qid += 1



    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_GProM, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_ProvSQL, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_SQLProv, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_SmokedDuck, 1, qid-1)










if __name__ == "__main__":
    f_util.lodConfig(THIS_BENCHMARK)

    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_GProM)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_ProvSQL)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_SQLProv)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_SmokedDuck)

    run()
