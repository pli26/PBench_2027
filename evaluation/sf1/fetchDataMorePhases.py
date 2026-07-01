import os
import statistics as sta
import re
import json


def resStructures():
    res = {}
    res["gprom"] = {
        "dt":{
            "p": {
                "times": [],
                "variances": [],
                "rescnt": [],
                "var-time":[]
            },
            "d": {
                "times": [],
                "variances": [],
                "rescnt": [],
                "var-time":[]
            }
        },
        "id":{
            "p": {
                "times": [],
                "variances": [],
                "rescnt": [],
                "var-time":[]
            },
            "d": {
                "times": [],
                "variances": [],
                "rescnt": [],
                "var-time":[]
            }
        }
    }
    res["smokedduck"] = {
        "1": {
            "times": [],
            "variances": [],
            "var-time":[]
        },
        "2": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "3": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "4": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "5": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "6": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
    }
    res["sqlprov"] = {
        "1": {
            "times": [],
            "variances": [],
            "logsize": [],
            "var-time":[]

        },
        "2": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "3": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "4": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "5": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "6": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
    }

    res["provsql"] = {
        "1": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "2": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "3": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "4": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "5": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
        "6": {
            "times": [],
            "variances": [],
            "var-time":[]

        },
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

def getDuckdbP4(infile, remotTop=RMTOP):
    fff = open(infile, 'r')
    lines = fff.readlines()
    fff.close()

    times = []
    tmpLines = []
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

    TT = []
    for idx in range(0, len(times), 2):
        TT.append(times[idx] + times[idx+1])

    times = TT
    print(f"infile: {infile}, times  of times after processing: {len(times)}")
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
def getPostgresqlSPP4(infile, remotTop=RMTOP):
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
    print(times)
    print(f"len of times before processing: {len(times)}")
    TT = []
    for idx in range(0, len(times), 2):
        TT.append(times[idx] + times[idx+1])
    times = TT
    print(f"infile: {infile}, times  of times after processing: {len(times)}")
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

def getPostgresqlWithoutMidian(infile, remotTop=RMTOP):
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
    return times

def getDuckdbWithoutMidian(infile, remotTop=RMTOP):
    fff = open(infile, 'r')
    lines = fff.readlines()
    fff.close()

    times = []
    tmpLines = []
    for line in lines:
        if len(line) > len('Total Time:') and 'Total Time:' in line:
            match = re.search(r'Total Time:\s*([\d.]+)s', line)
            if match:
                timeValue = match.group(1)
            else:
                print(f"Unexpected time format in line: {line}")
                exit()
            readTime = float(timeValue)
            times.append(readTime)
    return times

def getData(sf='sf1', bench='FPAgg', syss=['sqlprov'], qstart = 1, qend = 4, savename = 'tmp'):
    data = resStructures()
    for syst in syss:
        print(f"processing {sf}.....")
        if syst == 'sqlprov':
            p1 = []
            p2 = []
            p3 = []
            p4 = []
            p5 = []
            p6 = []
            for q in range(qstart, qend + 1):
                # -- p1
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                p1.append(med)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                if med != 0.0:
                    data[syst]["1"]["var-time"].append(float(var / med))
                else:
                    data[syst]["1"]["var-time"].append(float(0))

                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                p2.append(med)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                data[syst]["2"]["var-time"].append(float(var / med))

                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                p4.append(med)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                data[syst]["4"]["var-time"].append(float(var / med))

                # -- p6
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p6_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                p6.append(med)
                data[syst]["6"]["times"].append(med)
                data[syst]["6"]["variances"].append(var)
                data[syst]["6"]["var-time"].append(float(var / med))

        if syst == 'provsql':
            for q in range(qstart, qend + 1):
                ## -- p1
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                data[syst]["1"]["var-time"].append(float(var / med))

                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                data[syst]["2"]["var-time"].append(float(var / med))

                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                data[syst]["4"]["var-time"].append(float(var / med))

                # -- p6
                if bench != 'PMBD': ## PMFD does not have p6
                    file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p6_res.txt'
                    med = 0.0
                    var = 0.0
                    (med, var) = getPostgresql(file)
                    data[syst]["6"]["times"].append(med)
                    data[syst]["6"]["variances"].append(var)
                    data[syst]["6"]["var-time"].append(float(var / med))
                else:
                    timess = getPostgresqlWithoutMidian(file)
                    print("PMBDDDDDDDD PROVSQLLLLLLL")
                    print(f'len of timess: {len(timess)}, timess: {timess}')
                    qqq = qid - 1
                    times = []
                    while qqq < len(timess):
                        times.append(timess[qqq])
                        qqq += 5
        if syst == 'smokedduck':
            for q in range(qstart, qend + 1):
                # -- p1
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                data[syst]["1"]["var-time"].append(float(var / med))

                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                data[syst]["2"]["var-time"].append(float(var / med))
                # -- p3
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p3_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["3"]["times"].append(med)
                data[syst]["3"]["variances"].append(var)
                data[syst]["3"]["var-time"].append(float(var / med))

                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbP4(file)
                print(f"med: {med}, var: {var}")
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                data[syst]["4"]["var-time"].append(float(var / med))

                # -- p5
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p5_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["5"]["times"].append(med)
                data[syst]["5"]["variances"].append(var)
                if med != float(0):
                    data[syst]["5"]["var-time"].append(float(var / med))

                # -- p6
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p6_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["6"]["times"].append(med)
                data[syst]["6"]["variances"].append(var)

                data[syst]["6"]["var-time"].append(float(var / med))

    with open(f'{os.getcwd()}/zackups/{sf}/{bench}_{savename}.json', 'w') as fff:
        json.dump(data, fff, indent=4)



def getDataFD(sf='sf1', bench='FPAgg', syss=['sqlprov'], qstart = 1, qend = 4, savename = 'tmp'):
    data = resStructures()
    for syst in syss:
        print(f"processing {sf}.....")
        if syst == 'sqlprov':
            p4 = []
            for q in range(qstart, qend + 1):
                # -- p1
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                data[syst]["1"]["var-time"].append(float(var / med))

                    # -- p2
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                data[syst]["2"]["var-time"].append(float(var / med))
                # -- p4
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                data[syst]["4"]["var-time"].append(float(var / med))

                    # -- p6
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p6_res.txt'
                timess = getPostgresqlWithoutMidian(file)
                print("PMBDDDDDDDD SQLPROVVVVVVVVVV" + f'len of timess: {len(timess)}, timess: {timess}')

        if syst == 'provsql':
            for q in range(qstart, qend + 1):
                ## -- p1
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                data[syst]["1"]["var-time"].append(float(var / med))
                # -- p2
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                data[syst]["2"]["var-time"].append(float(var / med))

                # -- p4
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                data[syst]["4"]["var-time"].append(float(var / med))
                # -- p6
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p6_res.txt'
                timess = getPostgresqlWithoutMidian(file)
                print("PMBDDDDDDDD ROVVVVVVVVVV" + f'len of timess: {len(timess)}, timess: {timess}')

    with open(f'{os.getcwd()}/zackups/{sf}/{bench}_{savename}.json', 'w') as fff:
        json.dump(data, fff, indent=4)

def getDataPMBDG(sf='sf1', bench='PMBD', syss=['gprom'], qstart = 1, qend = 4, whichones = [2], savename = 'tmp'):
    data = resStructures()
    for qid in range(qstart, qend + 1):
        print(f"processing {sf}.....")
        file = f'{os.getcwd()}/newRes/{bench}/results/gprom_capPq{qid}_dt_res.txt'
        timesss = getPostgresqlWithoutMidian(file)
        times = []
        print(f"timesss: {timesss}")
        print(f"whichones: {whichones}")
        print(f'type of timesss: {type(timesss)}, length of timesss: {len(timesss)}')
        idx = 0
        while idx < len(timesss):
            time = 0.0
            for w in whichones:
                time += timesss[idx + w]
            times.append(time)
            idx += 3
        times = times[RMTOP:]
        median = sta.median(times)
        variabce = sta.variance(times)
        data['gprom']["dt"]["p"]["times"].append(median)
        data['gprom']["dt"]["p"]["variances"].append(variabce)
        data['gprom']["dt"]['p']["var-time"].append(float(variabce / median))
    for qid in range(qstart, qend + 1):
        file = f'{os.getcwd()}/newRes/{bench}/results/gprom_capDq{qid}_dt_res.txt'
        timesss = getDuckdbWithoutMidian(file)
        print(f"duckdb timesss: {timesss}")
        times = []
        idx = 0
        while idx < len(timesss):
            time = 0.0
            for w in whichones:
                time += timesss[idx + w]
            times.append(time)
            idx += 3

        times = times[RMTOP:]
        print(f"duckdb times: {times}")
        median = sta.median(times)
        variabce = sta.variance(times)
        print(f'median: {median}')
        data['gprom']["dt"]["d"]["times"].append(median)
        data['gprom']["dt"]["d"]["variances"].append(variabce)
        data['gprom']["dt"]["d"]["var-time"].append(float(variabce / median))

    with open(f'{os.getcwd()}/zackups/{sf}/{bench}_{savename}.json', 'w') as fff:
        json.dump(data, fff, indent=4)
def getDataPMFDG(sf='sf1', bench='PMFD', syss=['gprom'], qstart = 1, qend = 4, whichones = [2], queryspecifics: list = [], savename = 'tmp'):
    data = resStructures()
    specificid = 0
    for qid in range(qstart, qend + 1):
        print(f"processing {sf}.....PMFD")
        file = f'{os.getcwd()}/newRes/{bench}/results/gprom_capPq{qid}_dt_res.txt'
        timesss = getPostgresqlWithoutMidian(file)
        assert len(timesss) == 170, f"Expected 170 time entries in file {file}, but got {len(timesss)}"

        for qq in range(2, 17):
            times = timesss[qq:len(timesss):17]
            print(f"times for qid {qid}, qq {qq}: {times}")
            med = sta.median(times)
            var = sta.variance(times)
            data['gprom']["dt"]["p"]["times"].append(med)
            data['gprom']["dt"]["p"]["variances"].append(var)
            data['gprom']["dt"]["p"]["var-time"].append(float(var / med))


        file = f'{os.getcwd()}/newRes/{bench}/results/gprom_capDq{qid}_dt_res.txt'
        timesss = getDuckdbWithoutMidian(file)
        assert len(timesss) == 170, f"Expected 170 time entries in file {file}, but got {len(timesss)}"
        for qq in range(2, 17):
            times = timesss[qq:len(timesss):17]
            med = sta.median(times)
            var = sta.variance(times)
            data['gprom']["dt"]["d"]["times"].append(med)
            data['gprom']["dt"]["d"]["variances"].append(var)
            data['gprom']["dt"]["d"]["var-time"].append(float(var / med))


    with open(f'{os.getcwd()}/zackups/{sf}/{bench}_{savename}.json', 'w') as fff:
        json.dump(data, fff, indent=4)

def getDataPMBD(sf = 'sf1', bench = 'PMBD', syss = ['sqlprov'], qstart = 1, qend = 4, savename = 'tmp'):
    print("YES")
    data = resStructures()
    for syst in syss:
        print(f"processing {sf}.....")
        if syst == 'sqlprov':
            print("SQLPROV")
            for q in range(qstart, qend + 1):
                # -- p1
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                data[syst]["1"]["var-time"].append(float(var / med))

                print(f"p1: {med}, {var}")
                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                data[syst]["2"]["var-time"].append(var / med)

                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                data[syst]["4"]["var-time"].append(var / med)

                # -- p6
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p6_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["6"]["times"].append(med)
                data[syst]["6"]["variances"].append(var)
                data[syst]["6"]["var-time"].append(var/med)
        if syst == 'provsql':
            print("PROVSQL")
            qidx = 0
            for q in range(qstart, qend + 1):
                print(f'{bench} - q: {q} - {syst}')
                ## -- p1
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                data[syst]["1"]["var-time"].append(var / med)
                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                data[syst]["2"]["var-time"].append(var/ med)
                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                data[syst]["4"]["var-time"].append(var / med)

                # -- p6
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p6_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["6"]["times"].append(med)
                data[syst]["6"]["variances"].append(var)
                data[syst]["5"]["var-time"].append(var / med)
                qidx += 1
        if syst == 'smokedduck':
            print("SMOKEDDUCK")
            for q in range(qstart, qend + 1):
                # -- p1
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)

                data[syst]["1"]["var-time"].append(var / med)
                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var )

                data[syst]["2"]["var-time"].append(var / med)
                # -- p3
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p3_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["3"]["times"].append(med)
                data[syst]["3"]["variances"].append(var)
                data[syst]["3"]["var-time"].append(var / med)
                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                data[syst]["4"]["var-time"].append(var / med)
                # -- p5
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p5_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["5"]["times"].append(med)
                data[syst]["5"]["variances"].append(var)
                if med != float(0):
                    data[syst]["5"]["var-time"].append(var / med)
                else:
                    data[syst]["5"]["var-time"].append(0.0)

                # -- p6
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p6_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["6"]["times"].append(med)
                data[syst]["6"]["variances"].append(var)
                data[syst]["6"]["var-time"].append(var / med)
    print(f"data: {data}")
    with open(f'{os.getcwd()}/zackups/{sf}/{bench}_{savename}.json', 'w') as fff:
        json.dump(data, fff, indent=4)
