import fileUtils as f_util
import os
import json
from pathlib import Path
import subprocess
# Compute project root relative to this file
ROOT = Path(__file__).resolve().parents[1]

IS_SHOWN_LOG = True


def LOG(msg, MUST=False):
    if MUST:
        print(msg)
    elif IS_SHOWN_LOG:
        print(msg)


def readQueryFileAsList(filename):
    readF = open(filename, 'r')
    fileLines = readF.readlines()
    readF.close()

    # remove ";"
    lines = []
    for fileLine in fileLines:
        line = fileLine.strip()
        if len(line) > 0 and line[-1] == ';':
            line = line[:-1]
        if len(line) > 0:
            lines.append(line + '\n')
    return lines
# ------------------------------------------------------------------------------
# GProM Utils
# ------------------------------------------------------------------------------


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
        ]
        # '-prov_use_composable', 'TRUE']

    return gpromCMD


def gprom_rewrite(infile, outfile, isDuckDBBackend=False):
    with open(f'{ROOT}/utils/systems.cfg', 'r') as jsonFile:
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
                LOG(f"Error rewriting sql {process.stderr}", True)
                return (rt, process.stderr)
            LOG(process.stdout)
            out.write(process.stdout)
    except Exception as e:
        LOG(f'ERROR in gprom rewrite {e}\n', True)


def make_executable_gprom_capture(infile, outfile, isDuckDBBackend=False):
    lines = readQueryFileAsList(infile)
    with open(f'{outfile}', 'w') as ff:
        if isDuckDBBackend:
            ff.write('.timer on \n')
            ff.write('set threads to 1;\n')
            ff.write('explain analyze \n')
        else:
            ff.write(f'EXPLAIN(ANALYZE, TIMING OFF) \n')
        for line in lines:
            aLine = line
            if len(aLine) > 0 and 'IS NOT DISTINCT FROM' in aLine:
                aLine = aLine.replace('IS NOT DISTINCT FROM', '=')
            ff.write(aLine)
        ff.write(';')


def make_executable_gprom_capture_res_row_cnt(infile, outfile, tblname, isDuckDBBackend=False):
    lines = readQueryFileAsList(infile)
    with open(f'{outfile}', 'w') as ff:
        if isDuckDBBackend:
            ff.write('.timer on \n')
            ff.write('set threads to 1;\n')
            ff.write(f'drop table if exists {tblname};\n')
            ff.write(f'explain analyze create table {tblname} as \n')
        else:
            ff.write(f'drop table if exists {tblname};\n')
            ff.write(
                f'EXPLAIN(ANALYZE, TIMING OFF) create table {tblname} as \n')
        for line in lines:
            aLine = line
            if len(aLine) > 0 and 'IS NOT DISTINCT FROM' in aLine:
                aLine = aLine.replace('IS NOT DISTINCT FROM', '=')
            ff.write(aLine)
        ff.write(';\n')
        ff.write(f'select count(1) from {tblname};\n')


def make_executable(infile, outfile, system, isDuckDBBackend=False):
    lines = readQueryFileAsList(infile)
    with open(f'{outfile}', 'w') as ff:
        if isDuckDBBackend:
            ff.write('.timer on \n')
            ff.write('set threads to 1;\n')
            ff.write('explain analyze ')
        else:
            ff.write(f'EXPLAIN(ANALYZE, TIMING OFF) \n')

        for line in lines:
            aLine = line
            if system == f_util.SYS_GProM:
                if len(aLine) > 0 and 'IS NOT DISTINCT FROM' in aLine:
                    aLine = aLine.replace('IS NOT DISTINCT FROM', '=')
            ff.write(aLine)
        ff.write(';')


def make_executable_with_size_count(infile, outfile, system, idDuckDBBackend=False, isCountRes=False, tablesToQuery: list = None):
    lines = readQueryFileAsList(infile)
    with open(f'{outfile}', 'w') as ff:
        if isDuckDBBackend:
            ff.write('.timer on \n')
            ff.write('set threads to 1;\n')
            ff.write('explain analyze ')
        else:
            ff.write(f'EXPLAIN(ANALYZE, TIMING OFF) \n')

        for line in lines:
            aLine = line
            if system == f_util.SYS_GProM:
                if len(aLine) > 0 and 'IS NOT DISTINCT FROM' in aLine:
                    aLine = aLine.replace('IS NOT DISTINCT FROM', '=')
            ff.write(aLine)
        ff.write(';')


def make_executable_use_case(infile, outfile, system, tblname, isDuckDBBackend=False, tablesToQuery=None):
    lines = readQueryFileAsList(infile)
    with open(f'{outfile}', 'w') as ff:
        if isDuckDBBackend:
            ff.write(f'.timer on \n')
            ff.write(f'set threads to 1;\n')
            ff.write(f'drop table if exists {tblname};\n')
            ff.write(f'explain analyze \n')
            ff.write(f'create table {tblname} as \n')
        else:
            ff.write(f'drop table if exists {tblname};\n')
            ff.write(f'set max_parallel_workers_per_gather = 0;\n')
            ff.write(f'EXPLAIN(ANALYZE, TIMING OFF) \n')
            ff.write(f'create table {tblname} as \n')
        for line in lines:
            aLine = line
            if system == f_util.SYS_GProM:
                if len(aLine) > 0 and 'IS NOT DISTINCT FROM' in aLine:
                    aLine = aLine.replace('IS NOT DISTINCT FROM', '=')
            ff.write(aLine)
        ff.write(';\n')
        if isDuckDBBackend:
            for tbl in tablesToQuery:
                ff.write(f'SELECT \'{tbl}\' AS table_name, count(DISTINCT block_id) AS num_blocks, format_bytes(count(DISTINCT block_id) * (SELECT block_size FROM pragma_database_size())) AS total_size FROM pragma_storage_info(\'{tbl}\') WHERE block_id IS NOT NULL;\n')
                ff.write(f'select count(1) as {tbl}_row from {tbl};\n')
        else:
            for tbl in tablesToQuery:
                ff.write(
                    f'select pg_total_relation_size(\'{tbl}\') AS size;\n')
                ff.write(f'select count(1) as {tbl}_row from {tbl};\n')


