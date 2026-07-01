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
            "var-time": []
        },
        "d": {
            "times": [],
            "variances": [],
            "var-time": []
        }
    }
    res["smokedduck"] = {
        "1": {
            "times": [],
            "variances": [],
            "var-time": []
        },
        "2": {
            "times": [],
            "variances": [],
            "var-time": []
        }
    }
    res["sqlprov"] = {
        "1": {
            "times": [],
            "variances": [],
            "logsize": [],
            "var-time": []
        },
        "2": {
            "times": [],
            "variances": [],
            "var-time": []
        }
    }

    res["provsql"] = {
        "times": [],
        "variances": [],
        "var-time": []
    }

    res["links"] = {
        "times": [],
        "variances": [],
        "var-time": []
    }

    res["postgresql"] = {
        "times":[],
        "variances": [],
        "var-time": []
    }

    res["duckdb"] = {
        "times":[],
        "variances":[],
        "var-time": []
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
                    data[syst]["d"]["times"].append(med)
                    data[syst]["d"]["variances"].append(var)
                    data[syst]["d"]["var-time"].append(var/med)


                (med, var) = getPostgresql( f'{os.getcwd()}/newRes/{bench}/results/gprom_capPq{qid}_res.txt')
                data[syst]["p"]["times"].append(med)
                data[syst]["p"]["variances"].append(var)
                data[syst]["p"]['var-time'].append(float(var / med))
        elif syst == 'smokedduck':
            QList = qlist[syst] if qlist and syst in qlist else range(
                qstart, qend + 1)
            for qid in QList:
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(
                    # f'{os.getcwd()}/{sf}/{bench}/results/smd_capDq{qid}_p1_res.txt')
                    f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_p1_res.txt')
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                data[syst]["1"]['var-time'].append(float(var / med))
                var = 0.0
                med = 0.0
                if isSPecialSMD:
                # (med, var) = getDuckdbA(
                        # f'{os.getcwd()}/newRes/{sf}/{bench}/results/smd_capDq{qid}_p2_res.txt')
                    (med, var) == (0.0, 0.00)
                if bench in ['PMPP']:
                    (med, var) = getDuckdbTimer( f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_p2_res.txt', removeUnecessary=1, theNth=3)
                else:
                    (med, var) = getDuckdbB( f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{qid}_p2_res.txt')
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                data[syst]["2"]['var-time'].append(float(var / med))

        elif syst == 'sqlprov':
            QList = qlist[syst] if qlist and syst in qlist else range(
                qstart, qend + 1)
            for qid in QList:
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(
                    # f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{qid}_p1_res.txt')
                    f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{qid}_p1_res.txt')
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                data[syst]["1"]['var-time'].append(float(var / med))

                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(
                    # f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{qid}_p2_res.txt')
                    f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{qid}_p2_res.txt')
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                data[syst]["2"]['var-time'].append(float(var / med))

        elif syst == 'provsql':
            QList = qlist[syst] if qlist and syst in qlist else range(
                qstart, qend + 1)
            for qid in QList:
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(
                    # f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{qid}_res.txt')
                    f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{qid}_res.txt')
                data[syst]["times"].append(med)
                data[syst]["variances"].append(var)
                data[syst]['var-time'].append(float(var / med))
        elif syst == 'postgresql':
            QList = qlist[syst] if qlist and syst in qlist else range(qstart, qend + 1)
            for qid in QList:
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(f'{os.getcwd()}/newRes/{bench}/results/postgresql_capPq{qid}_res.txt')
                data[syst]["times"].append(med)
                data[syst]["variances"].append(var)
                data[syst]['var-time'].append(float(var / med))
        elif syst == 'duckdb':
            QList = qlist[syst] if qlist and syst in qlist else range(qstart, qend + 1)
            for qid in QList:
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(f'{os.getcwd()}/newRes/{bench}/results/duckdb_capDq{qid}_res.txt')
                data[syst]["times"].append(med)
                data[syst]["variances"].append(var)
                data[syst]['var-time'].append(float(var / med))

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


def getDataTPCH(sf, bench, syss: list, qstart, qend, qlist: {} = None, isSPecialSMD = False, isGProMPostOnly = False, specificName = None):
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






if __name__ == "__main__":
    os.makedirs(f'{os.getcwd()}/zackups/sf1', exist_ok=True)
#     benchs = {
#         # 'VPGN': {
#         #     "qrange": [1, 3],
#         #     "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql', 'postgresql', 'duckdb']
#         # },
#         # 'VPGS': {
#         #     "qrange": [1, 3],
#         #     "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql', 'postgresql', 'duckdb']
#         # },
#         'FPAgg': {
#             "qrange": [1, 3],
#             "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql', 'postgresql', 'duckdb']
#         },
#         # 'FPDist': {
#         #     "qrange": [1, 3],
#         #     "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql', 'postgresql', 'duckdb']
#         # },
#         # 'FPSDist': {
#         #     "qrange": [1, 18],
#         #     "sys": ['gprom', 'sqlprov', 'provsql', 'postgresql', 'duckdb']
#         # },
#         # 'VPJJ': {
#         #     "qrange": [1, 1],
#         #     "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql', 'postgresql', 'duckdb']
#         # },
#         # 'VPJJJ': {
#         #     "qrange": [1, 1],
#         #     "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql', 'postgresql', 'duckdb']
#         # },
#         # 'VPJC': {
#         #     "qrange": [1, 3],
#         #     "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql', 'postgresql', 'duckdb']
#         # },
#         # 'VPJS': {
#         #     "qrange": [1, 3],
#         #     "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql', 'postgresql', 'duckdb']
#         # },
#         # 'QTopK': {
#         #     "qrange": [1, 3],
#         #     "sys": ['gprom', 'sqlprov', 'provsql', 'smokedduck', 'postgresql', 'duckdb']
#         # },
#         # 'QTopK2':{
#         #     "qrange": [1, 3],
#         #     "sys": ['gprom', 'sqlprov', 'smokedduck', 'postgresql', 'duckdb']

#         # },
#         # 'QMLAgg': {
#         #     "qrange": [1, 1],
#         #     "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql', 'postgresql', 'duckdb']
#         # },
#         # 'QMLAgg2': {
#         #     "qrange": [1, 1],
#         #     "sys": ['gprom', 'smokedduck', 'postgresql', 'duckdb', 'sqlprov']
#         # },
#         # 'QAggNum': {
#         #     "qrange": [1, 2],
#         #     "sys": ['gprom', 'smokedduck', 'sqlprov', 'provsql', 'postgresql', 'duckdb']
#         # },
#         # 'FPSAgg': {
#         #     "qrange": [1, 6],
#         #     "sys": ['gprom', 'smokedduck', 'sqlprov', 'postgresql', 'duckdb']
#         # },
#         # 'QCMPLDC':{
#         #     "qrange": [1, 1],
#         #     "sys": ['gprom', 'sqlprov', 'provsql', 'postgresql', 'duckdb', 'smokedduck']
#         # },
#         # 'PMPP': {
#         #     "qrange": [1, 3],
#         #     "sys": ['gprom', 'provsql', 'smokedduck']
#         # },
#         'QARGMIN': {
#             "qrange": [1, 1],
#             "sys": ['gprom', 'sqlprov', 'smokedduck', 'postgresql', 'duckdb']
#         },
#         # 'PMAP':{
#         #     "qrange": [1, 6],
#         #     "sys": ['gprom']
#         # }
#         # 'QRCRW':{
#         #     "qrange": [1, 2],
#         #     "sys": ['sqlprov', 'postgresql', ]
#         # },
#         # 'QWIN1':{
#         #     "qrange": [1, 1],
#         #     "sys": ['sqlprov', 'postgresql', ]
#         # },
#         # 'QWIN2':{
#         #     "qrange": [1, 1],
#         #     "sys": ['sqlprov', 'postgresql', ]
#         # },

#     }
#     SpecialSMD = ['QMLAgg', 'QMLAgg2']
#     # for bench in benchs:
#     #     sysss = benchs[bench]["sys"]
#     #     qrange = benchs[bench]["qrange"]
#     #     print(bench)
#     #     print(sysss)
#     #     print(qrange)
#     #     print(f"isSpecialSMD: {True if bench in SpecialSMD else False}")
#     #     getData(sf, bench, sysss, qrange[0], qrange[1], qlist=None, isSPecialSMD = True if bench in SpecialSMD else False)
#     # getData(sf, 'PMAP', ['gprom'], 1, 6, qlist=None, isSPecialSMD = False, isGProMPostOnly=True)
#     # getData(sf, 'PMPP', ['gprom', 'smokedduck', 'provsql'], 1, 3, qlist=None, isSPecialSMD = False, isGProMPostOnly=False)
#     # getData(sf, 'PMPP', ['provsql', 'smokedduck'], 4, 4, qlist=None, isSPecialSMD = False, isGProMPostOnly=True, specificName = '2')
#     # getData(sf, 'QARGMIN', ['smokedduck', 'postgresql', 'duckdb', 'gprom', 'sqlprov'], 1, 1, qlist=None, isSPecialSMD = False, isGProMPostOnly=True)
# #

    # All systems: provsql, gprom, smokedduck, sqlprov, postgresql, duckdb
    sf = 'sf1'
    getData(sf, 'FPAgg', ['postgresql', 'duckdb', 'sqlprov', 'provsql', 'gprom', 'smokedduck'], 1, 3, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'FPSAgg', ['postgresql', 'duckdb', 'sqlprov', 'gprom', 'smokedduck'], 1, 4, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'FPDist', ['postgresql', 'duckdb', 'sqlprov', 'provsql', 'gprom', 'smokedduck'], 1, 3, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'FPSDist', ['postgresql', 'duckdb', 'sqlprov', 'provsql', 'gprom', 'smokedduck'], 1, 18, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'VPGN', ['postgresql', 'duckdb', 'sqlprov', 'provsql', 'gprom', 'smokedduck'], 1, 3, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'VPGS', ['postgresql', 'duckdb', 'sqlprov', 'provsql', 'gprom', 'smokedduck'], 1, 3, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'VPJJ', ['postgresql', 'duckdb', 'sqlprov', 'provsql', 'gprom', 'smokedduck'], 1, 1, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'VPJJJ', ['postgresql', 'duckdb', 'sqlprov', 'provsql', 'gprom', 'smokedduck'], 1, 1, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'VPJC', ['postgresql', 'duckdb', 'sqlprov', 'provsql', 'gprom', 'smokedduck'], 1, 3, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'VPJS', ['postgresql', 'duckdb', 'sqlprov', 'provsql', 'gprom', 'smokedduck'], 1, 3, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'QARGMIN', ['postgresql', 'duckdb', 'sqlprov', 'gprom', 'smokedduck'], 1, 2, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'QCMPLDC', ['postgresql', 'duckdb', 'sqlprov', 'provsql', 'gprom', 'smokedduck'], 1, 3, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'QLIMIT', ['postgresql', 'duckdb', 'sqlprov', 'provsql', 'gprom', 'smokedduck'], 1, 3, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'QMLAgg', ['postgresql', 'duckdb', 'sqlprov', 'gprom', 'smokedduck'], 1, 2, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'QRCRW', ['postgresql', 'sqlprov'], 1, 2, qlist=None, isSPecialSMD = False, isGProMPostOnly=True)
    getData(sf, 'QSET', ['postgresql', 'duckdb', 'provsql', 'gprom', 'smokedduck'], 1, 3, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'QWIN', ['postgresql', 'sqlprov'], 1, 3, qlist=None, isSPecialSMD = False, isGProMPostOnly=True)
    getData(sf, 'QAggNum', ['postgresql', 'duckdb', 'sqlprov', 'provsql', 'gprom', 'smokedduck'], 1, 2, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    getData(sf, 'QTopk2', ['postgresql', 'duckdb', 'sqlprov', 'gprom', 'smokedduck'], 1, 4, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    # -- QWHRSUB 1-3, for gprom 4-6, get the data below;
    getData(sf, 'QWHRSUB', ['postgresql', 'sqlprov', 'gprom', 'duckdb', 'smokedduck'], 1, 3, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
    # -- gprom has 6 queries where others have 3 queries
    # getData(sf, 'QWHRSUB', ['gprom'], 1, 6, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)

#
#     # PMAP get postgresql, since postgresql only run 1 times,
    getData(sf, 'PMAP', ['gprom'], 1, 6, qlist = None, isSPecialSMD= False, isGProMPostOnly= True)
#
#     # -- PMPP 1-3 including GPROM
    getData(sf, 'PMPP', ['provsql', 'gprom', 'smokedduck'], 1, 3, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)

#     # -- PMPP 4-5 provsql and smokedduck
    # getData(sf, 'PMPP', ['provsql', 'smokedduck'], 1, 5, qlist = None, isSPecialSMD= False, isGProMPostOnly= False)