def getDataPMFD(sf = 'sf1', bench = 'PMFD', syss = ['sqlprov'], qstart = 1, qend = 4, savename = 'tmp'):
    print("YES")
    data = resStructures()
    for syst in syss:
        print(f"processing {sf}.....")
        if syst == 'sqlprov':
            print("SQLPROV")
            for q in range(qstart, qend + 1):
                # -- p1
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                data[syst]["1"]["var-time"].append(var / med)

                print(f"p1: {med}, {var}")
                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                data[syst]["2"]["var-time"].append(var / med)
                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                data[syst]["4"]["var-time"].append(var / med)
                # -- p6
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p6_res.txt'
                timesss = getPostgresqlWithoutMidian(file)
                print(f"PMFD SQLPROVVVVVVVVVV" + f'len of timesss: {len(timesss)}, timesss: {timesss}')
                assert len(timesss) == 150, f"Expected 150 execution times in file {file}, but found {len(timesss)}. Please check the file format."
                for ttt in range(0, 15):
                    times = timesss[ttt:len(timesss):15]
                    med = sta.median(times)
                    var = sta.variance(times)
                    data[syst]["6"]["times"].append(med)
                    data[syst]["6"]["variances"].append(var)
                    data[syst]["6"]["var-time"].append(var / med)
        if syst == 'provsql':
            print("PROVSQL")
            for q in range(qstart, qend + 1):
                ## -- p1
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)

                data[syst]["1"]["var-time"].append(var / med)
                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)

                data[syst]["2"]["var-time"].append(var / med)
                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)

                data[syst]["4"]["var-time"].append(var / med)
                # -- p6
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p6_res.txt'
                timesss = getPostgresqlWithoutMidian(file)
                print("PMFD PROVVVVVVVVVV" + f'len of timesss: {len(timesss)}, timesss: {timesss}')
                assert len(timesss) == 90, f"Expected 150 execution times in file {file}, but found {len(timesss)}. Please check the file format."
                for ttt in range(0, 15):
                    times = timesss[ttt:len(timesss):15]
                    med = sta.median(times)
                    var = sta.variance(times)
                    data[syst]["6"]["times"].append(med)
                    data[syst]["6"]["variances"].append(var)

                    data[syst]["6"]["var-time"].append(var / med)
        if syst == 'smokedduck':
            print("SMOKEDDUCK")
            for q in range(qstart, qend + 1):
                # -- p1
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)

                data[syst]["1"]["var-time"].append(var / med)
                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)

                data[syst]["2"]["var-time"].append(var / med)
                # -- p3
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p3_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["3"]["times"].append(med)
                data[syst]["3"]["variances"].append(var)

                data[syst]["3"]["var-time"].append(var / med)
                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)

                data[syst]["4"]["var-time"].append(var / med)
                # -- p5
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p5_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["5"]["times"].append(med)
                data[syst]["5"]["variances"].append(var)
                if med != float(0.0):
                    data[syst]["5"]["var-time"].append(var / med)
                else:
                    data[syst]["5"]["var-time"].append(0.0)

                # -- p6
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p6_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                timesss = getDuckdbWithoutMidian(file)
                print(f"PMFD SMDDDD" + f'len of timesss: {len(timesss)}, timesss: {timesss}')
                assert len(timesss) == 150, f"Expected 150 execution times in file {file}, but found {len(timesss)}. Please check the file format."
                for ttt in range(0, 15):
                    times = timesss[ttt:len(timesss):15]
                    med = sta.median(times)
                    var = sta.variance(times)
                    data[syst]["6"]["times"].append(med)
                    data[syst]["6"]["variances"].append(var)
                    if med != float(0.0):
                        data[syst]["6"]["var-time"].append(var / med)
                    else:
                        data[syst]["6"]["var-time"].append(0.0)

    with open(f'{os.getcwd()}/zackups/{sf}/{bench}_{savename}.json', 'w') as fff:
        json.dump(data, fff, indent=4)