def make_executable_storage(infile, outfile, system, tblname, tablesToQuery: list, isDuckDBBackend=False):
    lines = readQueryFileAsList(infile)
    with open(f'{outfile}', 'w') as ff:
        if isDuckDBBackend:
            ff.write(f'.timer on \n')
            ff.write(f'set threads to 1;\n')
            ff.write(f'drop table if exists {tblname};\n')
            ff.write(f'create table {tblname} as \n')
        else:
            ff.write(f'drop table if exists {tblname};\n')
            ff.write(f'set max_parallel_workers_per_gather = 0;\n')
            ff.write(f'create table {tblname} as \n')
        for line in lines:
            aLine = line
            if system == f_util.SYS_GProM:
                if len(aLine) > 0 and 'IS NOT DISTINCT FROM' in aLine:
                    aLine = aLine.replace('IS NOT DISTINCT FROM', '=')
            ff.write(aLine)
        ff.write(';\n')
        if isDuckDBBackend:
            for tbl in tablesToQuery:
                ff.write(f'SELECT \'{tbl}\' AS table_name, count(DISTINCT block_id) AS num_blocks, format_bytes(count(DISTINCT block_id) * (SELECT block_size FROM pragma_database_size())) AS total_size FROM pragma_storage_info(\'{tbl}\') WHERE block_id IS NOT NULL;\n')
                ff.write(f'select count(1) as {tbl}_row from {tbl};\n')
        else:
            for tbl in tablesToQuery:
                ff.write(
                    f'select pg_total_relation_size(\'{tbl}\') AS size;\n')
                ff.write(f'select count(1) as {tbl}_row from {tbl};\n')


def make_executable_smd_storage(outfile, tblname, query, queryLin, tablesToQuery: list):
    with open(f'{outfile}', 'w') as ff:
        ff.write(f'.timer on \n')
        ff.write(f'set threads to 1;\n')
        ff.write(f'drop table if exists {tblname};\n')
        ff.write(f'pragma enable_lineage;\n')
        ff.write(f'{query}\n')
        ff.write(f'explain analyze \n')
        ff.write(f'create table {tblname} as \n')
        ff.write(f'{queryLin}\n')
        for tbl in tablesToQuery:
            ff.write(f'SELECT \'{tbl}\' AS table_name, count(DISTINCT block_id) AS num_blocks, format_bytes(count(DISTINCT block_id) * (SELECT block_size FROM pragma_database_size())) AS total_size FROM pragma_storage_info(\'{tbl}\') WHERE block_id IS NOT NULL;\n')
            ff.write(f'select count(1) as {tbl}_row from {tbl};\n')
        ff.write('pragma disable_lineage;\n')

SIZE_Q = """
SELECT '{TBL}' AS table_name,
    count(distinct block_id) AS num_blocks,
    count(distinct block_id) * (SELECT block_size FROM pragma_database_size()) AS total_bytes,
    format_bytes(count(distinct block_id) * (SELECT block_size FROM pragma_database_size())) AS human_readable
    FROM pragma_storage_info('{TBL}');
"""

def make_executable_smd_rmtbl(tableList: list, outfile):
    with open(f'{outfile}', 'w') as ff:
        for tbl in tableList:
            ff.write(f'drop table if exists {tbl};\n')

def make_executable_smd_rmtbldisk(tableList: list, outfile, storagepath):
    with open(f'{outfile}', 'w') as ff:
        for tbl in tableList:
            ff.write(f'{storagepath}/{tbl}.parquet\n')

def make_executable_smd_p1(query, outfile):
    query = query.strip()
    if query[-1] == ';':
        query = query[:-1]

    with open(f'{outfile}', 'w') as ff:
        ff.write('.timer on \n')
        ff.write('set threads to 1;\n')
        ff.write('pragma enable_lineage;\n')
        ff.write(f'explain analyze {query};\n')
        ff.write('pragma disable_lineage;\n')
def make_executable_smd_export(tableList, query, outfile, benchpath):
    with open(f'{outfile}', 'w') as ff:
        ff.write(f'.timer on \n')
        ff.write(f'set threads to 1;\n')
        ff.write(f'pragma enable_lineage;\n')
        ff.write(f'{query};\n')
        ff.write(f'pragma disable_lineage;\n\n')
        for tbl in tableList:
            ff.write(f'copy {tbl} to \'{benchpath}/{tbl}.parquet\' (format parquet);\n\n')

