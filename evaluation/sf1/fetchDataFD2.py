import os
import statistics as sta
import re
import json
from utils import fileUtils as f_util
from utils import resultUtils as r_util
from utils import plotUtils as p_util
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
FIG_HEIGHT = 5.7
FIG_WIDTH1 = 13
FIG_WIDTH2 = 6
FONT_SIZE = 30
LINE_WIDTH = 2
INCREASE_WIDTH = 1.4
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
def getAllDucks(infile):
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
    return times
def getAllPosts(infile):
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
            times.append(float(timeValue) / 1000)
    return times

def getData(whatPMFD):
    data = {
        'gp': {
            'res' :{

            },
            'map': {

            }
        },
        'gd': {
            'res':{

            },
            'map': {

            }
        },
        'pr': {
            'res': {

            },
            'map': {

            }
        },
        'sp' : {
            'res': {

            },
            'map': {

            }

        },
        'smd' : {
            'res': {
                
            },
            'map': {
                
            }
        }
    }
    gd = getAllDucks(f'{os.getcwd()}/newRes/{whatPMFD}/results/gprom_capDq1_dt_res.txt')
    print(f'{whatPMFD} \n\n gd all: {len(gd)} \n\n {gd}\n\n\n\n')
    gdRSingle = gd[2::8]
    gdRp1 = gd[3::8]
    gdRp5 = gd[4::8]
    gdMSingle = gd[5::8]
    gdMp1 = gd[6::8]
    gdMp5 = gd[7::8]

    gdRSingleMed = sta.median(gdRSingle)
    gdRp1Med = sta.median(gdRp1)
    gdRp5Med = sta.median(gdRp5)
    gdMSingleMed = sta.median(gdMSingle)
    gdMp1Med = sta.median(gdMp1)
    gdMp5Med = sta.median(gdMp5)

    data['gd']['res']['RSingle'] = gdRSingleMed
    data['gd']['res']['Rp1'] = gdRp1Med
    data['gd']['res']['Rp5'] = gdRp5Med
    data['gd']['map']['MSingle'] = gdMSingleMed
    data['gd']['map']['Mp1'] = gdMp1Med
    data['gd']['map']['Mp5'] = gdMp5Med


    # print(f'gdRSingle: {gdRSingle}')
    # print(f'gdRp1: {gdRp1}')
    # print(f'gdRp5: {gdRp5}')
    # print(f'gdMSingle: {gdMSingle}')
    # print(f'gdMp1: {gdMp1}')
    # print(f'gdMp5: {gdMp5}')
    gp = getAllPosts(f'{os.getcwd()}/newRes/{whatPMFD}/results/gprom_capPq1_dt_res.txt')
    print(f'{whatPMFD} \n\n gd all: {len(gp)} \n\n {gp}\n\n\n\n')

    gpRSingle = gp[2::8]
    gpRp1 = gp[3::8]
    gpRp5 = gp[4::8]
    gpMSingle = gp[5::8]
    gpMp1 = gp[6::8]
    gpMp5 = gp[7::8]

    gpRSingleMed = sta.median(gpRSingle)
    gpRp1Med = sta.median(gpRp1)
    gpRp5Med = sta.median(gpRp5)
    gpMSingleMed = sta.median(gpMSingle)
    gpMp1Med = sta.median(gpMp1)
    gpMp5Med = sta.median(gpMp5)

    data['gp']['res']['RSingle'] = gpRSingleMed
    data['gp']['res']['Rp1'] = gpRp1Med
    data['gp']['res']['Rp5'] = gpRp5Med
    data['gp']['map']['MSingle'] = gpMSingleMed
    data['gp']['map']['Mp1'] = gpMp1Med
    data['gp']['map']['Mp5'] = gpMp5Med


    # print(f'gpRSingle: {gpRSingle}')
    # print(f'gpRp1: {gpRp1}')
    # print(f'gpRp5: {gpRp5}')
    # print(f'gpMSingle: {gpMSingle}')
    # print(f'gpMp1: {gpMp1}')
    # print(f'gpMp5: {gpMp5}')

    pr1 = getAllPosts(f'{os.getcwd()}/newRes/{whatPMFD}/results/provsql_capPq1_p2_res.txt')
    print(f'{whatPMFD} \n\n pr1 all: {len(pr1)} \n\n {pr1}\n\n\n\n')

    pr1Med = sta.median(pr1)
    pr2 = getAllPosts(f'{os.getcwd()}/newRes/{whatPMFD}/results/provsql_capPq1_p4_res.txt')
    print(f'{whatPMFD} \n\n pr2 all: {len(pr2)} \n\n {pr2}\n\n\n\n')
    pr2Med = sta.median(pr2)

    data['pr']['res']['p2'] = pr1Med
    data['pr']['res']['p4'] = pr2Med


    pr3 = getAllPosts(f'{os.getcwd()}/newRes/{whatPMFD}/results/provsql_capPq1_p6_res.txt')
    print(f'{whatPMFD} \n\n pr3 all: {len(pr3)} \n\n {pr3}\n\n\n\n')

    prR3Single = pr3[0::6]
    prR3p1 = pr3[1::6]
    prR3p5 = pr3[2::6]

    prM3Single = pr3[3::6]
    prM3p1 = pr3[4::6]
    prM3p5 = pr3[5::6]

    prR3SingleMed = sta.median(prR3Single)
    prR3p1Med = sta.median(prR3p1)
    prR3p5Med = sta.median(prR3p5)

    prM3SingleMed = sta.median(prM3Single)
    prM3p1Med = sta.median(prM3p1)
    prM3p5Med = sta.median(prM3p5)

    data['pr']['res']['R3Single'] = prR3SingleMed
    data['pr']['res']['R3p1'] = prR3p1Med
    data['pr']['res']['R3p5'] = prR3p5Med
    data['pr']['map']['M3Single'] = prM3SingleMed
    data['pr']['map']['M3p1'] = prM3p1Med
    data['pr']['map']['M3p5'] = prM3p5Med

    # print(f'pr1: {pr1}')
    # print(f'pr2: {pr2}')
    # print(f'prR3Single: {prR3Single}')
    # print(f'prR3p1: {prR3p1}')
    # print(f'prR3p5: {prR3p5}')
    # print(f'prM3Single: {prM3Single}')
    # print(f'prM3p1: {prM3p1}')
    # print(f'prM3p5: {prM3p5}')

    sp1 = getAllPosts(f'{os.getcwd()}/newRes/{whatPMFD}/results/sp_capPq1_p1_res.txt')
    sp1Med = sta.median(sp1)
    sp2 = getAllPosts(f'{os.getcwd()}/newRes/{whatPMFD}/results/sp_capPq1_p2_res.txt')
    sp2Med = sta.median(sp2)
    sp4 = getAllPosts(f'{os.getcwd()}/newRes/{whatPMFD}/results/sp_capPq1_p4_res.txt')
    sp4Med = sta.median(sp4)

    sp6 = getAllPosts(f'{os.getcwd()}/newRes/{whatPMFD}/results/sp_capPq1_p6_res.txt')
    print(f'len sp6: {len(sp6)}\n\n DATA:{sp6}')
    spR6Single = sp6[0::6]
    spR6p1 = sp6[1::6]
    spR6p5 = sp6[2::6]
    spR6SingleMed = sta.median(spR6Single)
    spR6p1Med = sta.median(spR6p1)
    spR6p5Med = sta.median(spR6p5)

    spM6Single = sp6[3::6]
    spM6p1 = sp6[4::6]
    spM6p5 = sp6[5::6]
    spM6SingleMed = sta.median(spM6Single)
    spM6p1Med = sta.median(spM6p1)
    spM6p5Med = sta.median(spM6p5)

    data['sp']['res']['p1'] = sp1Med
    data['sp']['res']['p2'] = sp2Med
    data['sp']['res']['p4'] = sp4Med
    data['sp']['res']['R6Single'] = spR6SingleMed
    data['sp']['res']['R6p1'] = spR6p1Med
    data['sp']['res']['R6p5'] = spR6p5Med
    data['sp']['map']['M6Single'] = spM6SingleMed
    data['sp']['map']['M6p1'] = spM6p1Med
    data['sp']['map']['M6p5'] = spM6p5Med


    # -- smd
    smd1 = getAllDucks(f'{os.getcwd()}/newRes/{whatPMFD}/results/smd_capDq1_p1_res.txt')
    print(f'{whatPMFD}: SMD p1: {len(smd1)}\n\n {smd1}')
    smd1Med= sta.median(smd1)
    smd2 = getAllDucks(f'{os.getcwd()}/newRes/{whatPMFD}/results/smd_capDq1_p2_res.txt')
    smd2Med = sta.median(smd2)
    print(f'{whatPMFD}: SMD p2: {len(smd2)}\n\n {smd2}')
    smd4 = getAllDucks(f'{os.getcwd()}/newRes/{whatPMFD}/results/smd_capDq1_p4_res.txt')
    print(f'{whatPMFD}: SMD p4: {len(smd4)}\n\n {smd4}')
    smd4Med = sta.median(smd4)
    smd6 = getAllDucks(f'{os.getcwd()}/newRes/{whatPMFD}/results/smd_capDq1_p6_res.txt')
    print(f'{whatPMFD}: SMD p6: {len(smd6)}\n\n {smd6}')

    smdR6Single = smd6[0::6]
    smdR6p1 = smd6[1::6]
    smdR6p5 = smd6[2::6]
    smdR6SingleMed = sta.median(smdR6Single)
    smdR6p1Med = sta.median(smdR6p1)
    smdR6p5Med = sta.median(smdR6p5)

    smdM6Single = smd6[3::6]
    smdM6p1 = smd6[4::6]
    smdM6p5 = smd6[5::6]
    smdM6SingleMed = sta.median(smdM6Single)
    smdM6p1Med = sta.median(smdM6p1)
    smdM6p5Med = sta.median(smdM6p5)
    
    data['smd']['res']['p1'] = smd1Med
    data['smd']['res']['p2'] = smd2Med
    data['smd']['res']['p4'] = smd4Med
    data['smd']['res']['R6Single'] = smdR6SingleMed
    data['smd']['res']['R6p1']     = smdR6p1Med
    data['smd']['res']['R6p5']     = smdR6p5Med
    data['smd']['map']['M6Single'] = smdM6SingleMed
    data['smd']['map']['M6p1']     = smdM6p1Med
    data['smd']['map']['M6p5']     = smdM6p5Med



    with open(f'{os.getcwd()}/zackups/sf1/{whatPMFD}.json', 'w') as fff:
        json.dump(data, fff, indent=4)
    if True:
        return data

    print(f'sp1: {sp1}')
    print(f'sp2: {sp2}')
    print(f'spR6Single: {spR6Single}')
    print(f'spR6p1: {spR6p1}')
    print(f'spR6p5: {spR6p5}')
    print(f'spM6Single: {spM6Single}')
    print(f'spM6p1: {spM6p1}')
    print(f'spM6p5: {spM6p5}')

    Slogsize = 228016128 /1024/1024
    Sspp1 = 32768 /1024/1024
    Sspp2 = 262144 / 1024/1024
    Sprc = (131072 + 65536) / 1024 / 1024



