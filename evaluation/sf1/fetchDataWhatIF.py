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

isPR = True

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

def plot2(WHAT = 'WhatIF', Y_FLOOR = 0, Y_FLOOR2 = 0, Y_INCREASE_RATIO = 1):
    gpromD = []
    gpromP = []

    for q in range(1, 8, 1):
        time = getAllDucks(f'{os.getcwd()}/newRes/WhatIF/results/gprom_capDq{q}_res.txt')
        gpromD.append(sta.median(time))
        time = 0.0
        time = getAllPosts(f'{os.getcwd()}/newRes/WhatIF/results/gprom_capPq{q}_res.txt')
        gpromP.append(sta.median(time))
        time = 0.0

    smd = []
    for q in range(1, 10, 1):
        time = getAllDucks(f'{os.getcwd()}/newRes/WhatIF/results/smd_capDq1_p{q}_res.txt')
        smd.append(sta.median(time))
        time = 0.0

    prov = []
    for q in range(1, 7, 1):
        time = getAllPosts(f'{os.getcwd()}/newRes/WhatIF/results/provsql_capPq{q}_res.txt')
        prov.append(sta.median(time))

    print(f'GD: {gpromD}')
    print(f'GP: {gpromP}')
    print(f'SMD: {smd}')
    print(f'PROV: {prov}')

    BarNumbers = 4
    barWidth = (0.12 / (BarNumbers / 5))
    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=BarNumbers)
    fig, axes = plt.subplots( 2, 3, figsize=(FIG_WIDTH1 * INCREASE_WIDTH, FIG_HEIGHT), sharey='row', gridspec_kw={ 'height_ratios': [3, 1], 'hspace': 0.0, 'wspace': 0 })


    gPcap = gpromP[0]
    gDcap = gpromD[0]
    smdCap = smd[0] + smd[1] + smd[2]

    for id in range(3):
        ax = axes[0][id]
        barPos = 0
        # gprom post:
        ax.bar(offsets[barPos], gPcap + gpromP[id + 4], width = barWidth, bottom = Y_FLOOR, label = 'GProm-p', color = p_util.clrgp)
        ax.text(offsets[barPos], gPcap + gpromP[id + 4], s = f'{int(gpromP[id + 4]/(gPcap + gpromP[id + 4]) * 100)}%', ha = 'center', va = 'bottom', fontsize = FONT_SIZE - 8, color = 'blue' )

        barPos += 1
        # provsql
        ax.bar(offsets[barPos], prov[id + 3], width = barWidth, bottom = Y_FLOOR, label = 'prov', color = p_util.clrpr)
        barPos += 1

        # gprom duck:
        ax.bar(offsets[barPos], gDcap + gpromD[id + 4], width = barWidth, bottom = Y_FLOOR, label = 'GProm-p', color = p_util.clrgp)
        ax.text(offsets[barPos], gDcap + gpromD[id + 4], s = f'{int(gpromD[id + 4]/(gDcap + gpromD[id + 4]) * 100)}%', ha = 'center', va = 'bottom', fontsize = FONT_SIZE - 8, color = 'blue' )
        barPos += 1


        # smd
        ax.bar(offsets[barPos], smdCap + smd[id + 6], width = barWidth, bottom = Y_FLOOR, label = 'smd', color = p_util.clrsd)
        ax.text(offsets[barPos], smdCap + smd[id + 6], s = f'{int(smd[id + 6]/(smdCap + smd[id + 4]) * 100)}%', ha = 'center', va = 'bottom', fontsize = FONT_SIZE - 8, color = 'blue' )


        ax.grid(True, which='major', axis='y', linestyle='--')
        ax.set_axisbelow(True)
        # -- set ticks to None
        ax.set_xticks([])
        # -- set y scale to log
        ax.set_yscale('log')

        # -- line separator for postgreSQL and duckDB
        split_post = (offsets[1] + offsets[2]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
        current_ymin, current_ymax = ax.get_ylim()
        ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
        ax.text(
            0.25,
            0.93,
            r'$PostgreSQL$',
            ha='center',
            fontweight='bold',
            transform=ax.transAxes,
            color='red',
            fontsize=FONT_SIZE / 1.5
        )

        ax.text(
            0.81,
            0.93,
            r'$DuckDB$',
            ha='center',
            fontweight='bold',
            transform=ax.transAxes,
            color='red',
            fontsize=FONT_SIZE / 1.5
        )

        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)
    # plt.show()
        # STORAGE
    gns = ['1% Data Deleted', '10% Data Deleted', '50% Data Deleted']
    SgP = [50.4, 50.4, 50.4]
    SgD = [8,8,8]
    Ssmd = [26.65, 26.65, 26.65]
    Sprov = [139.688, 139.699, 139.688]
    for id in range(3):
        ax = axes[1][id]
        barPos = 0
        # gprom post:
        ax.bar(offsets[barPos], SgP[id], width = barWidth, bottom = Y_FLOOR, label = 'GProm-p', color = p_util.clrgp)

        barPos += 1
        # provsql
        ax.bar(offsets[barPos], Sprov[id], width = barWidth, bottom = Y_FLOOR, label = 'prov', color = p_util.clrpr)
        barPos += 1

        # gprom duck:
        ax.bar(offsets[barPos], SgD[id], width = barWidth, bottom = Y_FLOOR, label = 'GProm-p', color = p_util.clrgp)
        barPos += 1


        # smd
        ax.bar(offsets[barPos], Ssmd[id], width = barWidth, bottom = Y_FLOOR, label = 'smd', color = p_util.clrsd)


        ax.grid(True, which='major', axis='y', linestyle='--')
        ax.set_axisbelow(True)
        # -- set ticks to None
        ax.set_xticks([])
        # -- set y scale to log
        ax.set_yscale('log')

        # -- line separator for postgreSQL and duckDB
        split_post = (offsets[1] + offsets[2]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
        current_ymin, current_ymax = ax.get_ylim()
        ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
        ax.set_xlabel(f'{gns[id]}', fontsize=FONT_SIZE)
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)
    axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
    axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
    axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)
    plt.tight_layout()
    plt.savefig(f'{os.getcwd()}/zackups/Fig_whatif_sf1.png',
                bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    os.makedirs(f'{os.getcwd()}/zackups/sf1', exist_ok=True)
    plot2(Y_INCREASE_RATIO=1.8)