def make_executable_smd_import(tableList, outfile, benchpath):
    with open(f'{outfile}', 'w') as ff:
        ff.write(f'.timer on \n')
        ff.write(f'set threads to 1;\n')
        for tbl in tableList:
            ff.write(f'drop table  if exists {tbl};\n')
            ff.write(f'create table {tbl} as select * from read_parquet(\'{benchpath}/{tbl}.parquet\');\n\n')

        for tbl in tableList:
            sizeQ = SIZE_Q
            sizeQ = sizeQ.replace('{TBL}', f'{tbl}')
            ff.write(f'{sizeQ};\n\n')

def make_executable_smd_p2(query, outfile):
    query = query.strip()
    if query[-1] == ';':
        query = query[:-1]

    with open(f'{outfile}', 'w') as ff:
        ff.write('.timer on \n')
        ff.write('set threads to 1;\n')
        ff.write(f'explain analyze {query};\n')

def make_executable_smd_p3(query, outfile, storedTable):
    query = query.strip()
    if query[-1] == ';':
        query = query[:-1]
    with open(f'{outfile}', 'w') as ff:
        ff.write(f'.timer on \n')
        ff.write(f'set threads to 1;\n')
        ff.write(f'drop table if exists {storedTable};\n')
        ff.write(f'explain analyze create table {storedTable} as {query};\n')
        ff.write(f'select \'{storedTable}\' as table_name, count(DISTINCT block_id) AS num_blocks, count(distinct block_id) * (SELECT block_size FROM pragma_database_size()) AS total_bytes, format_bytes(count(DISTINCT block_id) * (SELECT block_size FROM pragma_database_size())) AS total_size FROM pragma_storage_info(\'{storedTable}\') WHERE block_id IS NOT NULL;\n')
def make_executable_smd_p4(infile, outfile, storedTable, tablesToQuery: list, originalTbl: list, tAttributes: list, storedTBLNames:list):
    with open(f'{outfile}', 'w') as ff:
        ff.write(f"select 'start to query lineage data from {storedTable} by each table';\n")
        ff.write(f'set threads to 1;\n')
        for id in range(len(tablesToQuery)):
            tToQuery = tablesToQuery[id]
            oTBL =  originalTbl[id]
            attr = tAttributes[id]
            tblLinQ = ''
            tblLinQ = f'with lids as (select distinct {tToQuery} from {storedTable}) select {attr} from (select {attr}, rowid as rwid from {oTBL}) o join lids on o.rwid = lids.{tToQuery};\n'
            ff.write(f"select 'querying lineage data for {tToQuery}';\n")
            ff.write(f'explain analyze \n')
            ff.write('  ' + tblLinQ)
            ff.write('\n')
def make_executable_smd_p5(infile, outfile, storedTable, tablesToQuery: list, originalTbl: list, tAttributes: list, storedTBLNames:list, hasConditions: list = None, conditions: str = None):

    with open(f'{outfile}', 'w') as ff:
        ff.write("SELECT 'start to store each lineage table';\n")
        ff.write('.timer on \n')
        ff.write(f'set threads to 1;\n')
        for id in range(len(tablesToQuery)):
            tToQuery = tablesToQuery[id]
            oTBL =  originalTbl[id]
            attr = tAttributes[id]
            sTBL = storedTBLNames[id]
            tblLinQ = ''
            if hasConditions is not None and hasConditions[id] and conditions is not None:
                tblLinQ = f'with lids as (select distinct {tToQuery} from {storedTable} where {conditions}) select {attr} from (select {attr}, rowid as rwid from {oTBL}) o join lids on o.rowid = lids.{tToQuery};\n'
            else:
                tblLinQ = f'with lids as (select distinct {tToQuery} from {storedTable}) select {attr} from (select {attr}, rowid as rwid from {oTBL}) o join lids on o.rwid = lids.{tToQuery};\n'
            ff.write(f"select 'Stored lineage data for {tToQuery}';\n")
            ff.write(f"drop table if exists {sTBL};\n")
            ff.write(f'explain analyze create table {sTBL} as \n')
            ff.write('  ' + tblLinQ)
            ff.write('\n')
            ff.write(f'select \'{sTBL}\' as table_name, count(DISTINCT block_id) AS num_blocks, count(distinct block_id) * (SELECT block_size FROM pragma_database_size()) AS total_bytes, format_bytes(count(DISTINCT block_id) * (SELECT block_size FROM pragma_database_size())) AS total_size FROM pragma_storage_info(\'{sTBL}\') WHERE block_id IS NOT NULL;\n')
def make_executable_smd_p6(infile, outfile, rpdquery: str):
    with open(f'{outfile}', 'w') as ff:
        ff.write(f'set threads to 1;\n')
        ff.write("SELECT 'start to query final rpd lineage query';\n")
        ff.write(f'explain analyze {rpdquery};\n')
def make_executable_smd_p6_qlist(infile, outfile, rpdquerylist: list):
    with open(f'{outfile}', 'w') as ff:
        ff.write(f'set threads to 1;\n')
        for q in rpdquerylist:
            ff.write("SELECT 'start to query final rpd lineage query';\n")
            ff.write(f'explain analyze {q};\n')
            ff.write('\n')

