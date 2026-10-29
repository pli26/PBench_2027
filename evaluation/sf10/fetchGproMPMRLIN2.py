import os
import statistics as sta
import re
import json





RMTOP = 3
def getAllDUCK(file):
    times = []
    fff = open(file, 'r')
    lines = fff.readlines()
    fff.close()
    for line in lines:
        if "Total Time:" in line:
            # print(line)
            aLine = line.strip().split(":")[1].strip()
            aLine = aLine.replace("│", '').strip()
            # print(aLine)
            if aLine[-1] == "s":
                # print(aLine)
                time = float(aLine[:-1].strip())
                times.append(time)

    return times
def getAllPOSTGRESQL(file):
    times = []
    fff = open(file, 'r')
    lines = fff.readlines()
    fff.close()
    for line in lines:
        if "Execution Time:" in line:
            aLine = line.strip().split(":")[1].strip()
            time = float(aLine.split(" ")[0].strip()) / 1000
            times.append(time)
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
                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                p2.append(med)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                p4.append(med)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)

                # -- p6
                file = f'{os.getcwd()}/newRes/{bench}/results/sp_capPq{q}_p6_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                p6.append(med)
                data[syst]["6"]["times"].append(med)
                data[syst]["6"]["variances"].append(var)
        if syst == 'provsql':
            for q in range(qstart, qend + 1):
                ## -- p1
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                # -- p6
                if bench != 'PMBD': ## PMFD does not have p6
                    file = f'{os.getcwd()}/newRes/{bench}/results/provsql_capPq{q}_p6_res.txt'
                    med = 0.0
                    var = 0.0
                    (med, var) = getPostgresql(file)
                    data[syst]["6"]["times"].append(med)
                    data[syst]["6"]["variances"].append(var)
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
                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                # -- p3
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p3_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["3"]["times"].append(med)
                data[syst]["3"]["variances"].append(var)
                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbP4(file)
                print(f"med: {med}, var: {var}")
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                # -- p5
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p5_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["5"]["times"].append(med)
                data[syst]["5"]["variances"].append(var)
                # -- p6
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p6_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["6"]["times"].append(med)
                data[syst]["6"]["variances"].append(var)

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
                    # -- p2
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)

                # -- p4
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
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
                # -- p2
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)

                # -- p4
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)

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
        file = f'{os.getcwd()}/{sf}/{bench}/results/gprom_capPq{qid}_dt_res.txt'
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
    for qid in range(qstart, qend + 1):
        file = f'{os.getcwd()}/{sf}/{bench}/results/gprom_capDq{qid}_dt_res.txt'
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
    with open(f'{os.getcwd()}/zackups/{sf}/{bench}_{savename}.json', 'w') as fff:
        json.dump(data, fff, indent=4)