if __name__ == "__main__":
    os.makedirs(f'{os.getcwd()}/zackups/sf1', exist_ok=True)
    benchs = {
        # 'PMRLIN': {
        #     "qrange": [1, 4],
        #     "sys": ['sqlprov', 'provsql']
        # },
        'PMRLIN2': {
            "qrange": [1, 4],
            "sys": ['sqlprov', 'provsql', 'smokedduck']
        },
    }
    plot = True
    sf = 'sf1'
    if plot:
        # -- Non-gprom
        for bench in benchs:

            getData(sf=sf, bench=bench, syss=benchs[bench]["sys"], qstart=1, qend= 3, savename='rlsppr')
            getData(sf=sf, bench=bench, syss=benchs[bench]["sys"], qstart=4, qend= 4, savename='flsppr')
        # -- Gprom
        # -- LIN
        getDataPMBDG(sf=sf, bench='PMRLIN2', syss=['gprom'], qstart=1, qend=3, whichones=[2], savename='rlgpuse')
        getDataPMBDG(sf=sf, bench='PMRLIN2', syss=['gprom'], qstart=1, qend=3, whichones=[0], savename='rlgpcap')
        getDataPMBDG(sf=sf, bench='PMRLIN2', syss=['gprom'], qstart=4, qend=4, whichones=[2], savename='flgpuse')
        getDataPMBDG(sf=sf, bench='PMRLIN2', syss=['gprom'], qstart=4, qend=4, whichones=[0], savename='flgpcap')

        # # -- gprom bd:
        getDataPMBD(sf=sf, bench='PMBD', syss=['sqlprov', 'provsql', 'smokedduck'], qstart=1, qend= 5, savename='sppr')

        getDataPMBDG(sf=sf, bench='PMBD', syss=['gprom'], qstart=1, qend=5, whichones=[2], savename='gp')

        # # -- gprom fd:
        getDataPMFD(sf=sf, bench='PMFD', syss=['sqlprov', 'provsql', 'smokedduck'], qstart=1, qend=3, savename='sppr')
        whichones = []
        for ii in range(2, 17):
            whichones.append(ii)
        print(f"whichones: {whichones}")
        queryspecificones = []
        start = 0
        queryspecificones.append([2, 5, 8, 11, 14])
        queryspecificones.append([3, 6, 9, 12, 15])
        queryspecificones.append([4, 7, 10, 13, 16])
        print(f"queryspecificones: {queryspecificones}")
        getDataPMFDG(sf=sf, bench='PMFD', syss=['gprom'], qstart=1, qend=3, whichones=[2], queryspecifics=queryspecificones, savename='gp')
        # '''
        getDataPMFD(sf=sf, bench='PMFD', syss=['sqlprov', 'provsql', 'smokedduck'], qstart=1, qend=3, savename='sppr')