def make_executable_smd_plin(query, outfile):
    query = query.strip()
    if query[-1] == ';':
        query = query[:-1]

    with open(f'{outfile}', 'w') as ff:
        ff.write('.timer on \n')
        ff.write('set threads to 1;\n')
        ff.write('pragma enable_lineage;\n')
        ff.write(f'{query};\n')
        ff.write(f'pragma Provenance(\'polynomial\', "{query};");\n')
        ff.write('pragma disable_lineage;\n')


def make_executable_smd_rpdO(smdpath, dbpath, query, outfile, storedTable, tablesToQuery: list, originalTbl: list, rpdquery: str):
    if (len(tablesToQuery) != len(originalTbl)):
        LOG(f"Error: tables to query and original tables do not match in length!", True)
        exit()
    rmSMDLineageTables(smdpath, dbpath)
    linQ = duckdbGetLineageQuery(smdpath, dbpath, query + ';')
    linTBLs = duckdbGetAllLineageTables(smdpath, dbpath, query + ';')
    query = query.strip()
    if query[-1] == ';':
        query = query[:-1]
    if linQ[-1] == ';':
        linQ = linQ[:-1]
    with open(f'{outfile}', 'w') as ff:
        # for linTBL in linTBLs:
        #     ff.write(f'drop table if exists {linTBL};\n')
        ff.write('.timer on \n')
        ff.write('set threads to 1;\n')
        ff.write('pragma enable_lineage;\n')
        ff.write(f'{query};\n')
        ff.write('pragma disable_lineage;\n')
        ff.write('\n')
        ff.write(f"select 'start to query lineage id';\n")
        ff.write(f'explain analyze {linQ};\n')
        ff.write('\n')
        ff.write(f"select 'start to store lineage id in {storedTable}';\n")
        ff.write(f'drop table if exists {storedTable};\n')
        ff.write(f'explain analyze create table {storedTable} as {linQ};\n')
        ff.write('\n')
        ff.write(
            f"select 'start to query lineage data from {storedTable} by each table';\n")
        for id in range(len(tablesToQuery)):
            tToQuery = tablesToQuery[id]
            oTbl = originalTbl[id]
            tblLinQ = f'with lids as (select distinct {tToQuery} from {storedTable}) select * from (select *, rowid as rn from {oTbl}) o join lids on o.rn = lids.{tToQuery};\n'
            ff.write(f"select 'querying lineage data for {tToQuery}';\n")
            ff.write(f'explain analyze \n')
            ff.write('  ' + tblLinQ)
            ff.write('\n')
            ff.write(f"select 'Stored lineage data for {tToQuery}';\n")
            ff.write(f"drop table if exists {tToQuery}_lineage;\n")
            ff.write(f'create table {tToQuery}_lineage as \n')
            ff.write(f'  ' + tblLinQ)
            ff.write('\n')
        ff.write('\n')
        ff.write("SELECT 'start to query final rpd lineage query';\n")
        ff.write(f'explain analyze {rpdquery};\n')


# set max_parallel_workers_per_gather = 0

def make_executable_sqlprov_rpd_p3(infile, outfile, storedTable):
    sql = ''
    with open(f'{infile}', 'r') as f:
        sql = f.read()
    sql = sql.replace(';', '')

    with open(f'{outfile}', 'w') as ff:
        ff.write(f"select 'start to store lineage id in {storedTable}';\n")
        ff.write(f'drop table if exists {storedTable};\n')
        ff.write(f'explain analyze create table {storedTable} as {sql};\n')
        ff.write(f'analyze {storedTable};\n')
        ff.write(f'select \'{storedTable}\' as table_name, pg_relation_size(\'{storedTable}\') AS size;\n')

def make_executable_sqlprov_rpd_p4(infile, outfile, storedTable, tablesToQuery: list, originalTbl: list, tAttributes: list, storedTBLNames:list):
    assert len(tablesToQuery) == len(originalTbl) and len(tablesToQuery) == len(tAttributes)
    with open(f'{outfile}', 'w') as ff:
        ff.write(f"select 'start to query lineage data from {storedTable} by each table';\n")
        for id in range(len(tablesToQuery)):
            tToQuery = tablesToQuery[id]
            oTBL =  originalTbl[id]
            attr = tAttributes[id]
            tblLinQ = ''
            tblLinQ = f'with lids as (select distinct {tToQuery} from {storedTable}) select {attr} from (select {attr} from {oTBL}_1) o join lids on o.tuid = lids.{tToQuery};\n'
            ff.write(f"select 'querying lineage data for {tToQuery}';\n")
            ff.write(f'explain analyze \n')
            ff.write('  ' + tblLinQ)
            ff.write('\n')
