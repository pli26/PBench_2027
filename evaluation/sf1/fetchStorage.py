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
        "storage": []
    }
    res["sqlprov"] = {
        "storage": []
    }

    res["provsql"] = {
        "storage": []
    }

    res["links"] = {
        "storage": []
    }

    return res


RMTOP = 3


def getDuckdbA(infile, remotTop=RMTOP):
    fff = open(infile, 'r')
    lines = fff.readlines()
    fff.close()

    times = []
    for line in lines:
        if len(line) > len('Total Time:') and 'Total Time:' in line:
            match = re.search(r'Total Time:\s*([\d.]+)s', line)
            if match:
                timeValue = match.group(1)
            else:
                print(f"Unexpected time format in line: {line}")
                exit()
            time = float(timeValue)
            times.append(float(timeValue))
    if len(times) == 0:
        print(
            f"Warning: No valid execution times found in file {infile}. Returning (0.0, 0.0).")
        return (0.0, 0.0)
    times = times[remotTop:]
    if len(times) == 0:
        print(
            f"Warning: No valid execution times left after removing the first {remotTop} entries in file {infile}. Returning (0.0, 0.0).")
        return (0.0, 0.0)
    median = sta.median(times)
    variance = sta.variance(times)
    return (median, variance)


def getDuckdbB(infile, remotTop=RMTOP):
    fff = open(infile, 'r')
    lines = fff.readlines()
    fff.close()

    times = []
    tmpLines = []
    for line in lines:
        if len(line) > len('Run Time (s) ') and 'Run Time (s)' in line:
            tmpLines.append(line.strip())
            # print(f"tmpLines: {tmpLines}")
        if len(line) > len('Total Time:') and 'Total Time:' in line:
            match = re.search(r'Total Time:\s*([\d.]+)s', line)
            if match:
                timeValue = match.group(1)
            else:
                print(f"Unexpected time format in line: {line}")
                exit()

            readTime = float(timeValue)
            userTime = 0.0
            sysTime = 0.0
            # print(f'len(tmpLines): {len(tmpLines)}')
            lastLine = tmpLines[-1]
            print(f"lastLine: {lastLine}")
            if lastLine.startswith('Run Time (s):'):
                print(f"lastLine: {lastLine}")
                cell = lastLine.split(':')[1].strip()
                # cell = cell.strip()
                cells = cell.split(' ')
                userTime = float(cells[3].strip())
                sysTime = float(cells[5].strip())
            print(
                f"total = {readTime + userTime + sysTime}, readTime: {readTime}, userTime: {userTime}, sysTime: {sysTime}")
            times.append(readTime + userTime + sysTime)
            tmpLines = []

    if len(times) == 0:
        print(
            f"Warning: No valid execution times found in file {infile}. Returning (0.0, 0.0).")
        return (0.0, 0.0)
    times = times[remotTop:]
    if len(times) == 0:
        print(
            f"Warning: No valid execution times left after removing the first {remotTop} entries in file {infile}. Returning (0.0, 0.0).")
        return (0.0, 0.0)
    median = sta.median(times)
    variance = sta.variance(times)
    return (median, variance)


def getPostgresql(infile, remotTop=RMTOP):
    fff = open(infile, 'r')
    lines = fff.readlines()
    fff.close()

    times = []
    for line in lines:
        if len(line) > len('Execution Time') and 'Execution Time' in line:
            timeValue = line.strip().split(':')[1].strip()
            if timeValue.endswith('ms'):
                timeValue = timeValue[:-2].strip()
            else:
                print(f"Unexpected time format: {timeValue}")
                exit()
            time = float(timeValue) / 1000
            times.append(float(timeValue) / 1000)
    if len(times) == 0:
        print(
            f"Warning: No valid execution times found in file {infile}. Returning (0.0, 0.0).")
        return (0.0, 0.0)
    times = times[remotTop:]
    if len(times) == 0:
        print(
            f"Warning: No valid execution times left after removing the first {remotTop} entries in file {infile}. Returning (0.0, 0.0).")
        return (0.0, 0.0)
    median = sta.median(times)
    variance = sta.variance(times)
    return (median, variance)


def getSQLProv(infile):
    with open(infile, 'r') as fff:
        text = fff.read()
    numbers = re.findall(r'^\s*(\d+)\s*$', text, re.MULTILINE)

    totalBytes = sum(float(num) for num in numbers)
    return totalBytes


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


def getProvsql(infile):
    # before
    ffff = open(infile, 'r')
    lines = ffff.readlines()
    ffff.close()
    beforeSize = 0.0
    afterSize = 0.0
    lineIdx = 0
    for line in lines:
        if "########## DBSIZE BEFORE 0:" in line:
            beforeSize = float(lines[lineIdx + 3])
        if "########## DBSIZE AFTER 5:" in line:
            afterSize = float(lines[lineIdx + 3])
        lineIdx += 1

    return afterSize - beforeSize


