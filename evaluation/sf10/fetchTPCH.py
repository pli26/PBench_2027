import os
import statistics as sta
import re
import json


def resStructures():
    res = {}
    res["gprom"] = {
        "p": {
            "times": [],
            "variances": [],
            "rescnt": []
        },
        "d": {
            "times": [],
            "variances": [],
            "rescnt": []
        }
    }
    res["smokedduck"] = {
        "1": {
            "times": [],
            "variances": []
        },
        "2": {
            "times": [],
            "variances": []
        }
    }
    res["sqlprov"] = {
        "1": {
            "times": [],
            "variances": [],
            "logsize": []
        },
        "2": {
            "times": [],
            "variances": []
        }
    }

    res["provsql"] = {
        "times": [],
        "variances": []
    }

    res["links"] = {
        "times": [],
        "variances": []
    }

    res["postgresql"] = {
        "times":[],
        "variances": []
    }

    res["duckdb"] = {
        "times":[],
        "variances":[]
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

def getDuckdbTimer(infile, removeUnecessary = 1, theNth = 3, remotTop=RMTOP):
    fff = open(infile, 'r')
    lines = fff.readlines()
    fff.close()

    times = []
    timess = []
    for line in lines:
        if len(line) > len('Run Time (s) ') and 'Run Time (s)' in line:
            aLines = line.strip().split(':')[1].strip().split(' ')
            timess.append(float(aLines[3].strip()) + float(aLines[5].strip()))
            print(f'PMPP: timer: {aLines}')
        if 'Disable Lineage Capture' in line:
            times.append(timess[-1])
    times = times[remotTop:]
    med = sta.median(times)
    var = sta.variance(times)
    return (med, var)


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

def getData(sf, bench, syss: list, qstart, qend, qlist: {} = None, isSPecialSMD = False, isGProMPostOnly = False, specificName = None):
    data = resStructures()
    gds = []
    gps = []

    sd1s = []
    sd2s = []

    sp1s = []
    sp2s = []

    prs = []
    posts = []
    ducks = []
    for syst in syss:
        if syst == 'gprom':
            QList = qlist[syst] if qlist and syst in qlist else range(
                qstart, qend + 1)
            for qid in QList:
                med = 0.0
                var = 0.0
                # (med, var) = getDuckdbA( f'{os.getcwd()}/{sf}/{bench}/results/gprom_capDq{qid}_res.txt')
                if isGProMPostOnly == False:
                    (med, var) = getDuckdbA( f'{os.getcwd()}/newRes/{bench}/results/gprom_capDq{qid}_res.txt')
                    data[syst]["d"]["times"].append(f'{qid}:{med}')
                    data[syst]["d"]["variances"].append(f'{qid}:{var}')
                    if qid in range(1, 23):
                        gds.append(med)
                    else:
                        gps.append('--')


                (med, var) = getPostgresql( f'{os.getcwd()}/newRes/{bench}/results/gprom_capPq{qid}_res.txt')
                data[syst]["p"]["times"].append(f'{qid}:{med}')
                data[syst]["p"]["variances"].append(f'{qid}:{var}')

                if qid in range(1, 23):
                    gps.append(med)
                else:
                    gps.append('--')
        elif syst == 'smokedduck':
            QList = qlist[syst] if qlist and syst in qlist else range(
                qstart, qend + 1)
            for qid in QList:
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(
                    # f'{os.getcwd()}/{sf}/{bench}/results/smd_capDq{qid}_p1_res.txt')
                    f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_p1_res.txt')
                data[syst]["1"]["times"].append(f'{qid}:{med}')
                data[syst]["1"]["variances"].append(f'{qid}:{var}')
                if qid in range(1, 23):
                    sd1s.append(med)
                else:
                    sd1s.append('--')
                var = 0.0
                med = 0.0
                if isSPecialSMD:
                # (med, var) = getDuckdbA(
                        # f'{os.getcwd()}/newRes/{sf}/{bench}/results/smd_capDq{qid}_p2_res.txt')
                    (med, var) == (0.0, 0.00)
                else:
                    (med, var) = getDuckdbB( f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_p2_res.txt')
                data[syst]["2"]["times"].append(f'{qid}:{med}')
                data[syst]["2"]["variances"].append(f'{qid}:{var}')
                if qid in range(1, 23):
                    sd2s.append(med)
                else:
                    sd2s.append('--')

        elif syst == 'sqlprov':
            QList = qlist[syst] if qlist and syst in qlist else range(
                qstart, qend + 1)
            for qid in QList:
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(
                    # f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{qid}_p1_res.txt')
                    f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{qid}_p1_res.txt')
                data[syst]["1"]["times"].append(f'{qid}:{med}')
                data[syst]["1"]["variances"].append(f'{qid}:{var}')
                med = 0.0
                var = 0.0
                if qid in range(1, 23):
                    sp1s.append(med)
                else:
                    sp1s.append('--')
                (med, var) = getPostgresql(
                    # f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{qid}_p2_res.txt')
                    f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{qid}_p2_res.txt')
                data[syst]["2"]["times"].append(f'{qid}:{med}')
                data[syst]["2"]["variances"].append(f'{qid}:{var}')
                if qid in range(1, 23):
                    sp2s.append(med)
                else:
                    sp2s.append('--')
        elif syst == 'provsql':
            QList = qlist[syst] if qlist and syst in qlist else range(
                qstart, qend + 1)
            for qid in QList:
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(
                    # f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{qid}_res.txt')
                    f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{qid}_res.txt')
                data[syst]["times"].append(f'{qid}:{med}')
                data[syst]["variances"].append(f'{qid}:{var}')
                if qid in range(1, 23):
                    prs.append(med)
                else:
                    prs.append('--')
        elif syst == 'postgresql':
            QList = qlist[syst] if qlist and syst in qlist else range(qstart, qend + 1)
            for qid in QList:
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(f'{os.getcwd()}/newRes/{bench}/results/postgresql_capPq{qid}_res.txt')
                data[syst]["times"].append(f'{qid}: {med}')
                data[syst]["variances"].append(f'{qid}: {var}')
                if qid in range(1, 23):
                    posts.append(med)
                else:
                    posts.append('--')
        elif syst == 'duckdb':
            QList = qlist[syst] if qlist and syst in qlist else range(qstart, qend + 1)
            for qid in QList:
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(f'{os.getcwd()}/newRes/{bench}/results/duckdb_capDq{qid}_res.txt')
                data[syst]["times"].append(f'{qid}: {med}')
                data[syst]["variances"].append(f'{qid}: {var}')
                if qid in range(1, 23):
                    ducks.append(med)
                else:
                    ducks.append('--')
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
    name = f'{bench}' if specificName is None else bench + specificName
    with open(f'{os.getcwd()}/zackups/{sf}/{name}.json', 'w') as fff:
        json.dump(data, fff, indent=4)
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
        if "########## DBSIZE AFTER 9:" in line:
            afterSize = float(lines[lineIdx + 3])
        lineIdx += 1

    return afterSize - beforeSize
def getStorage(sf, bench, syss: list, qstart, qend, qlist: {} = None):
    prs = []
    sps = []
    sds = []
    for syst in syss:
        if syst == 'smokedduck':
            QList = qlist['smokedduck'] if qlist and 'smokedduck' in qlist else range(qstart, qend + 1)
            for qid in QList:
                storage = getSMD(
                    f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_import_res.txt')
                sizeInMB = float(storage / (1024 * 1024))
                sds.append(f'{qid}:{sizeInMB}')
        elif syst == 'sqlprov':
            QList = qlist['sqlprov'] if qlist and 'sqlprov' in qlist else range(qstart, qend + 1)
            for qid in QList:
                storage = getSQLProv(
                    f'{os.getcwd()}/newRes/{bench}/results/logSize_q{qid}.txt')
                sizeInMB = float(storage / (1024 * 1024))
                sps.append(f'{qid}:{sizeInMB}')
        elif syst == 'provsql':
            QList = qlist['provsql'] if qlist and 'provsql' in qlist else range(qstart, qend + 1)
            for qid in QList:
                storage = getProvsql(
                    f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{qid}_res.txt')
                sizeInMB = float(storage / (1024 * 1024)) / 10
                prs.append(f'{qid}:{sizeInMB}')
    for syst in syss:
        print(f"processing {sf}.....")
        if syst == 'gprom':
            print(f"gprom: {...}")
        elif syst == 'smokedduck':
            print(f"smokedduck: {sds}")
        elif syst == 'sqlprov':
            print(f"sqlprov: {sps}")
        elif syst == 'provsql':
            print(f"provsql: {prs}")

    data = {
        'provsql': prs,
        'smokedduck': sds,
        'sqlprov':sps
    }
    with open(f'{os.getcwd()}/zackups/{sf}/{bench}STORAGE.json', 'w') as fff:
        json.dump(data, fff, indent=4)

if __name__ == "__main__":
    os.makedirs(f'{os.getcwd()}/zackups/sf1', exist_ok=True)
    sf = 'sf1'
    tpchList = {
        "gprom": [1, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 19],
        "smokedduck": [1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 13, 16, 18, 20, 21],
        "sqlprov": [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 15, 16, 17, 18, 19, 21, 22],
        "provsql": [1, 6, 7, 9, 12, 19]
    }
    SpecialSMD = ['QMLAgg', 'QMLAgg2']
    getData(sf, 'QTPCH', ['provsql'], 1, 22, qlist=tpchList, isSPecialSMD = True if 'QTPCH' in SpecialSMD else False)
    getStorage(sf, 'QTPCH', ['provsql'], 1, 22, qlist=tpchList)