def make_executable_sqlprov_rpd_p5(infile, outfile, storedTable, tablesToQuery: list, originalTbl: list, tAttributes: list, storedTBLNames:list, hasConditions:list = None, conditions:str = None):
    if not ( len(tablesToQuery) == len(originalTbl) and len(tablesToQuery) == len(tAttributes) and (len(storedTBLNames) == len(tablesToQuery))):
        LOG(f"Error: tables to query, original tables, attributes and stored table names do not match in length!", True)
        print(f'len tables to query: {len(tablesToQuery)}, len original tables: {len(originalTbl)}, len attributes: {len(tAttributes)}, len stored table names: {len(storedTBLNames)}')
        exit()


    with open(f'{outfile}', 'w') as ff:
        ff.write("SELECT 'start to store each table prov data';\n")
        for id in range(len(tablesToQuery)):
            tToQuery = tablesToQuery[id]
            oTBL =  originalTbl[id]
            attr = tAttributes[id]
            tblLinQ = ''
            if hasConditions is not None and hasConditions[id]:
                condition = conditions[id]
                tblLinQ = f'with lids as (select distinct {tToQuery} from {storedTable}) select {attr} from (select {attr} from {oTBL}_1) o join lids on o.tuid = lids.{tToQuery} where {condition};\n'
            else:
                tblLinQ = f'with lids as (select distinct {tToQuery} from {storedTable}) select {attr} from (select {attr} from {oTBL}_1) o join lids on o.tuid = lids.{tToQuery};\n'
            storedTBLName = storedTBLNames[id]
            ff.write(f"select 'Stored lineage data for {tToQuery}';\n")
            ff.write(f"drop table if exists {storedTBLName};\n")
            ff.write(f'create table {storedTBLName} as \n')
            ff.write('  ' + tblLinQ)
            ff.write('\n')
            ff.write(f"analyze {storedTBLName};\n")
            ff.write(f'select \'{storedTBLName}\' as table_name, pg_relation_size(\'{storedTBLName}\') AS size;\n')

def make_executable_sqlprov_rpd_p6(infile, outfile, rpdquery: str):
    sql = ''
    with open(f'{infile}', 'r') as f:
        sql = f.read()
    sql = sql.replace(';', '')

    with open(f'{outfile}', 'w') as ff:
        ff.write("SELECT 'start to query final rpd lineage query';\n")
        ff.write(f'explain analyze {rpdquery};\n')

def make_executable_sqlprov_rpd_p6_qLst(infile, outfile, rpdquery: list):
    sql = ''
    with open(f'{infile}', 'r') as f:
        sql = f.read()
    sql = sql.replace(';', '')

    with open(f'{outfile}', 'w') as ff:
        ff.write("SELECT 'start to query final rpd lineage query';\n")
        for rpdq in rpdquery:
            ff.write(f'select \'RPD query: {rpdq}\' as rpd_query;\n')
            ff.write(f'explain analyze {rpdq};\n')

def make_executable_gprom_rpd_dt(infile, outfile, rpdQ, storedTable, isDuckDBBackend=False, isRPDList = False):
    sql = ''
    with open(f'{infile}', 'r') as f:
        sql = f.read()
    sql = sql.replace(';', '')

    with open(f'{outfile}', 'w') as ff:
        if isDuckDBBackend:
            ff.write('.timer on \n')
            ff.write('set threads to 1;\n')

        ff.write(f"select 'start to query data for sqlprov';\n")
        ff.write(f'explain analyze {sql};\n')
        ff.write('\n')

        ff.write(f"select 'start to materialized data for gprom';\n")
        ff.write(f'drop table if exists {storedTable};\n')
        ff.write(f'explain analyze create table {storedTable} as {sql};\n')
        ff.write('\n')

        ff.write(f"select 'start to query size of materialized data for gprom';\n")
        if isDuckDBBackend:
            ff.write(f'select count(*) from {storedTable} as rowcnt_{storedTable};\n')
            ff.write(f'SELECT \'{storedTable}\' AS table_name, count(DISTINCT block_id) AS num_blocks, format_bytes(count(DISTINCT block_id) * (SELECT block_size FROM pragma_database_size())) AS total_size FROM pragma_storage_info(\'{storedTable}\') WHERE block_id IS NOT NULL;\n')
        else:
            ff.write(f"analyze {storedTable};\n")
            ff.write(f'select count(*) from {storedTable} as rowcnt_{storedTable};\n')
            ff.write(f'select \'{storedTable}\' as tblname, pg_relation_size(\'{storedTable}\') AS size;\n')
        ff.write('\n')


        ff.write("SELECT 'start to query final rpd lineage query';\n")
        if isRPDList:
            for rpdq in rpdQ:
                ff.write(f'select \'RPD query: {rpdq}\' as rpd_query;\n')
                ff.write(f'explain analyze with lineages as ({sql}) {rpdq};\n')
        else:
            ff.write(f'explain analyze with lineages as ({sql}) {rpdQ};\n')