def getData(sf, bench, syss: list, qstart, qend, qlist: {} = None):
    data = resStructures()

    for syst in syss:
        if syst == 'smokedduck':
            QList = qlist['smokedduck'] if qlist and 'smokedduck' in qlist else range(qstart, qend + 1)
            for qid in QList:
                storage = getSMD(
                    f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_import_res.txt')
                sizeInMB = float(storage / (1024 * 1024))
                data[syst]["storage"].append(sizeInMB)
        elif syst == 'sqlprov':
            QList = qlist['sqlprov'] if qlist and 'sqlprov' in qlist else range(qstart, qend + 1)
            for qid in QList:
                storage = getSQLProv(
                    f'{os.getcwd()}/newRes/{bench}/results/logSize_q{qid}.txt')
                sizeInMB = float(storage / (1024 * 1024))
                data[syst]["storage"].append(sizeInMB)
        elif syst == 'provsql':
            QList = qlist['provsql'] if qlist and 'provsql' in qlist else range(qstart, qend + 1)
            for qid in QList:
                storage = getProvsql(
                    f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{qid}_res.txt')
                sizeInMB = float(storage / (1024 * 1024)) / 6

                data[syst]["storage"].append(sizeInMB)
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

def getDataTPCH(sf, bench, syss: list, qstart, qend, qlist: {} = None):
    data = resStructures()

    for syst in syss:
        if syst == 'smokedduck':
            QList = qlist['smokedduck'] if qlist and 'smokedduck' in qlist else range(qstart, qend + 1)
            for qid in QList:
                storage = getSMD(
                    f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_import_res.txt')
                sizeInMB = float(storage / (1024 * 1024))
                data[syst]["storage"].append(f'{qid}: {sizeInMB}')
        elif syst == 'sqlprov':
            QList = qlist['sqlprov'] if qlist and 'sqlprov' in qlist else range(qstart, qend + 1)
            for qid in QList:
                storage = getSQLProv(
                    f'{os.getcwd()}/newRes/{bench}/results/logSize_q{qid}.txt')
                sizeInMB = float(storage / (1024 * 1024))
                data[syst]["storage"].append(f'{qid}: {sizeInMB}')
        elif syst == 'provsql':
            QList = qlist['provsql'] if qlist and 'provsql' in qlist else range(qstart, qend + 1)
            for qid in QList:
                storage = getProvsql(
                    f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{qid}0_metaSizeAfter.txt')
                sizeInMB = float(storage / (1024 * 1024))
                data[syst]["storage"].append(f'{qid}: {sizeInMB}')
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
        'VPGN': {
            "qrange": [1, 3],
            "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql']
        },
        'VPGS': {
            "qrange": [1, 3],
            "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql']
        },
        'FPAgg': {
            "qrange": [1, 3],
            "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql']
        },
        'FPDist': {
            "qrange": [1, 3],
            "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql']
        },
        'FPSDist': {
            "qrange": [1, 18],
            "sys": ['gprom', 'sqlprov', 'provsql']
        },
        'VPJJ': {
            "qrange": [1, 1],
            "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql']
        },
        'VPJJJ': {
            "qrange": [1, 1],
            "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql']
        },
        'VPJC': {
            "qrange": [1, 3],
            "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql']
        },
        'VPJS': {
            "qrange": [1, 3],
            "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql']
        },
        'QTopK2': {
            "qrange": [1, 4],
            "sys": ['gprom', 'sqlprov', 'smokedduck']
        },
        'QMLAgg': {
            "qrange": [1, 2],
            "sys": ['gprom', 'sqlprov', 'smokedduck']
        },
        'QAggNum': {
            "qrange": [1, 2],
            "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql']
        },
        'FPSAgg': {
            "qrange": [1, 4],
            "sys": ['gprom', 'sqlprov', 'smokedduck']
        },
        'QCMPLDC': {
            "qrange": [1, 3],
            "sys": ['gprom', 'sqlprov', 'provsql', 'smokedduck']
        },
        'QRCRW': {
            "qrange": [1, 2],
            "sys": ['sqlprov']
        },
        'QWIN': {
            "qrange": [1, 3],
            "sys": ['sqlprov']
        },
        'PMPP':
            {
                "qrange": [1, 5],
                "sys": ['gprom', 'provsql', 'smokedduck']
        },
        'QARGMIN': {
                "qrange": [1, 2],
                "sys": ['gprom', 'sqlprov', 'smokedduck', 'postgresql', 'duckdb']
        },
        'QLIMIT' :{
                "qrange": [1, 3],
                "sys": ['gprom', 'provsql', 'sqlprov', 'smokedduck', 'postgresql', 'duckdb']

        },
        'QSET' :{
                "qrange": [1, 3],
                "sys": ['gprom', 'smokedduck', 'provsql', 'duckdb']
        } ,
        'QWHRSUB' :{
                "qrange": [1, 3],
                "sys": ['sqlprov', 'smokedduck', 'smokedduck']
        }

    }

    sf = 'sf1'
    for bench in benchs:
        sysss = benchs[bench]["sys"]
        qrange = benchs[bench]["qrange"]
        print(bench)
        print(sysss)
        print(qrange)
        getData(sf, bench, sysss, qrange[0], qrange[1], qlist=None)
