import os
import json

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

################################################################################
SYS_GProM = 'gprom'
SYS_ProvSQL = 'provsql'
SYS_SmokedDuck = 'smokedduck'
SYS_Links = 'links'
SYS_SQLProv = 'sqlprov'

SYS_PostgreSQL = 'postgresql'
SYS_DuckDB = 'duckdb'

SYS_Config='systems.config'
SYS_ConfigGeneral = 'systems.cfg'

READ = 'r'
WRITE= 'w'
APPEND = 'a'
QSTART = 'qstart'
QEND = 'qend'



SPECIFIED_DUCKDB_BIN = '/Users/uicdbgroup/pengyuan/duckdb/duckdb'
################################################################################

def createQFolder(whichBench, whichSys):
    os.makedirs(f'{ROOT}/{whichBench}/{whichSys}', exist_ok = True)

def readFileAsList(filename: str):
    readF = open(filename, READ)
    fileLines = readF.readlines()
    readF.close()
    return fileLines

def lodConfig(whichBench: str):
    jsonFile = loadJsonConfig(f'{ROOT}/utils/{SYS_ConfigGeneral}')
    dumpJsonConfig(f'{ROOT}/{whichBench}/{SYS_Config}', jsonFile)

def updateQCnts(whichBench, whichSys, qStart, qEnd):
    jsonFile = loadJsonConfig(f'{ROOT}/{whichBench}/{SYS_Config}')

    jsonFile["queries"][whichSys][QSTART] = qStart
    jsonFile["queries"][whichSys][QEND] = qEnd

    dumpJsonConfig(f'{ROOT}/{whichBench}/{SYS_Config}', jsonFile)

def readTemplate(filePath):
    sql = ''
    with open(filePath, 'r') as f:
        sql = f.read()
    return sql

def loadJsonConfig(jsonPath):
    with open(jsonPath, 'r') as f:
        jsonFile = json.load(f)
    return jsonFile

def dumpJsonConfig(jsonPath, jsonFile):
    with open(jsonPath, 'w') as f:
        json.dump(jsonFile, f, indent = 4)

def createFile(filePath, mode = 'w', metadata = None):
    with open(filePath, mode) as f:
        if metadata is not None:
            f.write(f'{metadata}\n')

def appendToFile(filePath, content):
    with open(filePath, 'a') as f:
        f.write(f'{content}\n')

def getQList(qstart, qend, querylist, jsonConfig, system):
    # --------------------------------------------------------------------------
    # Determine the query range
    # If nither qstart/qend nor querylist is not specified, load from systems.cfg
    # --------------------------------------------------------------------------
    queryToRun = []
    if (qstart == -1 or qend == -1) and (querylist is None):
        configs = jsonConfig
        qstart = configs["queries"][system][QSTART]
        qend = configs["queries"][system][QEND]
        for qidx in range(qstart, qend + 1):
            queryToRun.append(qidx)
    elif querylist is not None:
        querylistStr = querylist
        queryListStrs = querylistStr.strip().split(',')
        for qstr in queryListStrs:
            queryToRun.append(int(qstr.strip()))
    elif qstart != -1 and qend != -1 and querylist is None and qend >= qstart:
        for qidx in range(qstart, qend + 1):
            queryToRun.append(qidx)
    else:
        print('ERROR: please specify EITHER qstart/qend OR provide a querylist\n')
        print('  e.g., --qstart=1 --qend=5')
        print('  OR')
        print('  e.g., --querylist=\'1,3,5\'')
        print('  NOT BOTH\n')
        exit()
    print(f'Queries to run: {queryToRun}')
    return queryToRun

################################################################################
# SQLProv pre.sql templates
################################################################################

logJoin = """
drop table if exists logJoin cascade;
create table logJoin (location int not null,
                       tuid int not null,
                       tuids int[] not null);
alter table logJoin alter column tuid set default nextval('tuids_seq');
alter table logJoin add primary key (location, tuid); -- Q: drop column location?
alter table logJoin add constraint logjoin_location_tuids_key unique (location, tuids);
"""

logAggs = """
drop table if exists logAggregation cascade;
create table logAggregation (location int not null,
                         tuids int[] not null,
                         tuid int not null);
alter table logAggregation alter column tuid set default nextval('tuids_seq');
alter table logAggregation add primary key (location, tuid);
create unique index logAggregation_location_tuids_key on logAggregation (location, (md5(tuids)));
"""