def make_executable_gprom_rpd_id(infile, outfile, storedTable, tableToQuery:list, originalTbl:list, idss:list, storedTBLNames: list, rpdQ, WHERECOND:str = None, isDuckDBBackend=False):
    sql = ''
    with open(f'{infile}', 'r') as f:
        sql = f.read()
    sql = sql.replace(';', '')

    with open(f'{outfile}', 'w') as ff:
        if isDuckDBBackend:
            ff.write('.timer on \n')
            ff.write('set threads to 1;\n')

        ff.write(f"select 'start to query id for sqlprov';\n")
        ff.write(f'explain analyze {sql};\n')
        ff.write('\n')

        ff.write(f"select 'start to store lineage id in {storedTable}';\n")
        ff.write(f'drop table if exists {storedTable};\n')
        if WHERECOND is not None:
            ff.write(f'explain analyze create table {storedTable} as {sql} where {WHERECOND};\n')
            ff.write(f'analyze {storedTable};\n')
        else:
            ff.write(f'explain analyze create table {storedTable} as {sql};\n')
            ff.write(f'analyze {storedTable};\n')

        if isDuckDBBackend:
            ff.write(f'SELECT \'{storedTable}\' AS table_name, count(DISTINCT block_id) AS num_blocks, format_bytes(count(DISTINCT block_id) * (SELECT block_size FROM pragma_database_size())) AS total_size FROM pragma_storage_info(\'{storedTable}\') WHERE block_id IS NOT NULL;\n')
        else:
            ff.write(f'select \'{storedTable}\' as table_name, pg_relation_size(\'{storedTable}\') AS size;\n')
        ff.write('\n')
        ff.write(f"select 'start to query row number of {storedTable}';\n")
        ff.write(f'select count(*) from {storedTable} as rowcnt_{storedTable};\n')
        ff.write('\n')

        ff.write(f"select 'start to query lineage data from {storedTable} by each table';\n")
        for id in range(len(tableToQuery)):
            tToQuery = tableToQuery[id]
            oTBL =  originalTbl[id]
            thisId = idss[id]
            tblLinQ = f'with lids as (select distinct {tToQuery} from {storedTable}) select * from (select * from {oTBL}) o join lids on o.{thisId}= lids.{tToQuery};\n'
            ff.write(f"select 'querying lineage data for {tToQuery}';\n")
            ff.write(f'explain analyze \n')
            ff.write('  ' + tblLinQ)
            ff.write('\n')
            ff.write(f"select 'Stored lineage data for {tToQuery}';\n")
            storedTBLN = storedTBLNames[id]
            ff.write(f"drop table if exists {storedTBLN};\n")
            ff.write(f'create table {storedTBLN} as \n')
            ff.write(f'  ' + tblLinQ)
            ff.write(f'\n')
            ff.write(f"analyze {storedTBLN};\n")
            if isDuckDBBackend:
                ff.write(f'SELECT \'{storedTBLN}\' AS table_name, count(DISTINCT block_id) AS num_blocks, format_bytes(count(DISTINCT block_id) * (SELECT block_size FROM pragma_database_size())) AS total_size FROM pragma_storage_info(\'{storedTBLN}\') WHERE block_id IS NOT NULL;\n')
            else:
                ff.write(f'select \'{storedTBLN}\' as table_name, pg_relation_size(\'{storedTBLN}\') AS size;\n')
            ff.write('\n')
            ff.write(f"select 'start to query row number of {storedTBLN}';\n")
            ff.write(f'select count(*) from {storedTBLN} as rowcnt_{storedTBLN};\n')
            ff.write('\n')

        ff.write("SELECT 'start to query final rpd lineage query';\n")
        ff.write(f'explain analyze {rpdQ};\n')

def make_executable_provsql_rpd_p2(infile, outfile):
    sql = ''
    with open(f'{infile}', 'r') as f:
        sql = f.read()
    sql = sql.replace(';', '')

    with open(f'{outfile}', 'w') as ff:
        ff.write(f"select 'start to query id for provsql';\n")
        ff.write(f'explain analyze {sql};\n')
        ff.write('\n')

def make_executable_provsql_rpd_p3(infile, outfile, storedTable):
    sql = ''
    with open(f'{infile}', 'r') as f:
        sql = f.read()
    sql = sql.replace(';', '')

    with open(f'{outfile}', 'w') as ff:
        ff.write(f"select 'start to store lineage id in {storedTable}';\n")
        ff.write(f'drop table if exists {storedTable};\n')
        ff.write(f'set max_parallel_workers_per_gather = 0;\n')
        ff.write(f'explain analyze create table {storedTable} as {sql};\n')
        ff.write(f'analyze {storedTable};\n')
        ff.write(f'select \'{storedTable}\' as table_name, pg_relation_size(\'{storedTable}\') AS size;\n')

def make_executable_provsql_rpd_p4(infile, outfile, storedTable, tablesToQuery: list, originalTbl: list, idss:list):
    with open(f'{outfile}', 'w') as ff:
        for id in range(len(tablesToQuery)):
            tToQuery = tablesToQuery[id]
            oTBL =  originalTbl[id]
            thisId = idss[id]
            tblLinQ = f'with lids as (select distinct {tToQuery} from {storedTable}) select * from (select * from {oTBL}) o join lids on o.{thisId} = lids.{tToQuery};\n'
            ff.write(f"select 'querying lineage data for {tToQuery}';\n")
            ff.write(f'explain analyze \n')
            ff.write('  ' + tblLinQ)
            ff.write('\n')

def make_executable_provsql_rpd_p5(infile, outfile, storedTable, tablesToQuery: list, originalTbl: list, idss:list, storedTBLNames:list, hasCondList:list = None, WHERECOND:list = None):
    with open(f'{outfile}', 'w') as ff:
        for id in range(len(tablesToQuery)):
            tToQuery = tablesToQuery[id]
            oTBL =  originalTbl[id]
            thisId = idss[id]
            storedTBLN = storedTBLNames[id]
            if hasCondList is not None and hasCondList[id] and WHERECOND is not None:
                condition = WHERECOND[id]
                tblLinQ = f'with lids as (select distinct {tToQuery} from {storedTable}) select * from (select * from {oTBL}) o join lids on o.{thisId} = lids.{tToQuery} where {condition};\n'
            else:
                tblLinQ = f'with lids as (select distinct {tToQuery} from {storedTable}) select * from (select * from {oTBL}) o join lids on o.{thisId} = lids.{tToQuery};\n'
            ff.write(f"select 'querying lineage data for {tToQuery}';\n")
            ff.write(f'explain analyze create table {storedTBLN} as \n')
            ff.write('  ' + tblLinQ)
            ff.write('\n')