def getDataPMFDG(sf='sf1', bench='PMFD', syss=['gprom'], qstart = 1, qend = 4, whichones = [2], queryspecifics: list = [], savename = 'tmp'):
    data = resStructures()
    specificid = 0
    for qid in range(qstart, qend + 1):
        print(f"processing {sf}.....PMFD")
        file = f'{os.getcwd()}/{sf}/{bench}/results/gprom_capPq{qid}_dt_res.txt'
        timesss = getPostgresqlWithoutMidian(file)
        assert len(timesss) == 170, f"Expected 170 time entries in file {file}, but got {len(timesss)}"

        for qq in range(2, 17):
            times = timesss[qq:len(timesss):17]
            print(f"times for qid {qid}, qq {qq}: {times}")
            med = sta.median(times)
            var = sta.variance(times)
            data['gprom']["dt"]["p"]["times"].append(med)
            data['gprom']["dt"]["p"]["variances"].append(var)

        file = f'{os.getcwd()}/{sf}/{bench}/results/gprom_capDq{qid}_dt_res.txt'
        timesss = getDuckdbWithoutMidian(file)
        assert len(timesss) == 170, f"Expected 170 time entries in file {file}, but got {len(timesss)}"
        for qq in range(2, 17):
            times = timesss[qq:len(timesss):17]
            med = sta.median(times)
            var = sta.variance(times)
            data['gprom']["dt"]["d"]["times"].append(med)
            data['gprom']["dt"]["d"]["variances"].append(var)

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
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                print(f"p1: {med}, {var}")
                # -- p2
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                # -- p4
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                # -- p6
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p6_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["6"]["times"].append(med)
                data[syst]["6"]["variances"].append(var)
        if syst == 'provsql':
            print("PROVSQL")
            qidx = 0
            for q in range(qstart, qend + 1):
                ## -- p1
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                # -- p2
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                # -- p4
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                # -- p6
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p6_res.txt'
                timesss = getPostgresqlWithoutMidian(file)
                times = []
                qq = qidx
                while qq < len(timesss):
                    times.append(timesss[qq])
                    qq += 5
                print(f'len of timesss: {len(timesss)}, timesss: {timesss}')
                med = sta.median(times)
                var = sta.variance(times)
                data[syst]["6"]["times"].append(med)
                data[syst]["6"]["variances"].append(var)
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
                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                # -- p3
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p3_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["3"]["times"].append(med)
                data[syst]["3"]["variances"].append(var)
                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                # -- p5
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p5_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["5"]["times"].append(med)
                data[syst]["5"]["variances"].append(var)
                # -- p6
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p6_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["6"]["times"].append(med)
                data[syst]["6"]["variances"].append(var)
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
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                print(f"p1: {med}, {var}")
                # -- p2
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)

                # -- p4
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)

                # -- p6
                file = f'{os.getcwd()}/{sf}/{bench}/results/sp_capPq{q}_p6_res.txt'
                timesss = getPostgresqlWithoutMidian(file)
                print(f"PMFD SQLPROVVVVVVVVVV" + f'len of timesss: {len(timesss)}, timesss: {timesss}')
                assert len(timesss) == 150, f"Expected 150 execution times in file {file}, but found {len(timesss)}. Please check the file format."
                for ttt in range(0, 15):
                    times = timesss[ttt:len(timesss):15]
                    med = sta.median(times)
                    var = sta.variance(times)
                    data[syst]["6"]["times"].append(med)
                    data[syst]["6"]["variances"].append(var)

        if syst == 'provsql':
            print("PROVSQL")
            for q in range(qstart, qend + 1):
                ## -- p1
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p1_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["1"]["times"].append(med)
                data[syst]["1"]["variances"].append(var)
                # -- p2
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresql(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                # -- p4
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getPostgresqlSPP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                # -- p6
                file = f'{os.getcwd()}/{sf}/{bench}/results/provsql_capPq{q}_p6_res.txt'
                timesss = getPostgresqlWithoutMidian(file)
                print("PMFD PROVVVVVVVVVV" + f'len of timesss: {len(timesss)}, timesss: {timesss}')
                assert len(timesss) == 150, f"Expected 150 execution times in file {file}, but found {len(timesss)}. Please check the file format."
                for ttt in range(0, 15):
                    times = timesss[ttt:len(timesss):15]
                    med = sta.median(times)
                    var = sta.variance(times)
                    data[syst]["6"]["times"].append(med)
                    data[syst]["6"]["variances"].append(var)
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
                # -- p2
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p2_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["2"]["times"].append(med)
                data[syst]["2"]["variances"].append(var)
                # -- p3
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p3_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["3"]["times"].append(med)
                data[syst]["3"]["variances"].append(var)
                # -- p4
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p4_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbP4(file)
                data[syst]["4"]["times"].append(med)
                data[syst]["4"]["variances"].append(var)
                # -- p5
                file = f'{os.getcwd()}/newRes/{bench}/results/smd_capDq{q}_p5_res.txt'
                med = 0.0
                var = 0.0
                (med, var) = getDuckdbA(file)
                data[syst]["5"]["times"].append(med)
                data[syst]["5"]["variances"].append(var)
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
    with open(f'{os.getcwd()}/zackups/{sf}/{bench}_{savename}.json', 'w') as fff:
        json.dump(data, fff, indent=4)
def resStructures():
    res = {}

    res["gpromp"] = {
        "1": {
            "times": [],
            "variances": [],
            "logsize": []
        },
        "2": {
            "times": [],
            "variances": []
        },
        "3": {
            "times": [],
            "variances": []
        },
        "4": {
            "times": [],
            "variances": []
        },
        "5": {
            "times": [],
            "variances": []
        },
        "6": {
            "times": [],
            "variances": []
        },
    }
    res["gpromd"] = {
        "1": {
            "times": [],
            "variances": [],
            "logsize": []
        },
        "2": {
            "times": [],
            "variances": []
        },
        "3": {
            "times": [],
            "variances": []
        },
        "4": {
            "times": [],
            "variances": []
        },
        "5": {
            "times": [],
            "variances": []
        },
        "6": {
            "times": [],
            "variances": []
        },
    }


    return res
def getDatas():
    data = resStructures()
    for q in [1, 2, 3, 4]:
        file = f'{os.getcwd()}/newRes/PMRLIN2/results/gprom_capPq{q}_p1_res.txt'
        allp1 = getAllPOSTGRESQL(file)
        print(f'len of allp1: {len(allp1)}, allp1: {allp1}')
        med = sta.median(allp1)
        var = sta.variance(allp1)
        data['gpromp']["1"]["times"].append(med)
        data['gpromp']["1"]["variances"].append(var)

        file = f'{os.getcwd()}/newRes/PMRLIN2/results/gprom_capPq{q}_p3_res.txt'
        allp3 = getAllPOSTGRESQL(file)


        print(f'len of allp3: {len(allp3)}, allp3: {allp3}')
        assert len(allp3) == 10, f"Expected 20 execution times in file {file}, but found {len(allp3)}. Please check the file format."

        allp3 = [allp3[i]  + allp3[i + 1] for i in range(0, len(allp3), 2)]
        print(f'len of allp3 after summing pairs: {len(allp3)}, allp3: {allp3}')
        med = sta.median(allp3)
        var = sta.variance(allp3)
        data['gpromp']["3"]["times"].append(med)
        data['gpromp']["3"]["variances"].append(var)
        file = f'{os.getcwd()}/newRes/PMRLIN2/results/gprom_capPq{q}_p5_res.txt'

        allp5 = getAllPOSTGRESQL(file)
        print(f'len of allp5: {len(allp5)}, allp5: {allp5}')
        med = sta.median(allp5)
        var = sta.variance(allp5)
        data['gpromp']["5"]["times"].append(med)
        data['gpromp']["5"]["variances"].append(var)

        file = f'{os.getcwd()}/newRes/PMRLIN2/results/gprom_capDq{q}_p1_res.txt'
        allp1d = getAllDUCK(file)
        print(f'len of allp1d: {len(allp1d)}, allp1d: {allp1d}')
        med = sta.median(allp1d)
        var = sta.variance(allp1d)
        data['gpromd']["1"]["times"].append(med)
        data['gpromd']["1"]["variances"].append(var)

        file = f'{os.getcwd()}/newRes/PMRLIN2/results/gprom_capDq{q}_p3_res.txt'
        allp3d = getAllDUCK(file)
        print(f'len of allp3d: {len(allp3d)}, allp3d: {allp3d}')
        assert len(allp3d) == 10, f"Expected 20 execution times in file {file}, but found {len(allp3d)}. Please check the file format."
        allp3d = [allp3d[i]  + allp3d[i + 1] for i in range(0, len(allp3d), 2)]
        print(f'len of allp3d after summing pairs: {len(allp3d)}, allp3d: {allp3d}')
        med = sta.median(allp3d)
        var = sta.variance(allp3d)
        data['gpromd']["3"]["times"].append(med)
        data['gpromd']["3"]["variances"].append(var)

        file = f'{os.getcwd()}/newRes/PMRLIN2/results/gprom_capDq{q}_p5_res.txt'
        allp5d = getAllDUCK(file)
        print(f'len of allp5d: {len(allp5d)}, allp5d: {allp5d}')
        med = sta.median(allp5d)
        var = sta.variance(allp5d)
        data['gpromd']["5"]["times"].append(med)
        data['gpromd']["5"]["variances"].append(var)
        print('\n\n\n\n\n\n')
    with open(f'{os.getcwd()}/zackups/sf1/PMRLIN2_gprom.json', 'w') as fff:
        json.dump(data, fff, indent=4)
if __name__ == "__main__":
    os.makedirs(f'{os.getcwd()}/zackups/sf1', exist_ok=True)
    getDatas()