logFilters = """
drop table if exists logFilter cascade;
create table logFilter (location int not null,
                        tuid int not null);
alter table logFilter add primary key (location, tuid);
"""

logOrderBy = """
drop table if exists logOrderBy cascade;
create table logOrderBy (location int not null,
                         tuid int not null,
                         sequence serial not null);
alter table logOrderBy add primary key (location, tuid);
"""

logTblf = """
drop table if exists logTblf cascade;
create table logTblf (location  int not null,
                      tuid      int not null);
alter table logTblf alter column tuid set default nextval('tuids_seq');
alter table logTblf add primary key (location, tuid);
"""

logLogs = """
DROP TABLE IF EXISTS log0 CASCADE;
CREATE TABLE log0 (location loc_t NOT NULL,
                   tuidout tuid_t NOT NULL);
ALTER TABLE log0 ADD PRIMARY KEY (location);
ALTER TABLE log0 ALTER COLUMN tuidout SET DEFAULT NEXTVAL('tuid_seq');

DROP TABLE IF EXISTS log1 CASCADE;
CREATE TABLE log1 (location loc_t NOT NULL,
                   tuidout tuid_t NOT NULL,
                   tuid1 tuid_t NOT NULL);
ALTER TABLE log1 ADD PRIMARY KEY (location, tuid1);
ALTER TABLE log1 ALTER COLUMN tuidout SET DEFAULT NEXTVAL('tuid_seq');

DROP TABLE IF EXISTS log2 CASCADE;
CREATE TABLE log2 (location loc_t NOT NULL,
                   tuidout tuid_t NOT NULL,
                   tuid1 tuid_t NOT NULL,
                   tuid2 tuid_t NOT NULL);
ALTER TABLE log2 ADD PRIMARY KEY (location, tuid1, tuid2);
ALTER TABLE log2 ALTER COLUMN tuidout SET DEFAULT NEXTVAL('tuid_seq');

DROP TABLE IF EXISTS log3 CASCADE;
CREATE TABLE log3 (location loc_t NOT NULL,
                   tuidout tuid_t NOT NULL,
                   tuid1 tuid_t NOT NULL,
                   tuid2 tuid_t NOT NULL,
                   tuid3 tuid_t NOT NULL);
ALTER TABLE log3 ADD PRIMARY KEY (location, tuid1, tuid2, tuid3);
ALTER TABLE log3 ALTER COLUMN tuidout SET DEFAULT NEXTVAL('tuid_seq');

DROP TABLE IF EXISTS log4 CASCADE;
CREATE TABLE log4 (location loc_t NOT NULL,
                   tuidout tuid_t NOT NULL,
                   tuid1 tuid_t NOT NULL,
                   tuid2 tuid_t NOT NULL,
                   tuid3 tuid_t NOT NULL,
                   tuid4 tuid_t NOT NULL);
ALTER TABLE log4 ADD PRIMARY KEY (location, tuid1, tuid2, tuid3, tuid4);
ALTER TABLE log4 ALTER COLUMN tuidout SET DEFAULT NEXTVAL('tuid_seq');

"""



def SQLProvPreFile(whichBench):
    with open(f'{ROOT}/{whichBench}/sqlprov/pre.sql', 'w') as f:
        f.write(f'{logJoin}\n')
        f.write(f'{logAggs}\n')
        f.write(f'{logFilters}\n')
        f.write(f'{logOrderBy}\n')
        f.write(f'{logTblf}\n')
        f.write(f'{logLogs}\n')
        f.write(f'alter sequence tuids_seq restart with 1;\n')

def SQLProvLogSizeFile(whichBench, logwhat:list):
    with open(f'{ROOT}/{whichBench}/sqlprov/logSize.sql', 'w') as f:
        for log in logwhat:
            f.write(f'select pg_relation_size(\'{log}\') as {log}_size;\n')

def ProvSQLExt(whichBench, cfg):
    db = cfg['db']
    with open(f'{ROOT}/{whichBench}/provsql/createExt.sql', 'w') as f:
        f.write(f'create extension if not exists provsql cascade;\n')
        f.write(f'alter database {db} set search_path to public, provsql;\n')

    with open(f'{ROOT}/{whichBench}/provsql/dropExt.sql', 'w') as f:
        f.write(f'drop extension if exists provsql cascade;\n')