def make_executable_provsql_rpd_p6(outfile, rpdQ, isRPDLIST=False):
    with open(f'{outfile}', 'w') as ff:
        ff.write(f"SELECT 'start to query final rpd lineage query';\n")
        if isRPDLIST:
            for rQ in rpdQ:
                ff.write(f'select \'RPD query: {rQ}\' as rpd_query;\n')
                ff.write(f'explain analyze {rQ};\n')
        else:
            ff.write(f'explain analyze {rpdQ};\n')

def make_executable_gprom_rpd_p1(infile, outfile, isDuckDBBackend=False):
    sql = ''
    with open(f'{infile}', 'r') as f:
        sql = f.read()
    sql = sql.replace(';', '')

    with open(f'{outfile}', 'w') as ff:
        if isDuckDBBackend:
            ff.write('.timer on \n')
            ff.write('set threads to 1;\n')
            ff.write(f'explain analyze {sql};\n')
        else:
            ff.write(f'explain analyze {sql};\n')

def make_executable_gprom_rpd_p2(infile, outfile, tablesName: list,isDuckDBBackend=False):
    sql = ''
    with open(f'{infile}', 'r') as f:
        sql = f.read()
    sql = sql.replace(';', '')

    with open(f'{outfile}', 'w') as ff:
        if isDuckDBBackend:
            ff.write('.timer on \n')
            ff.write('set threads to 1;\n')
            for tbl in tablesName:
                ff.write(f'drop table if exists {tbl};\n')
                ff.write(f'create table {tbl} as {sql};\n')
        else:
            for tbl in tablesName:
                ff.write(f'drop table if exists {tbl};\n')
                ff.write(f'explain analyze create table {tbl} as {sql};\n')


def make_executable_gprom_rpd_p3(outfile, distinctwhats: list, fromtables: list, isDuckDBBackend=False):
    with open(f'{outfile}', 'w')  as ff:
        if isDuckDBBackend:
            ff.write('.timer on \n')
            ff.write('set threads to 1;\n')
        for id in range(len(distinctwhats)):
            distinctwhat = distinctwhats[id]
            fromtbl = fromtables[id]

            q = f'select distinct {distinctwhat} from {fromtbl};\n'
            ff.write(f"select 'querying distinct {distinctwhat} from {fromtbl}';\n")
            ff.write(f'explain analyze {q}\n')

def make_executable_gprom_rpd_p4(outfile, storedTables: list, distinctwhats: list, fromtables: list, isDuckDBBackend=False):
    with open(f'{outfile}', 'w')  as ff:
        if isDuckDBBackend:
            ff.write('.timer on \n')
            ff.write('set threads to 1;\n')
        for id in range(len(storedTables)):

            storedTable = storedTables[id]
            distinctwhat = distinctwhats[id]
            fromtbl = fromtables[id]

            q = f'select distinct {distinctwhat} from {fromtbl};\n'
            ff.write(f"select 'querying distinct {distinctwhat} from {fromtbl}';\n")
            ff.write(f'drop table if exists {storedTable};\n')
            ff.write(f'explain analyze create table {storedTable} as select distinct {distinctwhat} from {fromtbl};\n')

def make_executable_gprom_rpd_p5(outfile, q, isDuckDBBackend=False):
    with open(f'{outfile}', 'w')  as ff:
        if isDuckDBBackend:
            ff.write('.timer on \n')
            ff.write('set threads to 1;\n')
        ff.write(f"select 'querying final rpd query';\n")
        ff.write(f'explain analyze {q};\n')


# def make_executable_provsql_rpd( outfile, storedTable, tablesToQuery:list, originalTbl:list, idss:list, rpdQ):
#     with open(f'{outfile}', 'w') as ff:


#         for id in range(len(tablesToQuery)):
#             tToQuery = tablesToQuery[id]
#             oTBL =  originalTbl[id]
#             thisId = idss[id]
#             tblLinQ = f'with lids as (select distinct {tToQuery} from {storedTable}) select * from (select * from {oTBL}) o join lids on o.{thisId} = lids.{tToQuery};\n'
#             ff.write(f"select 'querying lineage data for {tToQuery}';\n")
#             ff.write(f'explain analyze \n')
#             ff.write('  ' + tblLinQ)
#             ff.write('\n')
#             ff.write(f"select 'Stored lineage data for {tToQuery}';\n")
#             ff.write(f"drop table if exists {oTBL}_lineage;\n")
#             ff.write(f'create table {oTBL}_lineage as \n')
#             ff.write(f'  ' + tblLinQ)
#             ff.write('\n')
#         ff.write(f"explain analyze {rpdQ};\n")
#         ff.write('\n')

