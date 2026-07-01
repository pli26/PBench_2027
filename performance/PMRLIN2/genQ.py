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

THIS_BENCHMARK = 'PMRLIN2'
CURR_PATH = os.getcwd()

def run():
    CFGs = f_util.loadJsonConfig(f'{os.getcwd()}/systems.config')
    SMDCFG = CFGs[f_util.SYS_SmokedDuck + 'pre']
    qid = 1

    tables = ['fp1', 'fp2', 'fp3', 'fp']
    jointable = 'jc'
    TableAndAttr = f_util.loadJsonConfig(f'{ROOT}/utils/tables.cfg')
    tableAttr = TableAndAttr['fp']
    jointableAttr = TableAndAttr['jc']
    for table in tables:

        QTemplate = f_util.readTemplate(f'{CURR_PATH}/templates/q.sql')

        # -------------------smd
        sSQL = s_util.buildSQLFromTemplate(QTemplate, ['TABLE', 'JOINED_TBL'], [f'{table}', f'{jointable}'])

        s_util.writeStrToFile(f'{sSQL};', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/q{qid}.sql')

        # -- Phase I
        q_util.make_executable_smd_p1(f'{sSQL};', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p1.sql')
        # -- export table
        tableList = q_util.duckdbGetAllLineageTables(SMDCFG['duckdb_bin'], SMDCFG['database_path'], sSQL + ";")
        q_util.make_executable_smd_export(tableList, sSQL, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_export.sql', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}')
        # -- import table
        q_util.make_executable_smd_import(tableList, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_import.sql', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}')
        # -- Phase II
        LINQ = q_util.duckdbGetLineageQuery(SMDCFG['duckdb_bin'], SMDCFG['database_path'], sSQL + ";")
        q_util.make_executable_smd_p2(f'{LINQ};', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p2.sql')
        # -- Phase III
        q_util.make_executable_smd_p3(f'{LINQ}', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p3.sql', f'{THIS_BENCHMARK}_smd_{qid}')
        # -- Phase IV
        storedTBLNames = [f'{THIS_BENCHMARK}_smd_{qid}_{table}', f'{THIS_BENCHMARK}_smd_{qid}_{jointable}']
        q_util.make_executable_smd_p4(f'{LINQ}',
                                      f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p4.sql',
                                        f'{THIS_BENCHMARK}_smd_{qid}',
                                        [f'{table}', f'{jointable}'],
                                        [f'{table}', f'{jointable}'],
                                        [f'{tableAttr}', f'{jointableAttr}'],
                                        storedTBLNames=storedTBLNames)
        # -- Phase V
        q_util.make_executable_smd_p5(f'{LINQ}',
                                      f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p5.sql',
                                      f'{THIS_BENCHMARK}_smd_{qid}',
                                      [f'{table}', f'{jointable}'],
                                      [f'{table}', f'{jointable}'],
                                      [f'{tableAttr}', f'{jointableAttr}'],
                                      storedTBLNames=storedTBLNames)
        # -- Phase VI
        rpdQ = f'select gb, min(va) as minva from {THIS_BENCHMARK}_smd_{qid}_{table} join {THIS_BENCHMARK}_smd_{qid}_{jointable} on gb = c1to10 group by gb;'
        q_util.make_executable_smd_p6(f'{LINQ}', f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p6.sql', rpdQ)

        ## each lineage table is stored as {table}_lineage

        # rpdQ = s_util.buildSQLFromTemplate(QTemplate, ['TABLE', 'JOINED_TBL'], [f'{table}_lineage', f'{jointable}_lineage'])
        # q_util.make_executable_smd_rpdO(SMDCFG["duckdb_bin"], SMDCFG["database_path"], sSQL, f'{CURR_PATH}/{f_util.SYS_SmokedDuck}/capDq{qid}_p2.sql', f'rpd_smd_{qid}', [f'{table}', f'{jointable}'], [f'{table}', f'{jointable}'], rpdQ)

        # ----- sqlprov
        f_util.SQLProvPreFile(THIS_BENCHMARK)
        f_util.SQLProvLogSizeFile(THIS_BENCHMARK, ['logjoin', 'logfilter', 'logaggregation'])
        spTemplate1 = f_util.readTemplate(f'{CURR_PATH}/templates/sp_p1.sql')
        spSQL1 = s_util.buildSQLFromTemplate(spTemplate1, ['TABLE', 'JOINED_TBL'], [f'{table}', f'{jointable}'])
        s_util.writeStrToFile(f'{spSQL1};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql')
        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p1.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p1.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)

        spTemplate2 = f_util.readTemplate(f'{CURR_PATH}/templates/sp_p2.sql')
        spSQL2 = s_util.buildSQLFromTemplate(spTemplate2, ['TABLE', 'JOINED_TBL'], [f'{table}', f'{jointable}'])
        s_util.writeStrToFile(f'{spSQL2};', f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql')

        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p2.sql', f_util.SYS_SQLProv, isDuckDBBackend=False)

        q_util.make_executable_sqlprov_rpd_p3(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p3.sql', f'{THIS_BENCHMARK}_sqlprov_{qid}')
        storedTBLNames = [f'{THIS_BENCHMARK}_sqlprov_{qid}_{table}', f'{THIS_BENCHMARK}_sqlprov_{qid}_{jointable}']
        q_util.make_executable_sqlprov_rpd_p4(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p4.sql', f'{THIS_BENCHMARK}_sqlprov_{qid}',
                                              [f'provone', f'provtwo'], [f'{table}', f'{jointable}'], [f'tuid,{tableAttr}', f'tuid,{jointableAttr}'], storedTBLNames=storedTBLNames)

        q_util.make_executable_sqlprov_rpd_p5(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p5.sql',
                                              f'{THIS_BENCHMARK}_sqlprov_{qid}', [f'provone', f'provtwo'],
                                              [f'{table}', f'{jointable}'], [f'tuid,{tableAttr}', f'tuid,{jointableAttr}'],
                                              storedTBLNames=storedTBLNames)
        rpdQ = f'select gb, min(va) as minva from {THIS_BENCHMARK}_sqlprov_{qid}_{table} join {THIS_BENCHMARK}_sqlprov_{qid}_{jointable} on gb = c1to10 group by gb;'
        q_util.make_executable_sqlprov_rpd_p6(f'{CURR_PATH}/{f_util.SYS_SQLProv}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_SQLProv}/capPq{qid}_p6.sql', rpdQ)
        # ------ gprom
        # dt
        s_util.writeStrToFile(f'provenance of ({sSQL});', f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}.sql')
        q_util.gprom_rewrite(f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql', isDuckDBBackend=False)
        q_util.gprom_rewrite(f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql', isDuckDBBackend=True)

        q_util.make_executable_gprom_rpd_p1(f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}_p1.sql',  isDuckDBBackend=False)
        q_util.make_executable_gprom_rpd_p1(f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}_p1.sql',  isDuckDBBackend=True)

        q_util.make_executable_gprom_rpd_p2(f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}_p2.sql',  [f'{THIS_BENCHMARK}_gprom_{qid}'], isDuckDBBackend=False)
        q_util.make_executable_gprom_rpd_p2(f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}_p2.sql',  [f'{THIS_BENCHMARK}_gprom_{qid}'], isDuckDBBackend=True)
        distinctWhat = []
        distinctWhat1 = f'prov_{table}_id, prov_{table}_ga, prov_{table}_gb, prov_{table}_gc, prov_{table}_va, prov_{table}_vb, prov_{table}_vc, prov_{table}_hv'
        distinctWhat2 = f'prov_{jointable}_jid, prov_{jointable}_c1to10, prov_{jointable}_c1to1, prov_{jointable}_c1to50'
        distinctWhat.append(distinctWhat1)
        distinctWhat.append(distinctWhat2)
        q_util.make_executable_gprom_rpd_p3(f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}_p3.sql', distinctWhat, [f'{THIS_BENCHMARK}_gprom_{qid}', f'{THIS_BENCHMARK}_gprom_{qid}'], isDuckDBBackend=False)
        q_util.make_executable_gprom_rpd_p3(f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}_p3.sql', distinctWhat, [f'{THIS_BENCHMARK}_gprom_{qid}', f'{THIS_BENCHMARK}_gprom_{qid}'], isDuckDBBackend=True)

        q_util.make_executable_gprom_rpd_p4(
            f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}_p4.sql',
            [f'{THIS_BENCHMARK}_gprom_{qid}_{table}', f'{THIS_BENCHMARK}_gprom_{qid}_{jointable}'],
            distinctWhat,
            [f'{THIS_BENCHMARK}_gprom_{qid}', f'{THIS_BENCHMARK}_gprom_{qid}'],
            False
        )
        q_util.make_executable_gprom_rpd_p4(
            f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}_p4.sql',
            [f'{THIS_BENCHMARK}_gprom_{qid}_{table}', f'{THIS_BENCHMARK}_gprom_{qid}_{jointable}'],
            distinctWhat,
            [f'{THIS_BENCHMARK}_gprom_{qid}', f'{THIS_BENCHMARK}_gprom_{qid}'],
            True
        )

        gpromrpdq = f'select prov_{table}_gb as gb, min(prov_{table}_va) as minva from {THIS_BENCHMARK}_gprom_{qid}_{table} join {THIS_BENCHMARK}_gprom_{qid}_{jointable} on prov_{table}_gb = prov_{jointable}_c1to10 group by prov_{table}_gb;'
        q_util.make_executable_gprom_rpd_p5(
            f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}_p5.sql',
            gpromrpdq,
            False
        )
        q_util.make_executable_gprom_rpd_p5(
            f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}_p5.sql',
            gpromrpdq,
            True
        )










        # gStoredTable = f'{THIS_BENCHMARK}_gprom_dt_{qid}'
        # rpdQ = f'select prov_{table}_gb as gb, min(prov_{table}_va) as minva from (select distinct prov_{table}_id, prov_{table}_gb, prov_{table}_va from lineages) join (select distinct prov_{jointable}_jid, prov_{jointable}_c1to10 from lineages) on prov_{table}_gb = prov_{jointable}_c1to10 group by prov_{table}_gb;'
        # q_util.make_executable_gprom_rpd_dt(
        #     f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}.sql',
        #     f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}_dt.sql',
        #     rpdQ,
        #     f'{THIS_BENCHMARK}_gprom_dt_{qid}',
        #     isDuckDBBackend=False)
        # q_util.make_executable_gprom_rpd_dt(
        #     f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}.sql',
        #     f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}_dt.sql',
        #     rpdQ,
        #     f'{THIS_BENCHMARK}_gprom_dt_{qid}',
        #     isDuckDBBackend=True)
        # # #id
        # gSQLid = s_util.buildSQLFromTemplate(QTemplate, ['TABLE', 'JOINED_TBL'], [f'{table} use provenance(id)', f'{jointable} use provenance(jid)'])
        # s_util.writeStrToFile(f'provenance of ({gSQLid});', f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}_id.sql')

        # q_util.gprom_rewrite(f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}_id.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}_id.sql', isDuckDBBackend=False)
        # q_util.gprom_rewrite(f'{CURR_PATH}/{f_util.SYS_GProM}/q{qid}_id.sql', f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}_id.sql', isDuckDBBackend=True)
        # rpdQ = s_util.buildSQLFromTemplate(QTemplate, ['TABLE', 'JOINED_TBL'], [f'{THIS_BENCHMARK}_gprom_id_{qid}_{table}', f'{THIS_BENCHMARK}_gprom_id_{qid}_{jointable}'])
        # q_util.make_executable_gprom_rpd_id(
        #     f'{CURR_PATH}/{f_util.SYS_GProM}/rwPq{qid}_id.sql',
        #     f'{CURR_PATH}/{f_util.SYS_GProM}/capPq{qid}_id.sql',
        #     f'{THIS_BENCHMARK}_gprom_id_{qid}',
        #     [f'prov_{table}_id', f'prov_{jointable}_jid'],
        #     [f'{table}', f'{jointable}'],
        #     ['id', 'jid'],
        #     [f'{THIS_BENCHMARK}_gprom_id_{qid}_{table}', f'{THIS_BENCHMARK}_gprom_id_{qid}_{jointable}'],
        #     rpdQ=rpdQ,
        #     WHERECOND= None,
        #     isDuckDBBackend=False)
        # q_util.make_executable_gprom_rpd_id(
        #     f'{CURR_PATH}/{f_util.SYS_GProM}/rwDq{qid}_id.sql',
        #     f'{CURR_PATH}/{f_util.SYS_GProM}/capDq{qid}_id.sql',
        #     f'{THIS_BENCHMARK}_gprom_id_{qid}',
        #     [f'prov_{table}_id', f'prov_{jointable}_jid'],
        #     [f'{table}', f'{jointable}'],
        #     ['id', 'jid'],
        #     [f'{THIS_BENCHMARK}_gprom_id_{qid}_{table}', f'{THIS_BENCHMARK}_gprom_id_{qid}_{jointable}'],
        #     rpdQ=rpdQ,
        #     WHERECOND= None,
        #     isDuckDBBackend=True)

        # ---------- provsql
        pSQL = s_util.buildSQLFromTemplate(QTemplate, ['TABLE', 'JOINED_TBL'], [f'{table}', f'{jointable}'])

        s_util.writeStrToFile(f'{pSQL};', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}.sql')
        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}.sql', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p1.sql', f_util.SYS_ProvSQL, isDuckDBBackend=False)

        fetchQ = f_util.readTemplate(f'{CURR_PATH}/templates/prov.sql')
        fetchQ = s_util.buildSQLFromTemplate(fetchQ, ['{tableName}', '{joinedTable}'], [f'{table}', f'{jointable}'])
        s_util.writeStrToFile(f'{fetchQ};', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}_p2.sql')

        q_util.make_executable(f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p2.sql', f_util.SYS_ProvSQL, isDuckDBBackend=False)

        q_util.make_executable_provsql_rpd_p3(f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}_p2.sql', f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p3.sql', f'{THIS_BENCHMARK}_provsql_{qid}')

        q_util.make_executable_provsql_rpd_p4(
            f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}_p2.sql',
            f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p4.sql',
            f'{THIS_BENCHMARK}_provsql_{qid}',
            [f'provone', f'provtwo'],
            [f'{table}', f'{jointable}'],
            ['id', 'jid'])
            # [f'{THIS_BENCHMARK}_provsql_{qid}_{table}', f'{THIS_BENCHMARK}_provsql_{qid}_{jointable}'])

        q_util.make_executable_provsql_rpd_p5(
            f'{CURR_PATH}/{f_util.SYS_ProvSQL}/q{qid}_p2.sql',
            f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p5.sql',
            f'{THIS_BENCHMARK}_provsql_{qid}',
            [f'provone', f'provtwo'],
            [f'{table}', f'{jointable}'],
            ['id', 'jid'],
            [f'{THIS_BENCHMARK}_provsql_{qid}_{table}', f'{THIS_BENCHMARK}_provsql_{qid}_{jointable}'])

        rpdQ = f'select gb, min(va) as minva from {THIS_BENCHMARK}_provsql_{qid}_{table} join {THIS_BENCHMARK}_provsql_{qid}_{jointable} on gb = c1to10 group by gb;'
        q_util.make_executable_provsql_rpd_p6( f'{CURR_PATH}/{f_util.SYS_ProvSQL}/capPq{qid}_p6.sql', rpdQ)

        qid += 1

    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_GProM, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_ProvSQL, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_SmokedDuck, 1, qid-1)
    f_util.updateQCnts(THIS_BENCHMARK, f_util.SYS_SQLProv, 1, qid-1)









if __name__ == "__main__":
    f_util.lodConfig(THIS_BENCHMARK)

    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_GProM)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_ProvSQL)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_SmokedDuck)
    f_util.createQFolder(THIS_BENCHMARK, f_util.SYS_SQLProv)

    run()