def plot(whatPMFD, Y_FLOOR = 0, Y_FLOOR2 = 0, Y_INCREASE_RATIO = 1):
    data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{whatPMFD}.json')
    gdRp5 = data['gd']['res']['Rp5']
    gdMp5 = data['gd']['map']['Mp5']

    gpRp5 = data['gp']['res']['Rp5']
    gpMp5 = data['gp']['map']['Mp5']


    prC = data['pr']['res']['p2']
    prQ = data['pr']['res']['p4']
    prRp5 = data['pr']['res']['R3p5']
    prMp5 = data['pr']['map']['M3p5']

    spC1 = data['sp']['res']['p1']
    spC2 = data['sp']['res']['p2']

    spQ = data['sp']['res']['p4']

    spRp5 = data['sp']['res']['R6p5']
    spMp5 = data['sp']['map']['M6p5']

    smdC1 = data['smd']['res']['p1']
    smdC2 = data['smd']['res']['p2']

    smdQ = data['smd']['res']['p4']
    smdRp5 = data['smd']['res']['R6p5']
    smdMp5 = data['smd']['map']['M6p5']

    if whatPMFD == 'PMFD2':
        SspC = 217.476 + 0.281
        SspQ = 0.262

        SprC = 319.07 + 0.125
        SprQ = 0.065

        SsmdC = 14.7
        SsmdQ = 0.5

    elif whatPMFD == 'PMFD3':
        SspC = 228.02 + 296.75
        SspQ = 174.59

        SprC = 340.40 + 244
        SprQ = 192

        SsmdC = 13.5
        SsmdQ = 20.5





    # endtoend
    title = ['fetchRes', 'fetchMapping']
    print("########################################\n\n")
    print(f'gprom: {gpRp5}')
    print(f'sp: {spC1 + spC2 + spQ + spRp5}  - c:{spC1}+{spC2}, q: {spQ}, r:{spRp5}')
    print(f'pr: {prC + prQ + prRp5} -- c{prC}, q: {prQ}, r: {prRp5}')
    print(f'gd: {gdRp5}')

    print("########################################\n\n")
    # Y_FLOOR = 3*1e-4
    for id in range(2):
        fig, axes = plt.subplots(2, 4, figsize=(FIG_WIDTH1 * 1.4, FIG_HEIGHT), sharey='row', gridspec_kw={ 'height_ratios': [3, 1], 'hspace': 0.0, 'wspace': 0 })
        for aid in range(4):
            ax = axes[0][aid]
            # endtoend
            if aid == 0:
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
                if id == 0:
                    ax.bar(offsets[0], gpRp5, width=0.12, label='GProM-P', bottom = Y_FLOOR, color=p_util.clrgp)
                    ax.bar(offsets[1], spC1 + spC2 + spQ + spRp5, width=0.12, label='GProM-P', bottom = Y_FLOOR, color=p_util.clrsp)
                    ax.bar(offsets[2], prC + prQ + prRp5, width=0.12, label='GProM-D', bottom = Y_FLOOR, color=p_util.clrpr)
                    ax.bar(offsets[3], gdRp5, width=0.12, label='GProM-D', bottom = Y_FLOOR, color=p_util.clrgd)
                    ax.bar(offsets[4], smdC1 + smdC2 + smdQ + smdRp5, width = 0.12, label = 'SMD', bottom = Y_FLOOR, color = p_util.clrsd)
                    ax.text( 0.25, 0.94, r'$PostgreSQL$', ha='center', fontweight='bold', transform=ax.transAxes, color='red', fontsize=FONT_SIZE / 1.5)
                    ax.grid(True, which='major', axis='y', linestyle='--')
                    ax.set_axisbelow(True)
                elif id == 1:
                    ax.bar(offsets[0], gpMp5, width=0.12, label='GProM-P', bottom = Y_FLOOR, color=p_util.clrgp)
                    ax.bar(offsets[1], spC1 + spC2 + spQ + spMp5, width=0.12, label='GProM-P', bottom = Y_FLOOR, color=p_util.clrsp)
                    ax.bar(offsets[2], prC + prQ + prMp5, width=0.12, label='GProM-D', bottom = Y_FLOOR, color=p_util.clrpr)
                    ax.bar(offsets[3], gdMp5, width=0.12, label='GProM-D', bottom = Y_FLOOR, color=p_util.clrgd)
                    ax.bar(offsets[4], smdC1 + smdC2 + smdQ + smdMp5, width = 0.12, label = 'SMD', bottom = Y_FLOOR, color = p_util.clrsd)
                    ax.text( 0.25, 0.93, r'$PostgreSQL$', ha='center', fontweight='bold', transform=ax.transAxes, color='red', fontsize=FONT_SIZE / 1.5)
                ax.grid(True, which='major', axis='y', linestyle='--')
                ax.set_axisbelow(True)

                ax.text( 0.81, 0.93, r'$DuckDB$', ha='center', fontweight='bold', transform=ax.transAxes, color='red', fontsize=FONT_SIZE / 1.5)
                split_post = (offsets[2] + offsets[3]) / 2
                ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
                ax.set_yscale('log')
                ax.set_xticks([])
                current_ymin, current_ymax = ax.get_ylim()
                ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)


            elif aid == 1:
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
                ax.bar(offsets[0], spC1 + spC2, width=0.12, label='SQLPROV', bottom = Y_FLOOR, color=p_util.clrsp)
                ax.text(offsets[0], spC1 + spC2 + Y_FLOOR, s = f'{int(spC1/(spC1 + spC2) * 100)}%', ha='center', va = 'bottom',fontsize=FONT_SIZE -8, color = 'blue')
                ax.bar(offsets[1], prC, width = 0.12, label = 'PROVSQL', bottom = Y_FLOOR, color=p_util.clrpr)

                ax.bar(offsets[2], smdC1 + smdC2, width=0.12, label='SMD', bottom = Y_FLOOR, color=p_util.clrsd)
                ax.text(offsets[2], smdC1 + smdC2 + Y_FLOOR, s = f'{int(smdC1/(smdC1 + smdC2) * 100)}%', ha='center', va = 'bottom',fontsize=FONT_SIZE -8, color = 'blue')


                ax.grid(True, which='major', axis='y', linestyle='--')
                ax.set_axisbelow(True)

                ax.text( 0.25, 0.93, r'$PostgreSQL$', ha='center', fontweight='bold', transform=ax.transAxes, color='red', fontsize=FONT_SIZE / 1.5)
                ax.text( 0.84, 0.93, r'$DuckDB$', ha='center', fontweight='bold', transform=ax.transAxes, color='red', fontsize=FONT_SIZE / 1.5)
                split_post = (offsets[1] + offsets[2]) / 2
                ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
                ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)

            elif aid == 2:
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
                ax.bar(offsets[0], spQ, width=0.12, label='SQLPROV', bottom = Y_FLOOR, color=p_util.clrsp)
                ax.bar(offsets[1], prQ, width = 0.12, label = 'PROVSQL', bottom = Y_FLOOR, color=p_util.clrpr)
                ax.bar(offsets[2], smdQ, width = 0.12, label = 'SMD', bottom = Y_FLOOR, color=p_util.clrsd)
                ax.text( 0.25, 0.93, r'$PostgreSQL$', ha='center', fontweight='bold', transform=ax.transAxes, color='red', fontsize=FONT_SIZE / 1.5)
                ax.text( 0.84, 0.93, r'$DuckDB$', ha='center', fontweight='bold', transform=ax.transAxes, color='red', fontsize=FONT_SIZE / 1.5)
                split_post = (offsets[1] + offsets[2]) / 2
                ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)

                ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
                ax.grid(True, which='major', axis='y', linestyle='--')
                ax.set_axisbelow(True)
            elif aid == 3:
                if id == 0:
                    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
                    ax.bar(offsets[0], spRp5, width=0.12, label='SQLPROV', bottom = Y_FLOOR, color=p_util.clrsp)
                    ax.bar(offsets[1], prRp5, width=0.12, label='PROVSQL', bottom = Y_FLOOR, color=p_util.clrpr)
                    ax.bar(offsets[2], smdRp5, width=0.12, label='SMD', bottom = Y_FLOOR, color=p_util.clrsd)

                elif id == 1:
                    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
                    ax.bar(offsets[0], spMp5, width=0.12, label='SQLPROV', bottom = Y_FLOOR, color=p_util.clrsp)
                    ax.bar(offsets[1], prMp5, width=0.12, label='PROVSQL', bottom = Y_FLOOR, color=p_util.clrpr)
                    ax.bar(offsets[2], smdMp5, width=0.12, label='SMD', bottom = Y_FLOOR, color=p_util.clrsd)

                ax.text( 0.25, 0.93, r'$PostgreSQL$', ha='center', fontweight='bold', transform=ax.transAxes, color='red', fontsize=FONT_SIZE / 1.5)
                ax.text( 0.84, 0.93, r'$DuckDB$', ha='center', fontweight='bold', transform=ax.transAxes, color='red', fontsize=FONT_SIZE / 1.5)
                split_post = (offsets[1] + offsets[2]) / 2
                ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)

                ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
                ax.grid(True, which='major', axis='y', linestyle='--')
                ax.set_axisbelow(True)
        # -- storage overhead
        for aid in range(4):
            if aid == 0:
                ax = axes[1][aid]
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
                ax.bar(offsets[0], 0.0, width=0.12, label='GProM-P', bottom = Y_FLOOR2, color=p_util.clrsp)
                ax.bar(offsets[1], SspC + SspQ, width=0.12, label='sqlprov', bottom = Y_FLOOR2, color=p_util.clrsp)
                ax.bar(offsets[2], SprC + SprQ, width=0.12, label='provsql', bottom = Y_FLOOR2, color=p_util.clrpr)
                ax.bar(offsets[3], 0.0, width=0.12, label='GProM-D', bottom = Y_FLOOR2, color=p_util.clrgd)
                ax.bar(offsets[4], SsmdC + SsmdQ, width=0.12, label='SMD', bottom = Y_FLOOR2, color=p_util.clrsd)


                ax.set_yscale('log')
                ax.set_xticks([])
                split_post = (offsets[2] + offsets[3]) / 2
                ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)


                ax.set_xlabel('End-to-end', fontsize=FONT_SIZE)
            elif aid == 1:
                ax = axes[1][aid]
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
                ax.bar(offsets[0], SspC, width=0.12, label='sqlprov', bottom = Y_FLOOR2, color=p_util.clrsp)
                ax.bar(offsets[1], SprC, width=0.12, label='provsql', bottom = Y_FLOOR2, color=p_util.clrpr)
                ax.bar(offsets[2], SsmdC, width=0.12, label='SMD', bottom = Y_FLOOR2, color=p_util.clrsd)

                split_post = (offsets[1] + offsets[2]) / 2
                ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
 
                
                ax.set_xlabel('Capture', fontsize=FONT_SIZE)
                ax.set_xticks([])
                ax.set_yscale('log')
            elif aid == 2:
                ax = axes[1][aid]
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
                ax.bar(offsets[0], SspQ, width=0.12, label='sqlprov', bottom = Y_FLOOR2, color=p_util.clrsp)
                ax.bar(offsets[1], SprQ, width=0.12, label='provsql', bottom = Y_FLOOR2, color=p_util.clrpr)
                ax.bar(offsets[2], SsmdQ, width=0.12, label='SMD', bottom = Y_FLOOR2, color=p_util.clrsd)
                split_post = (offsets[1] + offsets[2]) / 2
                ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
 
                ax.set_xlabel('Query', fontsize=FONT_SIZE)
                ax.set_xticks([])
                ax.set_yscale('log')
            elif aid == 3:
                ax = axes[1][aid]
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)

                split_post = (offsets[1] + offsets[2]) / 2
                ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)

                for b in range(3):
                    ax.bar(offsets[b], 0.0, width=0.12 )

                if id == 0:
                    ax.set_xlabel('Fetch Result', fontsize=FONT_SIZE)
                elif id == 1:
                    ax.set_xlabel('Result & Lineage', fontsize=FONT_SIZE)
                ax.set_xticks([])
                ax.set_yscale('log')
        for ax in axes.flatten():
            for spine in ax.spines.values():
                spine.set_edgecolor('black')
                spine.set_linewidth(LINE_WIDTH)

        axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
        axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
        axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
        axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)
        plt.tight_layout()
        if id ==0 :
            saveName = f'Fig_{whatPMFD}_{title[id]}'
        elif id == 1:
            saveName = f'Fig_{whatPMFD}_{title[id]}'
        plt.savefig(f'{os.getcwd()}/zackups/{saveName}_sf1.png', bbox_inches='tight')

if __name__ == "__main__":
    os.makedirs(f'{os.getcwd()}/zackups/sf1', exist_ok=True)
    aggD = getData('PMFD2')
    jinD = getData('PMFD3')

    # print(f'aggD: {aggD}')
    # print(f'jinD: {jinD}')
    plot('PMFD2', Y_FLOOR = 4 * 1e-4, Y_FLOOR2=4 * 1e-2, Y_INCREASE_RATIO = 1.9)
    plot('PMFD3', Y_FLOOR = 1.1 * 1e-2, Y_FLOOR2=10, Y_INCREASE_RATIO = 1.9)