# def make_executable_smd_p3(benchmark, oQuery, infile, outfile):
#     with open('systems.config', 'r') as f:
#         jsonFile = json.load(f)
#     smdPath = jsonFile["smokedduck"]["duckdb_bin"]
#     dbdataPath = jsonFile["smokedduck"]["database_path"]v
#     cmd = smdPath + ' ' + dbdataPath + ' '
#     rmSMDLineageTables(smdPath, dbdataPath)
#     query = ''
#     with open(f'{infile}', 'r') as f:
#         query = f.read()
#     res = subprocess.run(cmd, shell=True, input=query, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     rt = res.returncode
#     outs = ''
#     # print(query)
#     if rt != 0:
    #     print(f'Error running SmokedDuck to get executable sql: {res.stderr}')
    #     exit(1)
    # outs = res.stdout
    # # print(outs)
    # lines = outs.split('\n')
    # sql = ''
    # for line in lines:
    #     toProcessLine = line.strip()
    #     if len(toProcessLine) > 0 and 'query =' in toProcessLine:
    #         sql = toProcessLine.strip().split('=')[1].strip()

    # if sql == '':
    #     print('Error: cannot find executable sql from SmokedDuck output!')
    #     exit(1)

    # sqls = []
    # sqls.append(f'.timer on \n')
    # sqls.append('set threads to 1;\n')
    # sqls.append('pragma enable_lineage;\n')
    # sqls.append(f'{oQuery};\n')
    # sqls.append(f'{sql};\n')

    # for idx, tbl in enumerate(tblList):
    #     idAttr = idAttrList[idx]
    #     sqls.append(f', o{idx+1} as (select {idAttr}, rowid as rid{idx+1} from {tbl})')
    # sqls.append(' \n')

    # for idx, tbl in enumerate(tblList):
    #     idAttr = idAttrList[idx]
    #     if idx > 0:
    #         sqls.append(', union all')
    #     sqls.append(f'(select distinct {idAttr}, \'{tbl}\' as tbl from tmp join o{idx+1} on (tmp.{tbl} = o{idx+1}.rid{idx+1}))')
    # sqls.append(';\n')

    # with open(f'{outfile}', 'w') as ff:
    #     for sql in sqls:
    #         ff.write(sql)

def rmSMDLineageTables(smdPath, dbdataPath):
    QGetAllLineageTables = """
.mode line
select 'drop table if exists ' || table_name || ' cascade;' as ltbl
from information_schema.tables
where table_name like 'LINEAGE_%';
    """

    cmd = f'{smdPath} {dbdataPath} '
    fetchRes = subprocess.run(cmd, shell=True, input=QGetAllLineageTables,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    rt = fetchRes.returncode
    if rt != 0:
        LOG(f"Error fetching lineage tables {fetchRes.stderr}", True)
        return (rt, fetchRes.stderr)
    outLines = fetchRes.stdout.split('\n')
    for line in outLines:
        toProcessLine = line.strip()
        if len(toProcessLine) > 0 and 'drop table if exists' in toProcessLine:
            sql = toProcessLine.strip().split('=')[1].strip()
            dropRes = subprocess.run(cmd,
                                     shell=True,
                                     input=sql,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     text=True)
            dropRT = dropRes.returncode
            if dropRT != 0:
                LOG(f"Error dropping lineage table {sql} : {dropRes.stderr}", True)
                return (dropRT, dropRes.stderr)


def duckdbGetAllLineageTables(smdPath, dbdataPath, query):
    rmSMDLineageTables(smdPath, dbdataPath)
    QGetAllLineageTables = """
set threads to 1;
pragma enable_lineage;
{qquery}
.mode line
select table_name as tblname from information_schema.tables where table_name like 'LINEAGE_%';
pragma disable_lineage;
    """.format(qquery=query)
    print(QGetAllLineageTables)
    cmd = f'{smdPath} {dbdataPath} '
    fetchRes = subprocess.run(cmd, shell=True, input=QGetAllLineageTables,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    rt = fetchRes.returncode
    lineageTables = []
    if rt != 0:
        LOG(f"Error fetching lineage tables {fetchRes.stderr}", True)
        exit(rt)
    outLines = fetchRes.stdout.split('\n')
    for line in outLines:
        toProcessLine = line.strip()
        if len(toProcessLine) > 0 and 'LINEAGE_' in toProcessLine:
            aline = toProcessLine.split('=')[1].strip()
            lineageTables.append(aline)
    return lineageTables


def duckdbGetLineageQuery(smdPath, dbdataPath, query):
    rmSMDLineageTables(smdPath, dbdataPath)
    QGetLineeageQ = """
set threads to 1;
pragma enable_lineage;
{qquery}
.mode line
pragma ProvenanceString('lineage', "{qquery}");
pragma disable_lineage;
    """.format(qquery=query)

    cmd = f'{smdPath} {dbdataPath} '
    fetchRes = subprocess.run(cmd, shell=True, input=QGetLineeageQ,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    rt = fetchRes.returncode
    lineageQuery = ''
    if rt != 0:
        LOG(f"Error fetching lineage query {fetchRes.stderr}", True)
        exit(rt)
    outLines = fetchRes.stdout.split('\n')
    for line in outLines:
        toProcessLine = line.strip()
        if len(toProcessLine) > 0 and 'query =' in toProcessLine:
            index = toProcessLine.find('=')
            lineageQuery = toProcessLine.strip()[index + 1:].strip()
    return lineageQuery


def duckdbRun(smdPath, dbdataPath, query):
    cmd = f'{smdPath} {dbdataPath} '
    runRes = subprocess.run(cmd, shell=True, input=query,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    rt = runRes.returncode
    if rt != 0:
        LOG(f"Error running DuckDB query {runRes.stderr}", True)
        exit(rt)
