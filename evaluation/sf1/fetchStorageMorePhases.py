import os
import statistics as sta
import re
import json


def resStructures():
    res = {}
    res["gprom"] = {
        "p": {
            "storage": [],
        },
        "d": {
            "storage": [],
        }
    }
    res["smokedduck"] = {
        "p0": [],
        "p3": [],
        "p5": []
    }
    res["sqlprov"] = {
        "p0": [],
        "p3": [],
        "p5": []
    }

    res["provsql"] = {
        "p0": [],
        "p3": [],
        "p5": []
    }

    res["links"] = {
        "storage": []
    }

    return res


RMTOP = 3


def getSPLog(infile):
    with open(infile, 'r') as fff:
        text = fff.read()
    numbers = re.findall(r'^\s*(\d+)\s*$', text, re.MULTILINE)
    totalBytes = sum(float(num) for num in numbers)
    return totalBytes
def getSPTSize(infile):
    files = open(infile, 'r')
    lines = files.readlines()
    files.close()
    totalSize = 0
    for index, line in enumerate(lines):
        if len(line.strip()) > 0 and 'table_name' in line:
            targetLine = lines[index + 2]
            cells = targetLine.split('|')
            totalSize += float(cells[1].strip())
    return totalSize
def getProvsqlLog(infile, phase):
    # before
    ffff = open(infile, 'r')
    lines = ffff.readlines()
    ffff.close()
    beforeSize = 0.0
    afterSize = 0.0

    if phase == 'p1':
        lineIdx = 0
        for line in lines:
            if '########## DBSIZE BEFORE 0:' in line:
                beforeSize = float(lines[lineIdx + 3].strip())
                print(f"BEFORE: {beforeSize}")
            if '########## DBSIZE AFTER 5:' in line:
                afterSize = float(lines[lineIdx + 3].strip())
                print(f"after: {afterSize}\n\n")
            lineIdx += 1
    if phase == 'p5':
        lineIdx = 0
        for line in lines:
            if '########## DBSIZE BEFORE 0:' in line:
                beforeSize = float(lines[lineIdx + 3].strip())
                print(f"BEFORE: {beforeSize}")
            if '########## DBSIZE AFTER 0:' in line:
                afterSize = float(lines[lineIdx + 3].strip())
                print(f"after: {afterSize}\n\n")
            lineIdx += 1



    return afterSize - beforeSize

def getSMD(infile):
    fff = open(infile, 'r')
    lines = fff.readlines()
    fff.close()

    totalBytes = 0.0
    for idx, line in enumerate(lines):
        aline = line.strip()
        if 'total_bytes' in aline:
            # storage = aline.split('=')[1].strip()
            acturalLine = lines[idx + 3].strip()
            storage = acturalLine.split('│')[3].strip()
            totalBytes += float(storage)
    return totalBytes

def getSMDLog(infile):
    fff = open(infile, 'r')
    lines = fff.readlines()
    fff.close()
    lineIdx = 0
    totalBytes = 0.0
    for line in lines:
        if 'total_bytes' in line:
            dtLine = lines[lineIdx + 3].strip().split('│')
            totalBytes += float(dtLine[3].strip())
        lineIdx += 1
    return totalBytes
def getSMDLogRmDuplicateTBLNane(infile):
    tname = []

    fff = open(infile, 'r')
    lines = fff.readlines()
    fff.close()
    lineIdx = 0
    totalBytes = 0.0

    for line in lines:
        if 'total_size' in line:
            dtLine = lines[lineIdx + 3].strip().split('│')
            tblName = dtLine[1].strip()
            if tblName not in tname:
                size = float(dtLine[3].strip().split(' ')[0])
                print(size)
                totalBytes += size
                tname.append(tblName)
        lineIdx += 1
    return totalBytes

