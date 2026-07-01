import os
import json
from pathlib import Path
import subprocess
import sys

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
        print(f"Error fetching lineage tables {fetchRes.stderr}", True)
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
                print(f"Error dropping lineage table {sql} : {dropRes.stderr}", True)
                return (dropRT, dropRes.stderr)


print("Cleaning DuckDB Lineage Tables for " + sys.argv[1] + ' on DB: ' + sys.argv[2])
rmSMDLineageTables(sys.argv[1], sys.argv[2])