def getData(sf, bench, syss: list, qstart, qend, qlist: {} = None):
    data = resStructures()

    for syst in syss:
        if syst == 'smokedduck':
            QLIst = qlist['smokedduck'] if qlist and 'smokedduck' in qlist else range(qstart, qend + 1)
            for qid in QLIst:
                p0 = getSMDLog(f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_import_res.txt')
                p3 = getSMDLogRmDuplicateTBLNane(f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_p3_res.txt')
                p5 = getSMDLogRmDuplicateTBLNane(f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_p5_res.txt')
                data[syst]["p0"].append(float(p0 / (1024 * 1024)))
                data[syst]["p3"].append(float(p3))
                data[syst]["p5"].append(float(p5))
        elif syst == 'sqlprov':
            QList = qlist['sqlprov'] if qlist and 'sqlprov' in qlist else range(qstart, qend + 1)
            for qid in QList:
                p0 = getSPLog(f'{os.getcwd()}/newRes/{bench}/results/logSize_q{qid}.txt')
                data[syst]["p0"].append(float(p0 / (1024 * 1024)))
                p3 = getSPTSize(f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{qid}_p3_res.txt')
                data[syst]["p3"].append(float(p3 / (1024 * 1024)))
                p5 = getSPTSize(f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{qid}_p5_res.txt')
                data[syst]["p5"].append(float(p5 / (1024 * 1024)))
        elif syst == 'provsql':
            QList = qlist['provsql'] if qlist and 'provsql' in qlist else range(qstart, qend + 1)
            for qid in QList:
                p0= getProvsqlLog(f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{qid}_p1_res.txt', 'p1')
                data[syst]["p0"].append(float(p0 / (1024 * 1024))/6)
                p3 = getSPTSize(f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{qid}_p3_res.txt')
                data[syst]["p3"].append(float(p3 / (1024 * 1024)))
                p5 = getProvsqlLog(f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{qid}_p5_res.txt', 'p5')
                data[syst]["p5"].append(float(p5 / (1024 * 1024)))
    for syst in syss:
        print(f"processing {sf}.....")
        if syst == 'gprom':
            print(f"gprom: {data[syst]}")
        elif syst == 'smokedduck':
            print(f"smokedduck: {data[syst]}")
        elif syst == 'sqlprov':
            print(f"sqlprov: {data[syst]}")
        elif syst == 'provsql':
            print(f"provsql: {data[syst]}")

    with open(f'{os.getcwd()}/zackups/{sf}/{bench}STORAGE.json', 'w') as fff:
        json.dump(data, fff, indent=4)
def getDataFD2_3(sf, bench, syss: list, qstart, qend, qlist: {} = None):
    data = resStructures()

    for syst in syss:
        if syst == 'smokedduck':
            QLIst = qlist['smokedduck'] if qlist and 'smokedduck' in qlist else range(qstart, qend + 1)
            for qid in QLIst:
                p0 = getSMDLog(f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_import_res.txt')
                p3 = getSMDLogRmDuplicateTBLNane(f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_p3_res.txt')
                p5 = getSMDLogRmDuplicateTBLNane(f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_p5_res.txt')
                data[syst]["p0"].append(float(p0 / (1024 * 1024)))
                data[syst]["p3"].append(float(p3))
                data[syst]["p5"].append(float(p5))
        elif syst == 'sqlprov':
            QList = qlist['sqlprov'] if qlist and 'sqlprov' in qlist else range(qstart, qend + 1)
            for qid in QList:
                p0 = getSPLog(f'{os.getcwd()}/newRes/{bench}/results/logSize_q{qid}.txt')
                data[syst]["p0"].append(float(p0 / (1024 * 1024)))
                p3 = getSPTSize(f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{qid}_p3_res.txt')
                data[syst]["p3"].append(float(p3 / (1024 * 1024)))
                p5 = getSPTSize(f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{qid}_p5_res.txt')
                data[syst]["p5"].append(float(p5 / (1024 * 1024)))
        elif syst == 'provsql':
            QList = qlist['provsql'] if qlist and 'provsql' in qlist else range(qstart, qend + 1)
            for qid in QList:
                p0= getProvsqlLog(f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{qid}_p1_res.txt', 'p1')
                data[syst]["p0"].append(float(p0 / (1024 * 1024))/6)
                p3 = getSPTSize(f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{qid}_p3_res.txt')
                data[syst]["p3"].append(float(p3 / (1024 * 1024)))
                p5 = getProvsqlLog(f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{qid}_p5_res.txt', 'p5')
                data[syst]["p5"].append(float(p5 / (1024 * 1024)))
    for syst in syss:
        print(f"processing {sf}.....")
        if syst == 'gprom':
            print(f"gprom: {data[syst]}")
        elif syst == 'smokedduck':
            print(f"smokedduck: {data[syst]}")
        elif syst == 'sqlprov':
            print(f"sqlprov: {data[syst]}")
        elif syst == 'provsql':
            print(f"provsql: {data[syst]}")

    with open(f'{os.getcwd()}/zackups/{sf}/{bench}STORAGE.json', 'w') as fff:
        json.dump(data, fff, indent=4)
if __name__ == "__main__":
    os.makedirs(f'{os.getcwd()}/zackups/sf1', exist_ok=True)
    benchs = {
        'PMBD': {
            "sys": ['gprom', 'sqlprov', 'provsql', 'smokedduck'],
            "qrange": [1, 5]
        },
        "PMFD":{
            "sys": ['gprom', 'sqlprov', 'provsql', 'smokedduck'],
            "qrange": [1, 3]
        },
        'PMRLIN2': {
            "sys": ['gprom', 'sqlprov', 'provsql', 'smokedduck'],
            "qrange": [1, 4]
        },
        "PMFD2":{
            "sys": ['gprom', 'sqlprov', 'provsql'],
            "qrange": [1, 1]
        },
        "PMFD3":{
            "sys": ['gprom', 'sqlprov', 'provsql'],
            "qrange": [1, 1]
        },
    }

    sf = 'sf1'
    for bench in benchs:
        if bench not in ['PMFD2', 'PMFD3']:
            sysss = benchs[bench]["sys"]
            qrange = benchs[bench]["qrange"]
            print(bench)
            print(sysss)
            print(qrange)
            getData(sf, bench, sysss, qrange[0], qrange[1], qlist=None)
        else:
            sysss = benchs[bench]["sys"]
            qrange = benchs[bench]["qrange"]
            print(bench)
            print(sysss)
            print(qrange)
            getDataFD2_3(sf, bench, sysss, qrange[0], qrange[1], qlist=None)

