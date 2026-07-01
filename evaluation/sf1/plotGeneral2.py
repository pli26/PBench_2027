from utils import fileUtils as f_util
from utils import resultUtils as r_util
from utils import plotUtils as p_util
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

FIG_HEIGHT = 5.7
FIG_WIDTH1 = 13
FIG_WIDTH2 = 6
FONT_SIZE = 30
LINE_WIDTH = 2
# TODO: plot.grid()



SHOW_GRID = True
PLOTTED_LEGEND = True

def getHowManyBars(systems):
    post = 0
    duck = 0
    if "gprom" in systems:
        post += 1
        duck += 1

    if "sqlprov" in systems:
        post += 1

    if "provsql" in systems:
        post += 1

    if "smokedduck" in systems:
        duck += 1

    return post, duck
def plot(sf,
         whichbench: list,
         benchQOrders: list,
         saveName: str,
         systems=['gprom', 'sqlprov', 'provsql', 'smokedduck'],
         subfigNumTitles: list = None,
         MarkerSize=20,
         Y_FLOOR=1e-3,
         Y_INCREASE_RATIO=1.0,
         Y_FLOOR2=1e-3,
         INCREASE_WIDTH=1.4,
         xticks: list = None,
         plot_all_phase = False,
         SECOND_SYS_START_POST = 0.81):

    # -- gprom
    gpT = []
    gdT = []

    gdS = []
    gpS = []

    # -- sqlprov
    spT1 = []
    spT2 = []
    spT = []
    spS = []

    # -- provsql
    prT = []
    prS = []

    # -- smokedduck
    sdT1 = []
    sdT2 = []
    sdT = []
    sdS = []

    # ----- Postgresql
    posts = []
    # ----- duckdb
    ducks = []

    if 'gprom' in systems:
        # -- time
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            gpT.append(dataT['gprom']['p']['times'][benchQOrders[index]])
            gdT.append(dataT['gprom']['d']['times'][benchQOrders[index]])

        # -- storage
        for index in range(len(whichbench)):
            gpS.append(0.0)
            gdS.append(0.0)
    if 'sqlprov' in systems:
        # -- time
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            spT1.append(dataT['sqlprov']['1']['times'][benchQOrders[index]])
            spT2.append(dataT['sqlprov']['2']['times'][benchQOrders[index]])
            spT.append(spT1[-1] + spT2[-1])
        # -- storage
        for index in range(len(whichbench)):
            dataS = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}Storage.json')
            spS.append(dataS['sqlprov']['storage'][benchQOrders[index]])
    else:
        spT = [0.0 for _ in range(len(gpT))]
        spS = [0.0 for _ in range(len(gpT))]
    if 'smokedduck' in systems:
        # -- time
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            sdT1.append(dataT['smokedduck']['1']['times'][benchQOrders[index]])
            sdT2.append(dataT['smokedduck']['2']['times'][benchQOrders[index]])
            sdT.append(sdT1[-1] + sdT2[-1])
        # -- storage
        for index in range(len(whichbench)):
            dataS = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}Storage.json')
            sdS.append(dataS['smokedduck']['storage'][benchQOrders[index]])
    else:
        sdT = [0.0 for _ in range(len(gpT))]
        sdS = [0.0 for _ in range(len(gpT))]
    if 'provsql' in systems:
        # -- time
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            prT.append(dataT['provsql']['times'][benchQOrders[index]])
        # -- storage
        for index in range(len(whichbench)):
            dataS = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}Storage.json')
            prS.append(dataS['provsql']['storage'][benchQOrders[index]])
    else:
        prT = [0.0 for _ in range(len(gpT))]
        prS = [0.0 for _ in range(len(gpT))]

    if 'postgresql' in systems:
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            posts.append(dataT['postgresql']['times'][benchQOrders[index]])
    else:
        posts = [0.0 for _ in range(len(gpT))]

    if 'duckdb' in systems:
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            ducks.append(dataT['duckdb']['times'][benchQOrders[index]])
    else:
        ducks = [0.0 for _ in range(len(gpT))]

    BarNumbers = 0

    if 'gprom' in systems:
        BarNumbers += 2
    if 'sqlprov' in systems:
        BarNumbers += 1
    if 'provsql' in systems:
        BarNumbers += 1
    if 'smokedduck' in systems:
        BarNumbers += 1

    barWidth = (0.12 / (BarNumbers / 5))

    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=BarNumbers)
    fig, axes = plt.subplots( 2, len(subfigNumTitles), figsize=(FIG_WIDTH1 * INCREASE_WIDTH, FIG_HEIGHT), sharey='row', gridspec_kw={ 'height_ratios': [3, 1], 'hspace': 0.0, 'wspace': 0 })
    gns = subfigNumTitles

    leftBars = 0
    if 'gprom' in systems:
        leftBars += 1
    if 'sqlprov' in systems:
        leftBars += 1
    if 'provsql' in systems:
        leftBars += 1
    # Y_FLOOR = None
    # plot titmes

    (PN, DN) = getHowManyBars(systems)
    for id in range(len(subfigNumTitles)):
        print(
            f'gn: {subfigNumTitles}, gpT: {gpT[id]}, spT: {spT[id]}, prT: {prT[id]}, gdT: {gdT[id]}, sdT: {sdT[id]}, posts: {posts[id]}, ducks: {ducks[id]}')

        print(f'offset: {offsets[id]}, posts: {posts[id]}, ducks: {ducks[id]}')
        ax = axes[0][id]
        barPos = 0
        leftLineStart = 0
        if 'gprom' in systems:
            ax.bar(offsets[barPos], gpT[id], width=barWidth,
                   bottom=Y_FLOOR, label='GProM-P', color=p_util.clrgp)

            # ax.plot(offsets[barPos], posts[id], marker=p_util.postmarker, linewidth = LINE_WIDTH, linestyle = '--', color = p_util.clrpg)

            barPos += 1
        if 'sqlprov' in systems:
            if plot_all_phase:
                ax.bar(offsets[barPos], spT[id], width=barWidth, bottom=Y_FLOOR, label='SQLProv', color=p_util.clrsp)
                ax.text(offsets[barPos], spT[id], s=f'{int(spT1[id]/spT[id]*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
            else:
                ax.bar(offsets[barPos], spT1[id], width=barWidth,bottom = Y_FLOOR, label = 'SQLProv', color = p_util.clrsp)

            barPos += 1
        if 'provsql' in systems:
            ax.bar(offsets[barPos], prT[id], width=barWidth,
                   bottom=Y_FLOOR, label='ProvSQL', color=p_util.clrpr)
            barPos += 1
        LeftLineEnd = barPos - 1


        ax.hlines(y = posts[id], xmin = offsets[leftLineStart] - barWidth / 2, xmax = offsets[LeftLineEnd] + barWidth / 2, colors = p_util.clrpg, linestyles = '--', linewidth = LINE_WIDTH, label='PostgreSQL')


        RightLineStart = LeftLineEnd + 1
        if 'gprom' in systems:
            ax.bar(offsets[barPos], gdT[id], width=barWidth,
                   bottom=Y_FLOOR, label='GProM-D', color=p_util.clrgd)
            # ax.plot(offsets[barPos], ducks[id], marker=p_util.duckmarker, linewidth = LINE_WIDTH, linestyle = '--', color = p_util.clrdk)
            barPos += 1
        if 'smokedduck' in systems:
            if plot_all_phase:
                ax.bar(offsets[barPos], sdT[id], width=barWidth, bottom=Y_FLOOR, label='SmokedDuck', color=p_util.clrsd)
                ax.text(offsets[barPos], sdT[id], s=f'{int(sdT1[id]/sdT[id]*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
            else:
                ax.bar(offsets[barPos], sdT1[id], width=barWidth, bottom=Y_FLOOR, label='SmokedDuck', color=p_util.clrsd)

            barPos += 1
        RightLineEnd = barPos - 1
        ax.hlines(y = ducks[id], xmin = offsets[RightLineStart] - barWidth/ 2, xmax = offsets[RightLineEnd] + barWidth / 2, colors = p_util.clrdk, linestyles = '--', linewidth = LINE_WIDTH, label='DuckDB')

        # -- show grid
        if SHOW_GRID:
            ax.grid(True, which='major', axis='y', linestyle='--')
            ax.set_axisbelow(True)
        # -- set ticks to None
        ax.set_xticks([])
        # -- set y scale to log
        ax.set_yscale('log')

        # -- line separator for postgreSQL and duckDB
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)

        # -- text for postgreSQL and duckDB
        # -- y increase to fit the text
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
            SECOND_SYS_START_POST,
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
    # -- plot storage
    for id in range(len(subfigNumTitles)):
        ax = axes[1][id]
        barPos = 0
        if 'gprom' in systems:
            ax.bar(offsets[barPos], gpS[id], width=barWidth,
                   bottom=Y_FLOOR2, label='GProM-P', color=p_util.clrgp)
            barPos += 1
        if 'sqlprov' in systems:
            ax.bar(offsets[barPos], spS[id], width=barWidth,
                   bottom=Y_FLOOR2, label='SQLProv', color=p_util.clrsp)
            barPos += 1
        if 'provsql' in systems:
            ax.bar(offsets[barPos], prS[id], width=barWidth,
                   bottom=Y_FLOOR2, label='ProvSQL', color=p_util.clrpr)
            barPos += 1
        if 'gprom' in systems:
            ax.bar(offsets[barPos], gdS[id], width=barWidth,
                   bottom=Y_FLOOR2, label='GProM-D', color=p_util.clrgd)
            barPos += 1
        if 'smokedduck' in systems:
            ax.bar(offsets[barPos], sdS[id], width=barWidth,
                   bottom=Y_FLOOR2, label='SmokedDuck', color=p_util.clrsd)
            barPos += 1
        if xticks is not None:
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticks, fontsize=FONT_SIZE)
        else:
            ax.set_xticks([])
        ax.set_yscale('log')

        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)

        # ax.invert_yaxis()
        ax.set_xlabel(f'{gns[id]}', fontsize=FONT_SIZE)
        # -- set edge color and line width for all spines
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)
    axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
    axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
    axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)
    plt.tight_layout()
    plt.savefig(f'{os.getcwd()}/zackups/{saveName}_{sf}.png',
                bbox_inches='tight')
    plt.close()

def plot2(sf,
          whichbench: list,
          benchQOrders: list,
          saveName: str,
          systems=['gprom', 'sqlprov', 'provsql', 'smokedduck'],
          subfigNumTitles: list = None,
          MarkerSize=20,
          Y_FLOOR=1e-3,
          Y_INCREASE_RATIO=1.0,
          Y_FLOOR2=1e-3,
          xticks: list = None):

    gps = []
    gds = []
    prs = []
    sps = []
    sp1s = []
    sp2s = []
    sd1s = []
    sd2s = []
    sds = []

    posts = []
    ducks = []
    if 'gprom' in systems:
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            gps.append(dataT['gprom']['p']['times'][benchQOrders[index]])
            gds.append(dataT['gprom']['d']['times'][benchQOrders[index]])
    if 'sqlprov' in systems:
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            sp1s.append(dataT['sqlprov']['1']['times'][benchQOrders[index]])
            sp2s.append(dataT['sqlprov']['2']['times'][benchQOrders[index]])
            sps.append(sp1s[-1] + sp2s[-1])
    if 'smokedduck' in systems:
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            sd1s.append(dataT['smokedduck']['1']['times'][benchQOrders[index]])
            sd2s.append(dataT['smokedduck']['2']['times'][benchQOrders[index]])
            sds.append(sd1s[-1] + sd2s[-1])
    if 'provsql' in systems:
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            prs.append(dataT['provsql']['times'][benchQOrders[index]])
    if 'postgresql' in systems:
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            posts.append(dataT['postgresql']['times'][benchQOrders[index]])
    if 'duckdb' in systems:
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            ducks.append(dataT['duckdb']['times'][benchQOrders[index]])
    gpS = []
    gdS = []
    prS = []
    spS = []
    sdS = []
    if 'gprom' in systems:
        for index in range(len(whichbench)):
            dataS = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}Storage.json')
            gpS.append(0.0)
            gdS.append(0.0)
    if 'sqlprov' in systems:
        for index in range(len(whichbench)):
            dataS = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}Storage.json')
            spS.append(dataS['sqlprov']['storage'][benchQOrders[index]])
    if 'provsql' in systems:
        for index in range(len(whichbench)):
            dataS = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}Storage.json')
            prS.append(dataS['provsql']['storage'][benchQOrders[index]])
    if 'smokedduck' in systems:
        for index in range(len(whichbench)):
            dataS = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}Storage.json')
            sdS.append(dataS['smokedduck']['storage'][benchQOrders[index]])

    numBars = 0
    if 'gprom' in systems:
        numBars += 2
    if 'sqlprov' in systems:
        numBars += 1
    if 'provsql' in systems:
        numBars += 1
    if 'smokedduck' in systems:
        numBars += 1

    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=numBars)

    fig, axes = plt.subplots(2, 1, figsize=(FIG_WIDTH1*1.4, FIG_HEIGHT), sharey='row',
                             gridspec_kw={'height_ratios': [3, 1], 'hspace': 0, 'wspace': 0})

    id = 0
    barWidth = (0.12 / (numBars / 5))

    # --- plot times
    leftBars = 0
    barPos = 0
    ax = axes[0]
    leftLineStart = 0
    if 'gprom' in systems:
        ax.bar(offsets[barPos], gps[id], width=barWidth,
               bottom = Y_FLOOR, label='GProM-P', color=p_util.clrgp)
        barPos += 1
        leftBars += 1
    if 'sqlprov' in systems:
        ax.bar(offsets[barPos], sp1s[id], width=barWidth,
               bottom = Y_FLOOR, label='SQLProv', color=p_util.clrsp)
        # ax.text(offsets[barPos], sps[id], s=f'{int(sp1s[id]/sps[id]*100)}%',
        #         ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
        barPos += 1
        leftBars += 1
    if 'provsql' in systems:
        ax.bar(offsets[barPos], prs[id], width=barWidth,
               bottom = Y_FLOOR, label='ProvSQL', color=p_util.clrpr)
        barPos += 1
        leftBars += 1
    LeftLineEnd = barPos - 1
    ax.hlines(y = posts[id], xmin = offsets[leftLineStart] - barWidth / 2, xmax = offsets[LeftLineEnd] + barWidth / 2, colors = p_util.clrpg, linestyles = '--', linewidth = LINE_WIDTH, label='PostgreSQL')

    RightLineStart = LeftLineEnd + 1
    if 'gprom' in systems:
        ax.bar(offsets[barPos], gds[id], width=barWidth,
               bottom = Y_FLOOR, label='GProM-D', color=p_util.clrgd)
        barPos += 1
    if 'smokedduck' in systems:
        ax.bar(offsets[barPos], sd1s[id], width=barWidth,
               bottom = Y_FLOOR, label='SmokedDuck', color=p_util.clrsd)
        # ax.text(offsets[barPos], sds[id], s=f'{int(sd1s[id]/sds[id]*100)}%',
        #         ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
        barPos += 1
    RightLineEnd = barPos - 1
    ax.hlines(y = ducks[id], xmin = offsets[RightLineStart] - barWidth / 2, xmax = offsets[RightLineEnd] + barWidth / 2, colors = p_util.clrdk, linestyles = '--', linewidth = LINE_WIDTH, label='DuckDB')

    if SHOW_GRID:
        ax.grid(True, which='major', axis='y', linestyle='--')
        ax.set_axisbelow(True)

    if xticks is not None:
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks, fontsize=FONT_SIZE)
    current_ymin, current_ymax = ax.get_ylim()
    ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)

    barPos = 0
    ax = axes[1]
    if 'gprom' in systems:
        ax.bar(offsets[barPos], gpS[id], width=barWidth, bottom=Y_FLOOR2, label='GProM-P', color=p_util.clrgp)
        barPos += 1
    if 'sqlprov' in systems:
        ax.bar(offsets[barPos], spS[id], width=barWidth, bottom=Y_FLOOR2,   label='SQLProv', color=p_util.clrsp)
        barPos += 1
    if 'provsql' in systems:
        ax.bar(offsets[barPos], prS[id], width=barWidth, bottom=Y_FLOOR2, label='ProvSQL', color=p_util.clrpr)
        barPos += 1
    if 'gprom' in systems:
        ax.bar(offsets[barPos], gdS[id], width=barWidth, bottom=Y_FLOOR2, label='GProM-D', color=p_util.clrgd)
        barPos += 1
    if 'smokedduck' in systems:
        ax.bar(offsets[barPos], sdS[id], width=barWidth, bottom=Y_FLOOR2, label='SmokedDuck', color=p_util.clrsd)
        barPos += 1

    if 'gprom' in systems or 'smokedduck' in systems:
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        axes[0].axvline(x=split_post, color='blue', linestyle=':', linewidth=LINE_WIDTH)
        axes[1].axvline(x=split_post, color='blue', linestyle=':', linewidth=LINE_WIDTH)

    axes[0].text(
        0.25,
        0.93,
        r'$PostgreSQL$',
        ha='center',
        fontweight='bold',
        transform=axes[0].transAxes,
        color='red',
        fontsize=FONT_SIZE / 1.5
    )
    if 'gprom' in systems or 'smokedduck' in systems:
        axes[0].text(
            0.83,
            0.93,
            r'$DuckDB$',
            ha='center',
            fontweight='bold',
            transform=axes[0].transAxes,
            color='red',
            fontsize=FONT_SIZE / 1.5
        )

    axes[0].set_xticks([])
    axes[0].set_yscale('log')

    axes[1].set_xticks([])
    axes[1].set_yscale('log')
    # axes[1].invert_yaxis()
    # split_post = (offsets[2] + offsets[3]) / 2

    axes[0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0].tick_params(axis='y', labelsize=FONT_SIZE)
    axes[1].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
    axes[1].tick_params(axis='y', labelsize=FONT_SIZE)
    for spine in axes[0].spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(LINE_WIDTH)
    # for spine in axes[1].spines.values():
    #     spine.set_edgecolor('black')
    #     spine.set_linewidth(LINE_WIDTH)

    plt.tight_layout()
    plt.savefig(f'{os.getcwd()}/zackups/{saveName}_{sf}.png',
                bbox_inches='tight')

    plt.close()
def plotSPOnly(sf,
          whichbench: list,
          benchQOrders: list,
          saveName: str,
          systems=['sqlprov', 'postgresql'],
          subfigNumTitles: list = None,
          MarkerSize=20,
          Y_FLOOR=1e-3,
          Y_INCREASE_RATIO=1.0,
          Y_FLOOR2=1e-3,
          xticks: list = None):

    assert len(benchQOrders) == len(whichbench), f'benchQOrders: {benchQOrders}, whichbench: {whichbench} : they should have the same length'
    sp1s = []
    sp2s = []
    Ssp = []
    posts = []
    for id in range(len(benchQOrders)):
        data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/{sf}/{whichbench[id]}.json')
        sp1s.append(data['sqlprov']['1']['times'][benchQOrders[id]])
        sp2s.append(data['sqlprov']['2']['times'][benchQOrders[id]])
        posts.append(data['postgresql']['times'][benchQOrders[id]])

        Sdata = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/{sf}/{whichbench[id]}STORAGE.json')
        Ssp.append(Sdata['sqlprov']['storage'][benchQOrders[id]])






    numBars = 0
    if 'gprom' in systems:
        numBars += 2
    if 'sqlprov' in systems:
        numBars += 1
    if 'provsql' in systems:
        numBars += 1
    if 'smokedduck' in systems:
        numBars += 1

    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)

    fig, axes = plt.subplots(2, len(whichbench), figsize=(FIG_WIDTH1*1.4, FIG_HEIGHT), sharey='row',
                             gridspec_kw={'height_ratios': [3, 1], 'hspace': 0, 'wspace': 0})
    if len(whichbench) != 1:
        for id in range(len(whichbench)):
            barWidth = (0.12 / (numBars / 5))

            # --- plot times
            leftBars = 0
            barPos = 0
            ax = axes[0][id]
            leftLineStart = 0
            ax.bar(offsets[barPos],0.0, width=barWidth, bottom = Y_FLOOR)
            barPos += 1
            if 'sqlprov' in systems:
                ax.bar(offsets[barPos], sp1s[id], width=barWidth,
                       bottom = Y_FLOOR, label='SQLProv', color=p_util.clrsp)
                ax.hlines(y = posts[id], xmin = offsets[barPos] - barWidth / 2, xmax = offsets[barPos] + barWidth / 2, colors = p_util.clrpg, linestyles = '--', linewidth = LINE_WIDTH, label='PostgreSQL')
                barPos += 1
            ax.bar(offsets[barPos],0.0, width=barWidth, bottom = Y_FLOOR)



            if SHOW_GRID:
                ax.grid(True, which='major', axis='y', linestyle='--')
                ax.set_axisbelow(True)

            # if xticks is not None:
            #     ax.set_xticks(xticks)
            #     ax.set_xticklabels(xticks, fontsize=FONT_SIZE)
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
        for id in range(len(whichbench)):
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
            barWidth = (0.12 / (numBars / 5))
            barPos = 0
            ax = axes[1][id]
            ax.bar(offsets[barPos],0.0, width=barWidth)
            barPos += 1
            if 'sqlprov' in systems:
                ax.bar(offsets[barPos], Ssp[id], width=barWidth, bottom=Y_FLOOR2,   label='SQLProv', color=p_util.clrsp)
                barPos += 1
            ax.bar(offsets[barPos],0.0, width=barWidth)
            ax.set_xlabel(f'{subfigNumTitles[id]}', fontsize=FONT_SIZE)
            ax.set_xticks([])

        axes[0][0].set_yscale('log')

        axes[1][0].set_xticks([])
        axes[1][0].set_yscale('log')
        # axes[1].invert_yaxis()
        # split_post = (offsets[2] + offsets[3]) / 2

        axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
        axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
        axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
        axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)
    else:
        pass
        # for id in range(len(whichbench)):
        #     offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
        #     barWidth = (0.12 / (numBars / 5))
        #     ax = axes[0][id]
        #     ax.bar(offsets[0],0.0, width=barWidth, bottom = Y_FLOOR)
        #     ax.bar(offsets[1], sp1s[id], width=barWidth,
        #            bottom = Y_FLOOR, label='SQLProv', color=p_util.clrsp)
        #     ax.hlines(y = posts[id], xmin = offsets[1] - barWidth / 2, xmax = offsets[1] + barWidth / 2, colors = p_util.clrpg, linestyles = '--', linewidth = LINE_WIDTH, label='PostgreSQL')
        #     ax.bar(offsets[2],0.0, width=barWidth, bottom = Y_FLOOR)

        #      # -- show grid
        #     if SHOW_GRID:
        #         ax.grid(True, which='major', axis='y', linestyle='--')
        #         ax.set_axisbelow(True)

        #     if xticks is not None:
        #         ax.set_xticks(xticks)
        #         ax.set_xticklabels(xticks, fontsize=FONT_SIZE)
        #     current_ymin, current_ymax = ax.get_ylim()
        #     ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)

        #     ax = axes[1][id]
        #     ax.bar(offsets[0], Ssp[id], width=barWidth, bottom=Y_FLOOR2,   label='SQLProv', color=p_util.clrsp)
    for ax in axes.flatten():
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)

    plt.tight_layout()
    plt.savefig(f'{os.getcwd()}/zackups/{saveName}_{sf}.png',
                bbox_inches='tight')

    plt.close()

def plotsrd(sf, saveName, subfigureTitles, wichbench, benchQOrders, isRL=True, Y_INCREASE_RATIO=1.0, Y_FLOOR=1e-3, Y_FLOOR2 = 1e-2, hasSMD = False):
    gps = []
    gds = []
    prs = []
    sps = []
    sp1s = []
    sp2s = []
    sd1s = []
    sd2s = []
    sds = []
    if isRL:
        data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}_rlgpcap.json')
    else:
        data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}_flgpcap.json')
    # capture only, with out rpd
    # gps.append(data['gprom']['dt']['p']['times'][benchQOrders])
    # gds.append(data['gprom']['dt']['d']['times'][benchQOrders])

    storage = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}STORAGE.json')
    ssp0 = 0.0
    ssp3 = 0.0
    ssp5 = 0.0
    spr0 = 0.0
    spr3 = 0.0
    spr5 = 0.0

    ssmd0 = 0.0
    ssmd3 = 0.0
    ssmd5 = 0.0
    if isRL:
        ssp0 = storage['sqlprov']['p0'][benchQOrders]
        ssp3 = storage['sqlprov']['p3'][benchQOrders]
        ssp5 = storage['sqlprov']['p5'][benchQOrders]

        spr0 = storage['provsql']['p0'][benchQOrders]
        spr3 = storage['provsql']['p3'][benchQOrders]
        spr5 = storage['provsql']['p5'][benchQOrders]
        if hasSMD:
            ssmd0 = storage['smokedduck']['p0'][benchQOrders]
            ssmd3 = storage['smokedduck']['p3'][benchQOrders]
            ssmd5 = storage['smokedduck']['p5'][benchQOrders]
    else:
        ssp0 = storage['sqlprov']['p0'][3]
        ssp3 = storage['sqlprov']['p3'][3]
        ssp5 = storage['sqlprov']['p5'][3]

        spr0 = storage['provsql']['p0'][3]
        spr3 = storage['provsql']['p3'][3]
        spr5 = storage['provsql']['p5'][3]
        if hasSMD:
            ssmd0 = storage['smokedduck']['p0'][3]
            ssmd3 = storage['smokedduck']['p3'][3]
            ssmd5 = storage['smokedduck']['p5'][3]
    # -- no fetch
    # gps.append(0.0)
    # gds.append(0.0)
    # -- use
    if isRL:
        data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}_rlgpuse.json')
    else:
        data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}_flgpuse.json')

    gps.append(data['gprom']['dt']['p']['times'][benchQOrders])
    gds.append(data['gprom']['dt']['d']['times'][benchQOrders])

    if isRL:
        data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}_rlsppr.json')
    else:
        data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}_flsppr.json')

    sp1s.append(data['sqlprov']['1']['times'][benchQOrders])
    sps.append(data['sqlprov']['1']['times'][benchQOrders] + data['sqlprov']['2']['times'][benchQOrders])
    sps.append(data['sqlprov']['4']['times'][benchQOrders])
    sps.append(data['sqlprov']['6']['times'][benchQOrders])

    prs.append(data['provsql']['2']['times'][benchQOrders])
    prs.append(data['provsql']['4']['times'][benchQOrders])
    prs.append(data['provsql']['6']['times'][benchQOrders])

    if hasSMD:
        sd1s.append(data['smokedduck']['1']['times'][benchQOrders])
        sds.append(data['smokedduck']['1']['times'][benchQOrders] + data['smokedduck']['2']['times'][benchQOrders])
        sds.append(data['smokedduck']['4']['times'][benchQOrders])
        sds.append(data['smokedduck']['6']['times'][benchQOrders])

    print(f'gps: {gps}, \n gds: {gds}, \n sps: {sps}, \n prs: {prs}, sds: {sds}')
    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=4)
    if hasSMD:
        offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
    fig, axes = plt.subplots(2, 4, figsize=(FIG_WIDTH1 * 1.4, FIG_HEIGHT), sharey='row', gridspec_kw={ 'height_ratios': [3, 1], 'hspace':0 , 'wspace': 0 })

    for id in range(4):
        # end to end time
        if id == 0:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=4)
            if hasSMD:
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            ax = axes[0][id]
            ax.bar(offsets[0], gps[id], bottom = Y_FLOOR, width=0.12, label='GP', color = p_util.clrgp)
            ax.bar(offsets[1], sps[0] + sps[1] + sps[2], bottom = Y_FLOOR, width=0.12, label='sP', color = p_util.clrsp)
            ax.bar(offsets[2], prs[0] + prs[1] + prs[2], bottom = Y_FLOOR, width=0.12, label='Pr', color = p_util.clrpr)
            ax.bar(offsets[3], gds[id], bottom = Y_FLOOR, width=0.12, label='Gd', color = p_util.clrgd)
            if (hasSMD):
                print("YES")
                ax.bar(offsets[4], sds[0] + sds[1] + sds[2], bottom = Y_FLOOR, width=0.12, label='smd', color = p_util.clrsd)
            if SHOW_GRID:
                ax.grid(True, which='major', axis='y', linestyle='--')
                ax.set_axisbelow(True)

            ax.set_xticks([])
            ax.set_yscale('log')
            ax.text(
                0.25,
                0.93,
                r'$PostgreSQL$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 1.5)

            ax.text(
                0.81,
                0.93,
                r'$DuckDB$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 1.5)
            # -- set edge color and line width for all spines
            current_ymin, current_ymax = ax.get_ylim()
            ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
            leftBars = 3
            split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
            ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
        else:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=2)
            if hasSMD:
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
            print(f'id: {id}')
            # offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
            ax = axes[0][id]
            ax.bar(offsets[0], sps[id - 1], bottom = Y_FLOOR, width=0.12, label='SQLPROV', color=p_util.clrsp)
            if id == 1:
                ax.text(offsets[0], sps[id - 1], s=f'{int(sp1s[id - 1]/(sps[id - 1])*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
            ax.bar(offsets[1], prs[id - 1], bottom = Y_FLOOR, width=0.12, label='ProvSQL', color=p_util.clrpr)
            if hasSMD:
                ax.bar(offsets[2], sds[id - 1], bottom = Y_FLOOR, width=0.12, label='SmokedDuck', color=p_util.clrsd)
                if id == 1:
                    ax.text(offsets[2], 0.0, s=f'{int(sd1s[id - 1]/(sds[id - 1])*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')


            if SHOW_GRID:
                ax.grid(True, which='major', axis='y', linestyle='--')
                ax.set_axisbelow(True)

            # ax.set_xlabel(f'{subfigureTitles[id]}', fontsize=FONT_SIZE)
            ax.set_xticks([])
            ax.set_yscale('log')
            ax.text(
                0.25,
                0.93,
                r'$PostgreSQL$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 1.5)
            if hasSMD:
                ax.text(
                    0.81,
                    0.93,
                    r'$DuckDB$',
                    ha='center',
                    fontweight='bold',
                    transform=ax.transAxes,
                    color='red',
                    fontsize=FONT_SIZE / 1.5)
            # -- set edge color and line width for all spines
            current_ymin, current_ymax = ax.get_ylim()
            ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
            if hasSMD:
                leftBars = 2
                split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
                ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
    for id in range(4):
        ax = axes[1][id]
        if (id == 0):
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=4)
            if hasSMD:
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            ax.bar(offsets[0], 0.0, bottom = Y_FLOOR2, width=0.12, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], ssp0 + ssp3+ ssp5, bottom = Y_FLOOR2, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[2], spr0 + spr3 + spr5, bottom = Y_FLOOR2, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[3], 0.0, bottom = Y_FLOOR2, width=0.12, label='GProM-D', color=p_util.clrgd)
            if hasSMD:
                ax.bar(offsets[4], ssmd0 + ssmd3 + ssmd5, bottom = Y_FLOOR2, width=0.12, label='SmokedDuck', color=p_util.clrsd)

        if (id == 1):
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=2)
            if hasSMD:
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
            ax.bar(offsets[0], ssp0 + ssp3, bottom = Y_FLOOR2, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[1], spr0 + spr3, bottom = Y_FLOOR2, width=0.12, label='ProvSQL', color=p_util.clrpr)
            if hasSMD:
                ax.bar(offsets[2], ssmd0 + ssmd3, bottom = Y_FLOOR2, width=0.12, label='SmokedDuck', color=p_util.clrsd)
        if (id == 2):
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=2)
            if hasSMD:
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
            ax.bar(offsets[0], ssp5, bottom = Y_FLOOR2, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[1], spr5, bottom = Y_FLOOR2, width=0.12, label='ProvSQL', color=p_util.clrpr)
            if hasSMD:
                ax.bar(offsets[2], ssmd5, bottom = Y_FLOOR2, width=0.12, label='SmokedDuck', color=p_util.clrsd)
        ax.set_yscale('log')
        # ax.invert_yaxis()
        ax.set_xticks([])
        ax.set_xlabel(f'{subfigureTitles[id]}', fontsize=FONT_SIZE)
    for ax in axes.flatten():
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)

    axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
    axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
    axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'{os.getcwd()}/zackups/{saveName}_{sf}.png', bbox_inches='tight')
    plt.close()

def plotsrd2(sf, saveName, subfigureTitles, wichbench, benchQOrders, isRL=True, Y_INCREASE_RATIO=1.0, Y_FLOOR=1e-3, Y_FLOOR2 = 1e-2, hasSMD = False, GPSS = 0.0, GDSS = 0.0):
    # gps = []
    # gds = []

    prs = []

    sps = []
    sp1s = []
    sp2s = []
    sd1s = []
    sd2s = []
    sds = []
    if isRL:
        data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}_gprom.json')
    else:
        data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}_gprom.json')
    # capture only, with out rpd
    # gps.append(data['gprom']['dt']['p']['times'][benchQOrders])
    # gds.append(data['gprom']['dt']['d']['times'][benchQOrders])

    storage = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}STORAGE.json')
    ssp0 = 0.0
    ssp3 = 0.0
    ssp5 = 0.0
    spr0 = 0.0
    spr3 = 0.0
    spr5 = 0.0

    ssmd0 = 0.0
    ssmd3 = 0.0
    ssmd5 = 0.0
    if isRL:
        ssp0 = storage['sqlprov']['p0'][benchQOrders]
        ssp3 = storage['sqlprov']['p3'][benchQOrders]
        ssp5 = storage['sqlprov']['p5'][benchQOrders]

        spr0 = storage['provsql']['p0'][benchQOrders]
        spr3 = storage['provsql']['p3'][benchQOrders]
        spr5 = storage['provsql']['p5'][benchQOrders]
        ssmd0 = storage['smokedduck']['p0'][benchQOrders]
        ssmd3 = storage['smokedduck']['p3'][benchQOrders]
        ssmd5 = storage['smokedduck']['p5'][benchQOrders]
    else:
        ssp0 = storage['sqlprov']['p0'][3]
        ssp3 = storage['sqlprov']['p3'][3]
        ssp5 = storage['sqlprov']['p5'][3]

        spr0 = storage['provsql']['p0'][3]
        spr3 = storage['provsql']['p3'][3]
        spr5 = storage['provsql']['p5'][3]
        ssmd0 = storage['smokedduck']['p0'][3]
        ssmd3 = storage['smokedduck']['p3'][3]
        ssmd5 = storage['smokedduck']['p5'][3]
    # -- no fetch
    # gps.append(0.0)
    # gds.append(0.0)
    gps = []
    gds = []
    data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}_gprom.json')

    if isRL:
        gps.append(data['gpromp']['1']['times'][benchQOrders])
        gps.append(data['gpromp']['3']['times'][benchQOrders])
        gps.append(data['gpromp']['5']['times'][benchQOrders])
        gds.append(data['gpromd']['1']['times'][benchQOrders])
        gds.append(data['gpromd']['3']['times'][benchQOrders])
        gds.append(data['gpromd']['5']['times'][benchQOrders])
    else:
        gps.append(data['gpromp']['1']['times'][3])
        gps.append(data['gpromp']['3']['times'][3])
        gps.append(data['gpromp']['5']['times'][3])
        gds.append(data['gpromd']['1']['times'][3])
        gds.append(data['gpromd']['3']['times'][3])
        gds.append(data['gpromd']['5']['times'][3])



    # gds = []
    # gps.append(data['gprom']['dt']['p']['times'][benchQOrders])
    # gds.append(data['gprom']['dt']['d']['times'][benchQOrders])

    if isRL:
        data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}_rlsppr.json')
    else:
        data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/{wichbench}_flsppr.json')

    sp1s.append(data['sqlprov']['1']['times'][benchQOrders])
    sps.append(data['sqlprov']['1']['times'][benchQOrders] + data['sqlprov']['2']['times'][benchQOrders])
    sps.append(data['sqlprov']['4']['times'][benchQOrders])
    sps.append(data['sqlprov']['6']['times'][benchQOrders])

    prs.append(data['provsql']['2']['times'][benchQOrders])
    prs.append(data['provsql']['4']['times'][benchQOrders])
    prs.append(data['provsql']['6']['times'][benchQOrders])

    sd1s.append(data['smokedduck']['1']['times'][benchQOrders])
    sds.append(data['smokedduck']['1']['times'][benchQOrders] + data['smokedduck']['2']['times'][benchQOrders])
    sds.append(data['smokedduck']['4']['times'][benchQOrders])
    sds.append(data['smokedduck']['6']['times'][benchQOrders])

    print(f'gps: {gps}, \n gds: {gds}, \n sps: {sps}, \n prs: {prs}, sds: {sds}')
    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
    fig, axes = plt.subplots(2, 4, figsize=(FIG_WIDTH1 * 1.4, FIG_HEIGHT), sharey='row', gridspec_kw={ 'height_ratios': [3, 1], 'hspace':0 , 'wspace': 0 })

    for id in range(4):
        # end to end time
        if id == 0:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            ax = axes[0][id]
            ax.bar(offsets[0], gps[0] + gps[1] + gps[2], bottom = Y_FLOOR, width=0.12, label='GP', color = p_util.clrgp)
            ax.bar(offsets[1], sps[0] + sps[1] + sps[2], bottom = Y_FLOOR, width=0.12, label='sP', color = p_util.clrsp)
            ax.bar(offsets[2], prs[0] + prs[1] + prs[2], bottom = Y_FLOOR, width=0.12, label='Pr', color = p_util.clrpr)
            ax.bar(offsets[3], gds[0] + gds[1] + gds[2], bottom = Y_FLOOR, width=0.12, label='Gd', color = p_util.clrgd)
            ax.bar(offsets[4], sds[0] + sds[1] + sds[2], bottom = Y_FLOOR, width=0.12, label='smd', color = p_util.clrsd)
            if SHOW_GRID:
                ax.grid(True, which='major', axis='y', linestyle='--')
                ax.set_axisbelow(True)

            ax.set_xticks([])
            ax.set_yscale('log')
            ax.text(
                0.25,
                0.93,
                r'$PostgreSQL$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 1.5)

            ax.text(
                0.81,
                0.93,
                r'$DuckDB$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 1.5)
            # -- set edge color and line width for all spines
            current_ymin, current_ymax = ax.get_ylim()
            ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
            leftBars = 3
            split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
            ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
        else:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            print(f'id: {id}')
            # offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
            ax = axes[0][id]
            ax.bar(offsets[0], gps[id - 1], bottom = Y_FLOOR, width=0.12, label='GP', color=p_util.clrgp)
            ax.bar(offsets[1], sps[id - 1], bottom = Y_FLOOR, width=0.12, label='SQLPROV', color=p_util.clrsp)
            if id == 1:
                ax.text(offsets[1], sps[id - 1], s=f'{int(sp1s[id - 1]/(sps[id - 1])*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
            ax.bar(offsets[2], prs[id - 1], bottom = Y_FLOOR, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[3], gds[id - 1], bottom = Y_FLOOR, width=0.12, label='GProM-D', color=p_util.clrgd)
            ax.bar(offsets[4], sds[id - 1], bottom = Y_FLOOR, width=0.12, label='SmokedDuck', color=p_util.clrsd)
            if id == 1:
                ax.text(offsets[4], sds[id - 1], s=f'{int(sd1s[id - 1]/(sds[id - 1])*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')


            if SHOW_GRID:
                ax.grid(True, which='major', axis='y', linestyle='--')
                ax.set_axisbelow(True)

            # ax.set_xlabel(f'{subfigureTitles[id]}', fontsize=FONT_SIZE)
            ax.set_xticks([])
            ax.set_yscale('log')
            ax.text(
                0.25,
                0.93,
                r'$PostgreSQL$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 1.5)
            if hasSMD:
                ax.text(
                    0.81,
                    0.93,
                    r'$DuckDB$',
                    ha='center',
                    fontweight='bold',
                    transform=ax.transAxes,
                    color='red',
                    fontsize=FONT_SIZE / 1.5)
            # -- set edge color and line width for all spines
            current_ymin, current_ymax = ax.get_ylim()
            ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
            leftBars = 3
            split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
            ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
    for id in range(4):
        ax = axes[1][id]
        if (id == 0):
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            ax.bar(offsets[0], GPSS, bottom = Y_FLOOR2, width=0.12, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], ssp0 + ssp3+ ssp5, bottom = Y_FLOOR2, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[2], spr0 + spr3 + spr5, bottom = Y_FLOOR2, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[3], GDSS, bottom = Y_FLOOR2, width=0.12, label='GProM-D', color=p_util.clrgd)
            ax.bar(offsets[4], ssmd0 + ssmd3 + ssmd5, bottom = Y_FLOOR2, width=0.12, label='SmokedDuck', color=p_util.clrsd)
            split_post = (offsets[2] + offsets[3]) / 2
            ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
        if (id == 1):
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            ax.bar(offsets[0], 0.0, bottom = Y_FLOOR2, width=0.12, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], ssp0 + ssp3, bottom = Y_FLOOR2, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[2], spr0 + spr3, bottom = Y_FLOOR2, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[3], 0.0, bottom = Y_FLOOR2, width=0.12, label='GProM-D', color=p_util.clrgd)
            ax.bar(offsets[4], ssmd0 + ssmd3, bottom = Y_FLOOR2, width=0.12, label='SmokedDuck', color=p_util.clrsd)
            split_post = (offsets[2] + offsets[3]) / 2
            ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
        if (id == 2):
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            ax.bar(offsets[0], GPSS, bottom = Y_FLOOR2, width=0.12, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], ssp5, bottom = Y_FLOOR2, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[2], spr5, bottom = Y_FLOOR2, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[3], GDSS, bottom = Y_FLOOR2, width=0.12, label='GProM-D', color=p_util.clrgd)
            ax.bar(offsets[4], ssmd5, bottom = Y_FLOOR2, width=0.12, label='SmokedDuck', color=p_util.clrsd)
            split_post = (offsets[2] + offsets[3]) / 2
            ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
        if (id == 3):
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            ax.bar(offsets[0], 0.0, bottom = Y_FLOOR2, width=0.12, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], 0.0, bottom = Y_FLOOR2, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[2], 0.0, bottom = Y_FLOOR2, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[3], 0.0, bottom = Y_FLOOR2, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[4], 0.0, bottom = Y_FLOOR2, width=0.12, label='SQLPROV', color=p_util.clrsp)
            split_post = (offsets[2] + offsets[3]) / 2
            ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
        ax.set_yscale('log')
        # ax.invert_yaxis()
        ax.set_xticks([])
        ax.set_xlabel(f'{subfigureTitles[id]}', fontsize=FONT_SIZE)
    for ax in axes.flatten():
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)

    axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
    axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
    axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'{os.getcwd()}/zackups/{saveName}_{sf}.png')
    plt.close()

def plotProvPoly(sf, saveName, subfigureTitles, whichbench, benchQOrders, Y_INCREASE_RATIO=1.0, Y_FLOOR=1e-3, Y_FLOOR2 = 1e-1):
    data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMPP.json')
    gds = []
    gps = []
    sd1s = []
    sd2s = []
    prs = []
    gds = data['gprom']['d']['times']
    gps = data['gprom']['p']['times']

    prs = data['provsql']['times']
    sd1s = data['smokedduck']['1']['times']
    sd2s = data['smokedduck']['2']['times']


#     sd1s.append(Agg['smokedduck']['1']['times'][0])
#     sd2s.append(Agg['smokedduck']['2']['times'][0])
#
#     prs.append(Agg['provsql']['times'][0])

    PMPPStorage = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMPPSTORAGE.json')
    Ssds = PMPPStorage['smokedduck']['storage']
    Sprs = PMPPStorage['provsql']['storage']
    Sgps = [0.0 for _ in range(4)]
    Sgds = [0.0 for _ in range(4)]


    fig, axes = plt.subplots(2, 5, figsize=(FIG_WIDTH1 * 1.4, FIG_HEIGHT), sharey='row', gridspec_kw={ 'height_ratios': [3, 1], 'hspace':0 , 'wspace': 0 })

    for id in range(5):
        ax = axes[0][id]
        if id < 3:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=4)
            ax.bar(offsets[0], gps[id], bottom = Y_FLOOR, width=0.12, label='GP', color = p_util.clrgp)
            ax.bar(offsets[1], prs[id], bottom = Y_FLOOR, width=0.12, label='Pr', color = p_util.clrpr)
            ax.bar(offsets[2], gds[id], bottom = Y_FLOOR, width=0.12, label='Gd', color = p_util.clrgd)
            ax.bar(offsets[3], sd1s[id] + sd2s[id], bottom = Y_FLOOR, width=0.12, label='smd', color = p_util.clrsd)
            ax.text(offsets[3], sd1s[id] + sd2s[id] + 0.1, s=f'{int(sd1s[id] / (sd1s[id] + sd2s[id]) * 100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
        else:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=2)
            ax.bar(offsets[0], prs[id], bottom = Y_FLOOR, width=0.12, label='Pr', color = p_util.clrpr)
            ax.bar(offsets[1], sd1s[id] + sd2s[id], bottom = Y_FLOOR, width=0.12, label='smd', color = p_util.clrsd)
            ax.text(offsets[1], sd1s[id] + sd2s[id] + 0.1, s=f'{int(sd1s[id] / (sd1s[id] + sd2s[id]) * 100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')

        if SHOW_GRID:
            ax.grid(True, which='major', axis='y', linestyle='--')
            ax.set_axisbelow(True)

        ax.set_xticks([])
        ax.set_yscale('log')
        ax.text(
                0.25,
                0.93,
                r'$PostgreSQL$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 1.5)

        ax.text(
                0.81,
                0.93,
                r'$DuckDB$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 1.5)
        # -- set edge color and line width for all spines
        current_ymin, current_ymax = ax.get_ylim()
        ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
        if id < 3:
            leftBars = 2
        else:
            leftBars = 1
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
    for id in range(5):
        ax = axes[1][id]
        offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=4)
        if id < 3:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=4)
            ax.bar(offsets[0], Sgps[id], bottom = Y_FLOOR2, width=0.12, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], Sprs[id], bottom = Y_FLOOR2, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[2], Sgds[id], bottom = Y_FLOOR2, width=0.12, label='GProM-D', color=p_util.clrgd)
            ax.bar(offsets[3], Ssds[id], bottom = Y_FLOOR2, width=0.12, label='SmokedDuck', color=p_util.clrsd)
        else:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=2)
            ax.bar(offsets[0], Sprs[id], bottom = Y_FLOOR2, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[1], Ssds[id], bottom = Y_FLOOR2, width=0.12, label='SmokedDuck', color=p_util.clrsd)
        leftBars = 2
        offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=4)
        if id < 3:
            leftBars = 2
        else:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=2)
            leftBars = 1
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)

        ax.set_yscale('log')
        # ax.invert_yaxis()
        ax.set_xticks([])
        ax.set_xlabel(f'{subfigureTitles[id]}', fontsize=FONT_SIZE)

    for ax in axes.flatten():
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)
    axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
    axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
    axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'{os.getcwd()}/zackups/{saveName}_{sf}.png', bbox_inches='tight')
    plt.close()

def plotApproProv(sf, saveName, subfigureTitles, whichbench, benchQOrders, Y_INCREASE_RATIO=1.0, Y_FLOOR=1e-3):
    Join = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMAP.json')
    gps = []
    gps = Join['gprom']['p']['times']


    fig, axes = plt.subplots(1, 3, figsize=(FIG_WIDTH1 * 1.4, FIG_HEIGHT), sharey='row', gridspec_kw={ 'hspace':0 , 'wspace': 0 })

    for id in range(3):
        ax = axes[id]
        offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
        ax.bar(offsets[0], 0.0, bottom = Y_FLOOR, width=0.12, label='GP', color = p_util.clrgp)
        ax.bar(offsets[1], gps[id] + gps[id + 3], bottom = Y_FLOOR, width=0.12, label='Pr', color = p_util.clrgp)
        ax.text(offsets[1], gps[id] + gps[id + 3], s=f'{int(gps[id]/(gps[id] + gps[id + 3])*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
        ax.bar(offsets[2], 0.0, bottom = Y_FLOOR, width=0.12, label='Gd', color = p_util.clrgd)

        if SHOW_GRID:
            ax.grid(True, which='major', axis='y', linestyle='--')
            ax.set_axisbelow(True)

        ax.set_xticks([])
        ax.set_yscale('log')
        ax.text(
                0.25,
                0.93,
                r'$PostgreSQL$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 1.5)
        ax.set_xlabel(f'{subfigureTitles[id]}', fontsize=FONT_SIZE)
        # -- set edge color and line width for all spines
        current_ymin, current_ymax = ax.get_ylim()
        ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
    for ax in axes.flatten():
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)
    axes[0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0].tick_params(axis='y', labelsize=FONT_SIZE)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'{os.getcwd()}/zackups/{saveName}_{sf}.png', bbox_inches='tight')
    plt.close()

def plotDBG(sf, savename, subfigureTitles, whichbench, benchQOrders, isRL=True, Y_INCREASE_RATIO=1.0, Y_FLOOR=1e-3, Y_FLOOR2 = 1, SECOND_SYS_START_POST = 0.81):
    data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMBD_gp.json')
    gps = data['gprom']['dt']['p']['times']
    gds = data['gprom']['dt']['d']['times']

    data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMBD_sppr.json')
    sp1s = data['sqlprov']['1']['times'][0]
    sp2s = data['sqlprov']['2']['times'][0]

    sp4s = data['sqlprov']['4']['times'][0]
    sp6s = data['sqlprov']['6']['times']

    prs = data['provsql']['2']['times']
    pr1s = data['provsql']['1']['times'][0]
    pr2s = data['provsql']['2']['times'][0]
    pr4s = data['provsql']['4']['times'][0]
    pr6s = data['provsql']['6']['times']

    sd1s = data['smokedduck']['1']['times'][0]
    sd2s = data['smokedduck']['2']['times'][0]
    sd4s = data['smokedduck']['4']['times'][0]
    sd6s = data['smokedduck']['6']['times']



    smd1cap = [0.0 for _ in range(len(prs))]
    smd2cap = [0.0 for _ in range(len(prs))]
    smd4fetch = [0.0 for _ in range(len(prs))]
    smd6use = [0.0 for _ in range(len(prs))]

    storage = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMBDSTORAGE.json')
    smd0s = storage['smokedduck']['p0']
    smd3s = storage['smokedduck']['p3']
    smd5s = storage['smokedduck']['p5']

    sp0s = storage['sqlprov']['p0']
    sp3s = storage['sqlprov']['p3']
    sp5s = storage['sqlprov']['p5']

    pr0s = storage['provsql']['p0']
    pr3s = storage['provsql']['p3']
    pr5s = storage['provsql']['p5']
    ################################
    # plot all end to end
    ################################
    fig, axes = plt.subplots(2, 3, figsize=(FIG_WIDTH1 * 1.5, FIG_HEIGHT), sharey='row', gridspec_kw={ 'height_ratios': [3, 1], 'hspace':0 , 'wspace': 0 })
    gpHere = [gps[1], gps[2], gps[3]]
    gdHere = [gds[1], gds[2], gds[3]]
    spHere = [sp1s + sp2s + sp4s + sp6s[1],
              sp1s + sp2s + sp4s + sp6s[2],
              sp1s + sp2s + sp4s + sp6s[3]]
    prHere = [pr1s + pr2s + pr4s + pr6s[1],
              pr1s + pr2s + pr4s + pr6s[2],
              pr1s + pr2s + pr4s + pr6s[3]]
    sdHere = [sd1s + sd2s + sd4s + sd6s[1],
                sd1s + sd2s + sd4s + sd6s[2],
                sd1s + sd2s + sd4s + sd6s[3]]

    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
    for id in range(3):
        ax = axes[0][id]
        ax.bar(offsets[0], gpHere[id], bottom = Y_FLOOR, width = 0.12, color = p_util.clrgp)
        ax.bar(offsets[1], spHere[id], bottom = Y_FLOOR, width = 0.12, color = p_util.clrsp)
        ax.bar(offsets[2], prHere[id], bottom = Y_FLOOR, width = 0.12, color = p_util.clrpr)
        ax.bar(offsets[3], gdHere[id], bottom = Y_FLOOR, width = 0.12, color = p_util.clrgd)
        ax.bar(offsets[4], sdHere[id], bottom = Y_FLOOR, width = 0.12, color = p_util.clrsd)

        ax.set_xticks([])
        ax.set_yscale('log')
        if SHOW_GRID:
            ax.grid(True, which='major', axis='y', linestyle='--')
            ax.set_axisbelow(True)
        ax.text(
                0.25,
                0.93,
                r'$PostgreSQL$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 1.5)

        ax.text(
                SECOND_SYS_START_POST,
                0.93,
                r'$DuckDB$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 1.5)
        # -- set edge color and line width for all spines
        current_ymin, current_ymax = ax.get_ylim()
        ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
        leftBars = 3
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
    endtoendTitles = ['Data error rate: 1%', 'Data error rate: 10%', 'Data error rate: 50%']
    for id in range(3):
        offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
        ax = axes[1][id]
        ax.bar(offsets[0], 0.0, width = 0.12)
        ax.bar(offsets[1], sp0s[id] + sp3s[id] + sp5s[id], width=0.12, label='SQLPROV', color=p_util.clrsp)
        ax.bar(offsets[2], pr0s[id] + pr3s[id] + pr5s[id], width=0.12, label='ProvSQL', color=p_util.clrpr)
        ax.bar(offsets[3], 0.0,  width=0.12, label='GProM-D', color=p_util.clrgd)
        ax.bar(offsets[4], smd0s[id] + smd3s[id] + smd5s[id], bottom = Y_FLOOR2, width=0.12, label='SmokedDuck', color=p_util.clrsd)

        ax.set_xticks([])
        ax.set_yscale('log')

        leftBars = 3
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)

        ax.set_xlabel(f'{endtoendTitles[id]}', fontsize=FONT_SIZE)

    for ax in axes.flatten():
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)

    axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
    axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
    axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)
    fig.set_constrained_layout(True)
    plt.tight_layout()
    plt.savefig(f'{os.getcwd()}/zackups/Fig_pmbd_endtoend_{sf}.png', bbox_inches='tight')
    plt.close()

    ####################################
    # breakdown for sp, pr and sd
    ####################################
    fig, axes = plt.subplots(2, 5, figsize=(FIG_WIDTH1 * 1.5, FIG_HEIGHT), sharey='row', gridspec_kw={ 'height_ratios': [3, 1], 'hspace':0 , 'wspace': 0 })
    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)

    titles = ['Capture', 'Query', 'Debugging: 1%', 'Debugging: 10%', 'Debugging: 50%']
    for id in range(5):
        spH = sp1s+ sp2s if id == 0 else (sp4s if id == 1 else sp6s[id - 1])
        prH = pr2s if id == 0 else (pr4s if id == 1 else pr6s[id - 1])
        sdH = sd1s + sd2s if id == 0 else (sd4s if id == 1 else sd6s[id - 1])
        # sdH = 0.0 ## now set to 0.0

        offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
        ax = axes[0][id]

        ax.bar(offsets[0], spH, bottom = Y_FLOOR, width=0.12, label='SQLPROV', color=p_util.clrsp)
        if id == 0:
            ax.text(offsets[0], spH, s=f'{int(sp1s/(sp1s + sp2s)*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
        ax.bar(offsets[1], prH, bottom = Y_FLOOR, width=0.12, label='ProvSQL', color=p_util.clrpr)
        ax.bar(offsets[2], sdH, bottom = Y_FLOOR, width=0.12, label='SmokedDuck', color=p_util.clrsd)
        if id == 0:
            ax.text(offsets[2], sdH, s=f'{int(sd1s/(sd1s + sd2s)*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
        if SHOW_GRID:
            ax.grid(True, which='major', axis='y', linestyle='--')
            ax.set_axisbelow(True)
        ax.set_xticks([])
        ax.set_yscale('log')
        ax.text(
            0.25,
            0.93,
            r'$PostgreSQL$',
            ha='center',
            fontweight='bold',
            transform=ax.transAxes,
            color='red',
            fontsize=FONT_SIZE / 1.5)

        ax.text(
            SECOND_SYS_START_POST,
            0.93,
            r'$DuckDB$',
            ha='center',
            fontweight='bold',
            transform=ax.transAxes,
            color='red',
            fontsize=FONT_SIZE / 1.5)
        # -- set edge color and line width for all spines
        current_ymin, current_ymax = ax.get_ylim()
        ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
        leftBars = 2
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)

    for id in range(5):
        ax = axes[1][id]
        if id == 0:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
            ax.bar(offsets[0], sp0s[id] + sp3s[id],  width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[1], pr0s[id] + pr3s[id],  width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[2], smd0s[id] + smd3s[id], width=0.12, label='SmokedDuck', color=p_util.clrsd)
        elif id == 1:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
            ax.bar(offsets[0], sp5s[id],  width = 0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[1], pr5s[id],  width = 0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[2], smd5s[id], width = 0.12, label='SmokedDuck', color=p_util.clrsd)
        else:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
            ax.bar(offsets[0], 0.0, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[1], 0.0, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[2], 0.0, width=0.12, label='SmokedDuck', color=p_util.clrsd)

        leftBars = 2
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
        ax.set_yscale('log')
        ax.set_xticks([])
        ax.set_xlabel(f'{titles[id]}', fontsize=FONT_SIZE)

    for ax in axes.flatten():
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)
    axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
    axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
    axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)
    plt.tight_layout()
    plt.savefig(f'{os.getcwd()}/zackups/Fig_pmbd_Breakdown_{sf}.png', bbox_inches='tight')
    plt.close()

def plotFBG(sf, savename, subfigureTitles, whichbench, benchQOrders, isRL=True, Y_INCREASE_RATIO=1.0, Y_FLOOR=1e-3, SECOND_SYS_START_POST = 0.81):
    data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMFD_gp.json')
    lowerBound = benchQOrders * 15
    uppderBound = benchQOrders * 15 + 15
    print(f'lowerBound: {lowerBound}, upperBound: {uppderBound}')
    print(f'len(gps): {len(data["gprom"]["dt"]["p"]["times"])}, len(gds): {len(data["gprom"]["dt"]["d"]["times"])}')
    gps = data['gprom']['dt']['p']['times'][lowerBound:uppderBound]
    gds = data['gprom']['dt']['d']['times'][lowerBound:uppderBound]

    GPS = []
    gpP1In = gps[3 + benchQOrders]
    gpP10In = gps[9 + benchQOrders]
    gpP30In = gps[12 + benchQOrders]
    GPS.append(gpP1In)
    GPS.append(gpP10In)
    GPS.append(gpP30In)

    gpP1out = gds[4 - benchQOrders]
    gpP10out = gds[10 - benchQOrders]
    gpP30out = gds[13 - benchQOrders]

    GPS.append(gpP1out)
    GPS.append(gpP10out)
    GPS.append(gpP30out)

    GDS = []
    gdP1In = gds[3 + benchQOrders]
    gdP10In = gds[9 + benchQOrders]
    gdP30In = gds[12 + benchQOrders]
    GDS.append(gdP1In)
    GDS.append(gdP10In)
    GDS.append(gdP30In)

    gdP1out = gds[4 - benchQOrders]
    gdP10out = gds[10 - benchQOrders]
    gdP30out = gds[13 - benchQOrders]
    GDS.append(gdP1out)
    GDS.append(gdP10out)
    GDS.append(gdP30out)


    data = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMFD_sppr.json')

    sd1s = data['smokedduck']['1']['times'][benchQOrders]
    sd2s = data['smokedduck']['2']['times'][benchQOrders]
    sd4s = data['smokedduck']['4']['times'][benchQOrders]
    sd6s = data['smokedduck']['6']['times'][lowerBound:uppderBound]
    SDS = []
    sdP1In = sd6s[3 + benchQOrders]
    sdP10In = sd6s[9 + benchQOrders]
    sdP30In = sd6s[12 + benchQOrders]
    SDS.append(sdP1In)
    SDS.append(sdP10In)
    SDS.append(sdP30In)
    sdP1out = sd6s[4 - benchQOrders]
    sdP10out = sd6s[10 - benchQOrders]
    sdP30out = sd6s[13 - benchQOrders]
    SDS.append(sdP1out)
    SDS.append(sdP10out)
    SDS.append(sdP30out)


    sp1s = data['sqlprov']['1']['times'][benchQOrders]
    sp2s = data['sqlprov']['2']['times'][benchQOrders]

    sp4s = data['sqlprov']['4']['times'][benchQOrders]
    sp6s = data['sqlprov']['6']['times'][lowerBound:uppderBound]

    SPS = []

    spP1In = sp6s[3 + benchQOrders]
    spP10In = sp6s[9 + benchQOrders]
    spP30In = sp6s[12 + benchQOrders]

    SPS.append(spP1In)
    SPS.append(spP10In)
    SPS.append(spP30In)

    spP1out = sp6s[4 - benchQOrders]
    spP10out = sp6s[10 - benchQOrders]
    spP30out = sp6s[13 - benchQOrders]

    SPS.append(spP1out)
    SPS.append(spP10out)
    SPS.append(spP30out)





    prs = data['provsql']['2']['times']
    pr1s = data['provsql']['1']['times'][benchQOrders]
    pr2s = data['provsql']['2']['times'][benchQOrders]
    pr4s = data['provsql']['4']['times'][benchQOrders]
    pr6s = data['provsql']['6']['times'][lowerBound:uppderBound]

    PRS = []
    prP1In = pr6s[3 + benchQOrders]
    prP10In = pr6s[9 + benchQOrders]
    prP30In = pr6s[12 + benchQOrders]

    PRS.append(prP1In)
    PRS.append(prP10In)
    PRS.append(prP30In)

    prP1out = pr6s[4 - benchQOrders]
    prP10out = pr6s[10 - benchQOrders]
    prP30out = pr6s[13 - benchQOrders]
    PRS.append(prP1out)
    PRS.append(prP10out)
    PRS.append(prP30out)


    Sgd = 0.0
    Sgp = 0.0
    sData = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMFDSTORAGE.json')
    SsdC = sData['smokedduck']['p0'] + sData['smokedduck']['p3']
    SsdFetch = sData['smokedduck']['p5']

    SprC = sData['provsql']['p0'] + sData['provsql']['p3']
    SprFetch = sData['provsql']['p5']

    SspC = sData['sqlprov']['p0'] + sData['sqlprov']['p3']
    SspFetch = sData['sqlprov']['p5']
    ########################################
    # end to end
    ########################################
    titles = ['Q Affected\nError rate: 1%', 'Q Affected\nError rate: 10%', 'Q Affected\nError rate: 30%', 'Q Not Affected\nError rate: 1%', 'Q Not Affected\nError rate: 10%', 'Q Not Affected\nError rate: 30%']
    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
    fig, axes = plt.subplots(2, 6, figsize=(FIG_WIDTH1 * 1.8, FIG_HEIGHT), sharey='row', gridspec_kw={ 'height_ratios': [3, 1], 'hspace':0 , 'wspace': 0 })
    for id in range(6):
        ax = axes[0][id]
        ax.bar(offsets[0], GPS[id], bottom = Y_FLOOR, width=0.12, label='GProM-P', color=p_util.clrgp)
        ax.bar(offsets[1], SPS[id] + sp1s + sp2s + sp4s, bottom = Y_FLOOR, width=0.12, label='SQLPROV', color=p_util.clrsp)
        ax.bar(offsets[2], PRS[id] + pr2s + pr4s, bottom = Y_FLOOR, width=0.12, label='ProvSQL', color=p_util.clrpr)
        ax.bar(offsets[3], GDS[id], bottom = Y_FLOOR, width=0.12, label='gd', color=p_util.clrgd)
        ax.bar(offsets[4], SDS[id] + sd1s + sd2s + sd4s, bottom = Y_FLOOR, width=0.12, label='SmokedDuck', color=p_util.clrsd)
        ax.set_xticks([])
        ax.set_yscale('log')
        if SHOW_GRID:
            ax.grid(True, which='major', axis='y', linestyle='--')
            ax.set_axisbelow(True)
        ax.text(
            0.25,
            0.93,
            r'$PostgreSQL$',
            ha='center',
            fontweight='bold',
            transform=ax.transAxes,
            color='red',
            fontsize=FONT_SIZE / 2)
        ax.text(
            SECOND_SYS_START_POST,
            0.93,
            r'$DuckDB$',
            ha='center',
            fontweight='bold',
            transform=ax.transAxes,
            color='red',
            fontsize=FONT_SIZE / 2)
        # -- set edge color and line width for all spines
        current_ymin, current_ymax = ax.get_ylim()
        ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
        leftBars = 3
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)

    # -- plot storage
    for id in range(6):
        ax = axes[1][id]
        for bar in range(5): # dummy bars
            ax.bar(offsets[0], 0.0, width=0.12, color=p_util.clrgp)
            ax.bar(offsets[1], SspC + SspFetch, width=0.12, color=p_util.clrsp)
            ax.bar(offsets[2], SprC + SprFetch, width=0.12, color=p_util.clrpr)
            ax.bar(offsets[3], 0.0, width=0.12, color=p_util.clrgd)
            ax.bar(offsets[4], SsdC + SsdFetch, width=0.12, color=p_util.clrsd)
        ax.set_xticks([])
        ax.set_yscale('log')
        leftBars = 3
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
        ax.set_xlabel(f'{titles[id]}', fontsize=FONT_SIZE - 5)

    for ax in axes.flatten():
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)
    axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
    axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
    axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)

    plt.tight_layout()
    plt.savefig(f'{os.getcwd()}/zackups/{savename}_endtoend_{sf}.png', bbox_inches='tight')
    plt.close()

    # breakdown
    titles = ['Capture', 'Query', '1% & Affected ', '10% & Affected', '30% & Affected', '1% & Not Affected', '10% & Not Affected', '30% & Not Affected']
    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
    fig, axes = plt.subplots(2, 8, figsize=(FIG_WIDTH1 * 1.8, FIG_HEIGHT), sharey='row', gridspec_kw={ 'height_ratios': [3, 1], 'hspace':0 , 'wspace': 0 })
    for id in range(8):
        ax = axes[0][id]
        sp = sp1s + sp2s if id == 0 else (sp4s if id == 1 else SPS[id - 2])
        pr = pr2s if id == 0 else (pr4s if id == 1 else PRS[id - 2])
        sd = sd1s + sd2s if id == 0 else (sd4s if id == 1 else SDS[id - 2])
        ax.bar(offsets[0], sp, bottom = Y_FLOOR, width=0.12, label='SQLPROV', color=p_util.clrsp)
        if id == 0:
            ax.text(offsets[0], sp, s=f'{int(sp1s/(sp1s + sp2s)*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
        ax.bar(offsets[1], pr, bottom = Y_FLOOR, width=0.12, label='ProvSQL', color=p_util.clrpr)
        ax.bar(offsets[2], sd, bottom = Y_FLOOR, width=0.12, label='SmokedDuck', color=p_util.clrsd)
        if id == 0:
            ax.text(offsets[2], sd, s=f'{int(sd1s/(sd1s + sd2s)*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
        if SHOW_GRID:
            ax.grid(True, which='major', axis='y', linestyle='--')
            ax.set_axisbelow(True)
        ax.set_xticks([])
        ax.set_yscale('log')
        ax.text(
            0.25,
            0.93,
            r'$PostgreSQL$',
            ha='center',
            fontweight='bold',
            transform=ax.transAxes,
            color='red',
            fontsize=FONT_SIZE / 2)
        ax.text(
            SECOND_SYS_START_POST,
            0.93,
            r'$DuckDB$',
            ha='center',
            fontweight='bold',
            transform=ax.transAxes,
            color='red',
            fontsize=FONT_SIZE / 2)
        # -- set edge color and line width for all spines
        current_ymin, current_ymax = ax.get_ylim()
        ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
        leftBars = 2
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)

    for id in range(8):
        ax = axes[1][id]
        if id == 0:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
            ax.bar(offsets[0], SspC, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[1], SprC, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[2], SsdC, width=0.12, label='SmokedDuck', color=p_util.clrsd)
        if id == 1:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=3)
            ax.bar(offsets[0], SspFetch, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[1], SprFetch, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[2], SsdFetch, width=0.12, label='SmokedDuck', color=p_util.clrsd)
        else:
            for bar in range(3): # dummy bars
                ax.bar(offsets[bar], 0.0, width=0.12)
        ax.set_xticks([])
        ax.set_yscale('log')
        leftBars = 2
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
        ax.set_xlabel(f'{titles[id]}', fontsize=FONT_SIZE - 10)
    for ax in axes.flatten():
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)
    axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
    axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
    axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)
    plt.tight_layout()
    plt.savefig(f'{os.getcwd()}/zackups/{savename}_breakdown_{sf}.png', bbox_inches='tight')
    plt.close()

def plotPM(sf, savename, subfigureTitles, whichbench, benchQOrders, isRL=True, Y_INCREASE_RATIO=1.0, Y_FLOOR=1e-3):
    # ------------ Lineage and witness
    # gprom full
    gData = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMRLIN2_flgpcap.json')
    gdF = gData['gprom']['dt']['d']['times'][0]
    gpF = gData['gprom']['dt']['p']['times'][0]
    SgpF = 0.0
    SgdF = 0.0


    # gprom min
    gData = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMRLIN2_rlgpcap.json')
    gdR = gData['gprom']['dt']['d']['times'][0]
    gpR = gData['gprom']['dt']['p']['times'][0]
    SgdR = 0.0
    SgpR = 0.0

    # other full
    mData = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMRLIN2_flsppr.json')
    spF1 = mData['sqlprov']['1']['times'][0]
    spF2 = mData['sqlprov']['2']['times'][0]



    sdF1 = mData['smokedduck']['1']['times'][0]
    sdF2 = mData['smokedduck']['2']['times'][0]


    prF1 = mData['provsql']['1']['times'][0]

    fullStorage = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMRLIN2STORAGE.json')

    SspF = fullStorage['sqlprov']['p0'][3] + fullStorage['sqlprov']['p3'][3] + fullStorage['sqlprov']['p5'][3]
    SprF = fullStorage['provsql']['p0'][3] + fullStorage['provsql']['p3'][3] + fullStorage['provsql']['p5'][3]
    SsdF = fullStorage['smokedduck']['p0'][3] + fullStorage['smokedduck']['p3'][3] + fullStorage['smokedduck']['p5'][3]
    # sData = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMRLINSTORAGE.json')
    # spS = sData['sqlprov']['p0']

    # others min
    mData = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMRLIN2_rlsppr.json')
    spR1 = mData['sqlprov']['1']['times'][0]
    spR2 = mData['sqlprov']['2']['times'][0]

    sdR1 = mData['smokedduck']['1']['times'][0]
    sdR2 = mData['smokedduck']['2']['times'][0]

    prR1 = mData['provsql']['1']['times'][0]

    SspR = fullStorage['sqlprov']['p0'][0] + fullStorage['sqlprov']['p3'][0] + fullStorage['sqlprov']['p5'][0]
    SprR = fullStorage['provsql']['p0'][0] + fullStorage['provsql']['p3'][0] + fullStorage['provsql']['p5'][0]
    SsdR = fullStorage['smokedduck']['p0'][0] + fullStorage['smokedduck']['p3'][0] + fullStorage['smokedduck']['p5'][0]

    # ------------ PP
    mData = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMPP.json')
    gdPP = mData['gprom']['d']['times'][0]
    gpPP = mData['gprom']['p']['times'][0]

    sdPP1 = mData['smokedduck']['1']['times'][0]
    sdPP2 = mData['smokedduck']['2']['times'][0]
    prPP1 = mData['provsql']['times'][0]

    PPS = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMPPSTORAGE.json')
    SprPP = PPS['provsql']['storage'][0]
    SsdPP = PPS['smokedduck']['storage'][0]
    SgpPP = 0.0
    # ---------- AP
    mData = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/sf1/PMAP.json')
    gpAPC = mData['gprom']['p']['times'][0]
    gpAPU = mData['gprom']['p']['times'][3]

    SgpAP = 0.0
    fig, axes = plt.subplots(2, 4, figsize=(FIG_WIDTH1 * 1.4, FIG_HEIGHT), sharey='row', gridspec_kw={ 'height_ratios': [3, 1], 'hspace':0 , 'wspace': 0 })
    subtitles = ['Lineage', 'Minimal\nWitnesses', 'Provenance\nPolynomials', 'Approximate\nProvenance']
    for id in range(4):
        ax = axes[0][id]
        # -- lineage
        if id == 0:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            ax.bar(offsets[0], gpF, width=0.11, bottom = Y_FLOOR, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], spF1 + spF2, width=0.11, bottom = Y_FLOOR, label='SQLPROV', color=p_util.clrsp)
            ax.text(offsets[1], spF1 + spF2, s=f'{int(spF1/(spF1 + spF2)*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
            ax.bar(offsets[2], prF1, width=0.11, bottom = Y_FLOOR, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[3], gdF, width=0.11, bottom = Y_FLOOR, label='GProM-D', color=p_util.clrgd)
            ax.bar(offsets[4], sdF1 + sdF2, width=0.11, bottom = Y_FLOOR, label='SmokedDuck', color=p_util.clrsd)
            ax.text(offsets[4], sdF1 + sdF2, s=f'{int(sdF1/(sdF1 + sdF2)*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
        # -- minimal witnesses
        elif id == 1:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            ax.bar(offsets[0], gpR, width=0.11, bottom = Y_FLOOR, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], spR1 + spR2, width=0.11, bottom = Y_FLOOR, label='SQLPROV', color=p_util.clrsp)
            ax.text(offsets[1], spR1 + spR2, s=f'{int(spR1/(spR1 + spR2)*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
            ax.bar(offsets[2], prR1, width=0.11, bottom = Y_FLOOR, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[3], gdR, width=0.11, bottom = Y_FLOOR, label='GProM-D', color=p_util.clrgd)
            ax.bar(offsets[4], sdR1 + sdR2, width=0.11, bottom = Y_FLOOR, label='SmokedDuck', color=p_util.clrsd)
            ax.text(offsets[4], sdR1 + sdR2 + 0.02, s=f'{int(sdR1/(sdR1 + sdR2)*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
        # -- provenance polynomials
        elif id == 2:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=4)
            ax.bar(offsets[0], gpPP, width=0.11, bottom = Y_FLOOR, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], prPP1, width=0.11, bottom = Y_FLOOR, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[2], gdPP, width=0.11, bottom = Y_FLOOR, label='GProM-D', color=p_util.clrgd)
            ax.bar(offsets[3], sdPP1 + sdPP2, width=0.11, bottom = Y_FLOOR, label='SmokedDuck', color=p_util.clrsd)
            ax.text(offsets[3], sdPP1 + sdPP2, s=f'{int(sdPP1/(sdPP1 + sdPP2)*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
        else:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            ax.bar(offsets[0], 0.0, width=0.11, bottom = Y_FLOOR, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], 0.0, width=0.11, bottom = Y_FLOOR, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[3], 0.0, width=0.11, bottom = Y_FLOOR, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[4], 0.0, width=0.11, bottom = Y_FLOOR, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[2], gpAPC, width=0.12, bottom = Y_FLOOR, label='GProM-P', color=p_util.clrgp)
            # ax.text(offsets[2], gpAPC + gpAPU, s=f'{int(gpAPC/(gpAPC + gpAPU)*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
            ax.text(
                0.25,
                0.94,
                r'$PostgreSQL$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 2)

        ax.set_xticks([])
        ax.set_yscale('log')
        if SHOW_GRID:
            ax.grid(True, which='major', axis='y', linestyle='--')
            ax.set_axisbelow(True)
        if id == 0 or id == 1 or id == 2:
            if id == 0 or id == 1:
                leftBars = 3
            elif id == 2:
                leftBars = 2
            ax.text(
                0.25,
                0.93,
                r'$PostgreSQL$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 2)
            ax.text(
                0.81,
                0.94,
                r'$DuckDB$',
                ha='center',
                fontweight='bold',
                transform=ax.transAxes,
                color='red',
                fontsize=FONT_SIZE / 2)
            # -- set edge color and line width for all spines
            current_ymin, current_ymax = ax.get_ylim()
            ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
            split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
            ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
    print(f'{subfigureTitles}')


    for id in range(4):
        ax = axes[1][id]
        if id == 0:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            ax.bar(offsets[0], SgpF, width=0.12, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], SspF, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[2], SprF, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[3], 0.0, width=0.12, label='GProM-D', color=p_util.clrgd)
            ax.bar(offsets[4], SsdF, width=0.12, label='SmokedDuck', color=p_util.clrsd)
        elif id == 1:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            ax.bar(offsets[0], SgpR, width=0.12, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], SspR, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[2], SprR, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[3], SsdR, width=0.12, label='SmokedDuck', color=p_util.clrsd)
            ax.bar(offsets[4], 0.0, width=0.12, label='GProM-D', color=p_util.clrgd)
        elif id == 2:
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=4)
            ax.bar(offsets[0], SgpPP, width=0.12, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], SprPP, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[2], 0.0, width=0.12, label='GProM-D', color=p_util.clrgd)
            ax.bar(offsets[3], SsdPP, width=0.12, label='SmokedDuck', color=p_util.clrsd)
        for bar in range(5): # dummy bars
            offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
            # ax.bar(bar, 0.0, width=0.12)
            ax.bar(offsets[0], 0.0, width=0.12, label='GProM-P', color=p_util.clrgp)
            ax.bar(offsets[1], 0.0, width=0.12, label='SQLPROV', color=p_util.clrsp)
            ax.bar(offsets[2], 0.0, width=0.12, label='ProvSQL', color=p_util.clrpr)
            ax.bar(offsets[3], 0.0, width=0.12, label='SmokedDuck', color=p_util.clrsd)
            ax.bar(offsets[4], 0.0, width=0.12, label='GProM-D', color=p_util.clrgd)


        if id == 0 or id == 1 or id == 2:
            if id == 0 or id == 1:
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=5)
                leftBars = 3
            elif id == 2:
                offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=4)
                leftBars = 2
            current_ymin, current_ymax = ax.get_ylim()
            # ax.set_ylim(current_ymin, current_ymax * Y_INCREASE_RATIO)
            split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
            ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)
        ax.set_xticks([])
        ax.set_yscale('log')
        ax.set_xlabel(f'{subtitles[id]}', fontsize=FONT_SIZE - 10)

        # -- set edge color and line width for all spines
        # current_ymin, current_ymax = ax.get_ylim()
    for ax in axes.flatten():
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)
    axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
    axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
    axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)
    plt.tight_layout()
    plt.savefig(f'{os.getcwd()}/zackups/{savename}_pm_{sf}.png', bbox_inches='tight')



def plotLegend():
    fig, ax = plt.subplots(figsize=(FIG_WIDTH1 / 4, FIG_HEIGHT / 12))
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=p_util.clrgp),
        plt.Rectangle((0, 0), 1, 1, color=p_util.clrsp),
        plt.Rectangle((0, 0), 1, 1, color=p_util.clrpr),
        # plt.Rectangle((0, 0), 1, 1, color=p_util.clrgd),
        plt.Rectangle((0, 0), 1, 1, color=p_util.clrsd),
        # Line2D([0], [0], color=p_util.clrpg, linestyle='--', linewidth=4),
        Line2D([0], [0], color=p_util.clrdk, linestyle='--', linewidth=4)
    ]
    labels = ['GProM', 'SQLProv', 'ProvSQL', 'SmokedDuck', 'DB Execution']
    ax.legend(handles=handles, labels=labels, loc='center', ncol = 6,  fontsize=FONT_SIZE/2, frameon = False)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f'{os.getcwd()}/zackups/Fig_legend.png', bbox_inches='tight')

    plt.close()
    fig, ax = plt.subplots(figsize=(FIG_WIDTH1 / 4, FIG_HEIGHT / 12))
    ax.legend(handles=handles[:-1], labels=labels[:-1], loc='center', ncol = 6,  fontsize=FONT_SIZE/2, frameon = False)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f'{os.getcwd()}/zackups/Fig_legend_nodb.png', bbox_inches='tight')

def showColors():
    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=10)
    colors = [p_util.clrgp, p_util.clrsp, p_util.clrpr, p_util.clrgd, p_util.clrsd, p_util.clrpg, '#006400', '#800000', '#CD7F32', '#7A9A01']
    fig, ax = plt.subplots(figsize=(FIG_WIDTH1 * 1.8, FIG_HEIGHT))
    for i in range(len(colors)):
        plt.bar(offsets[i], 1, color=colors[i], width = 0.05)
    plt.savefig(f'{os.getcwd()}/zackups/colors.png', bbox_inches='tight')

def plotWHRSUB(sf,
         whichbench: list,
         benchQOrders: list,
         saveName: str,
         systems=['gprom', 'sqlprov', 'provsql', 'smokedduck'],
         subfigNumTitles: list = None,
         MarkerSize=20,
         Y_FLOOR=1e-3,
         Y_INCREASE_RATIO=1.0,
         Y_FLOOR2=1e-3,
         INCREASE_WIDTH=1.4,
         xticks: list = None,
         plot_all_phase = False):

    # -- gprom
    gpT = []
    gdT = []

    # -- add the below two for extra gproms
    gp2T = []
    gd2T = []

    gdS = []
    gpS = []
    gd2S = []
    gp2S = []


    # -- sqlprov
    spT1 = []
    spT2 = []
    spT = []
    spS = []

    # -- provsql
    prT = []
    prS = []

    # -- smokedduck
    sdT1 = []
    sdT2 = []
    sdT = []
    sdS = []

    # ----- Postgresql
    posts = []
    # ----- duckdb
    ducks = []

    if 'gprom' in systems:
        # -- time
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            gpT.append(dataT['gprom']['p']['times'][benchQOrders[index]])
            gdT.append(dataT['gprom']['d']['times'][benchQOrders[index]])

            # -- add 2T for postgresql and duckdb, since we have 6 queries, the
            # 4-6 belongs to 2T
            gp2T.append(dataT['gprom']['p']['times'][benchQOrders[index] + len(whichbench)])
            gd2T.append(dataT['gprom']['d']['times'][benchQOrders[index] + len(whichbench)])

        # -- storage
        for index in range(len(whichbench)):
            gpS.append(0.0)
            gdS.append(0.0)
            gp2S.append(0.0)
            gd2S.append(0.0)


    if 'sqlprov' in systems:
        # -- time
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            spT1.append(dataT['sqlprov']['1']['times'][benchQOrders[index]])
            spT2.append(dataT['sqlprov']['2']['times'][benchQOrders[index]])
            spT.append(spT1[-1] + spT2[-1])
        # -- storage
        for index in range(len(whichbench)):
            dataS = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}Storage.json')
            spS.append(dataS['sqlprov']['storage'][benchQOrders[index]])
    else:
        spT = [0.0 for _ in range(len(gpT))]
        spS = [0.0 for _ in range(len(gpT))]
    if 'smokedduck' in systems:
        # -- time
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            sdT1.append(dataT['smokedduck']['1']['times'][benchQOrders[index]])
            sdT2.append(dataT['smokedduck']['2']['times'][benchQOrders[index]])
            sdT.append(sdT1[-1] + sdT2[-1])
        # -- storage
        for index in range(len(whichbench)):
            dataS = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}Storage.json')
            sdS.append(dataS['smokedduck']['storage'][benchQOrders[index]])
    else:
        sdT = [0.0 for _ in range(len(gpT))]
        sdS = [0.0 for _ in range(len(gpT))]
    if 'provsql' in systems:
        # -- time
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            prT.append(dataT['provsql']['times'][benchQOrders[index]])
        # -- storage
        for index in range(len(whichbench)):
            dataS = f_util.loadJsonConfig(
                f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}Storage.json')
            prS.append(dataS['provsql']['storage'][benchQOrders[index]])
    else:
        prT = [0.0 for _ in range(len(gpT))]
        prS = [0.0 for _ in range(len(gpT))]

    if 'postgresql' in systems:
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            posts.append(dataT['postgresql']['times'][benchQOrders[index]])
    else:
        posts = [0.0 for _ in range(len(gpT))]

    if 'duckdb' in systems:
        for index in range(len(whichbench)):
            dataT = f_util.loadJsonConfig(f'{os.getcwd()}/zackups/{sf}/{whichbench[index]}.json')
            ducks.append(dataT['duckdb']['times'][benchQOrders[index]])
    else:
        ducks = [0.0 for _ in range(len(gpT))]

    BarNumbers = 0

    if 'gprom' in systems:
        BarNumbers += 4 # update to 4
    if 'sqlprov' in systems:
        BarNumbers += 1
    if 'provsql' in systems:
        BarNumbers += 1
    if 'smokedduck' in systems:
        BarNumbers += 1

    barWidth = (0.12 / (BarNumbers / 5))

    offsets = p_util.getBarDistributeOffsets(totalWidth=0.8, NBars=BarNumbers)
    fig, axes = plt.subplots(2, len(subfigNumTitles), figsize=(FIG_WIDTH1 * INCREASE_WIDTH, FIG_HEIGHT), sharey='row', gridspec_kw={ 'height_ratios': [3, 1], 'hspace': 0.0, 'wspace': 0 })
    gns = subfigNumTitles

    leftBars = 0
    if 'gprom' in systems:
        leftBars += 2 # update to 2
    if 'sqlprov' in systems:
        leftBars += 1
    if 'provsql' in systems:
        leftBars += 1 # added smd
    # Y_FLOOR = None
    # plot titmes

    (PN, DN) = getHowManyBars(systems)
    for id in range(len(subfigNumTitles)):
        # print(f'gn: {subfigNumTitles}, gpT: {gpT[id]}, spT: {spT[id]}, prT: {prT[id]}, gdT: {gdT[id]}, sdT: {sdT[id]}, posts: {posts[id]}, ducks: {ducks[id]}')

        print(f'offset: {offsets[id]}, posts: {posts[id]}, ducks: {ducks[id]}')
        ax = axes[0][id]
        barPos = 0
        leftLineStart = 0
        if 'gprom' in systems:
            ax.bar(offsets[barPos], gpT[id], width=barWidth,
                   bottom=Y_FLOOR, label='GProM-P', color=p_util.clrgp, hatch = '/')
            barPos += 1

            # ax.plot(offsets[barPos], posts[id], marker=p_util.postmarker, linewidth = LINE_WIDTH, linestyle = '--', color = p_util.clrpg)
            ax.bar(offsets[barPos], gp2T[id], width=barWidth,
                   bottom=Y_FLOOR, label='GProM-P', color=p_util.clrgp)
            barPos += 1
        if 'sqlprov' in systems:
            if plot_all_phase:
                ax.bar(offsets[barPos], spT[id], width=barWidth, bottom=Y_FLOOR, label='SQLProv', color=p_util.clrsp)
                ax.text(offsets[barPos], spT[id], s=f'{int(spT1[id]/spT[id]*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
            else:
                ax.bar(offsets[barPos], spT1[id], width=barWidth,bottom = Y_FLOOR, label = 'SQLProv', color = p_util.clrsp)

            barPos += 1
        if 'provsql' in systems:
            ax.bar(offsets[barPos], prT[id], width=barWidth,
                   bottom=Y_FLOOR, label='ProvSQL', color=p_util.clrpr)
            barPos += 1
        LeftLineEnd = barPos - 1


        ax.hlines(y = posts[id], xmin = offsets[leftLineStart] - barWidth / 2, xmax = offsets[LeftLineEnd] + barWidth / 2, colors = p_util.clrpg, linestyles = '--', linewidth = LINE_WIDTH, label='PostgreSQL')


        RightLineStart = LeftLineEnd + 1
        if 'gprom' in systems:
            ax.bar(offsets[barPos], gdT[id], width=barWidth,
                   bottom=Y_FLOOR, label='GProM-D', color=p_util.clrgd, hatch = '/')
            # ax.plot(offsets[barPos], ducks[id], marker=p_util.duckmarker, linewidth = LINE_WIDTH, linestyle = '--', color = p_util.clrdk)

            barPos += 1
            ax.bar(offsets[barPos], gd2T[id], width=barWidth,
                   bottom=Y_FLOOR, label='GProM-D', color=p_util.clrgd)
            barPos += 1
        if 'smokedduck' in systems:
            if plot_all_phase:
                ax.bar(offsets[barPos], sdT[id], width=barWidth, bottom=Y_FLOOR, label='SmokedDuck', color=p_util.clrsd)
                ax.text(offsets[barPos], sdT[id], s=f'{int(sdT1[id]/sdT[id]*100)}%', ha='center', va='bottom', fontsize=FONT_SIZE-8, color='blue')
            else:
                ax.bar(offsets[barPos], sdT1[id], width=barWidth, bottom=Y_FLOOR, label='SmokedDuck', color=p_util.clrsd, hatch = '/')

            barPos += 1
        RightLineEnd = barPos - 1
        ax.hlines(y = ducks[id], xmin = offsets[RightLineStart] - barWidth/ 2, xmax = offsets[RightLineEnd] + barWidth / 2, colors = p_util.clrdk, linestyles = '--', linewidth = LINE_WIDTH, label='DuckDB')

        # -- show grid
        if SHOW_GRID:
            ax.grid(True, which='major', axis='y', linestyle='--')
            ax.set_axisbelow(True)
        # -- set ticks to None
        ax.set_xticks([])
        # -- set y scale to log
        ax.set_yscale('log')

        # -- line separator for postgreSQL and duckDB
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)

        # -- text for postgreSQL and duckDB
        # -- y increase to fit the text
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
    # -- plot storage
    for id in range(len(subfigNumTitles)):
        ax = axes[1][id]
        barPos = 0
        if 'gprom' in systems:
            ax.bar(offsets[barPos], gpS[id], width=barWidth,
                   bottom=Y_FLOOR2, label='GProM w/o Sub', color=p_util.clrgp)
            barPos += 1
            ax.bar(offsets[barPos], gp2S[id], width=barWidth,
                   bottom=Y_FLOOR2, label='GProM w/ Sub', color=p_util.clrgp)
            barPos += 1

        if 'sqlprov' in systems:
            ax.bar(offsets[barPos], spS[id], width=barWidth,
                   bottom=Y_FLOOR2, label='SQLProv w/o Sub', color=p_util.clrsp)
            barPos += 1
        if 'provsql' in systems:
            ax.bar(offsets[barPos], prS[id], width=barWidth,
                   bottom=Y_FLOOR2, label='ProvSQL', color=p_util.clrpr)
            barPos += 1
        if 'gprom' in systems:
            ax.bar(offsets[barPos], gdS[id], width=barWidth,
                   bottom=Y_FLOOR2, label='GProM w/o Sub', color=p_util.clrgd)
            barPos += 1
            
            ax.bar(offsets[barPos], gp2S[id], width=barWidth,
                   bottom=Y_FLOOR2, label='GProM w/ Sub', color=p_util.clrgp)
            barPos += 1
        if 'smokedduck' in systems:
            ax.bar(offsets[barPos], sdS[id], width=barWidth,
                   bottom=Y_FLOOR2, label='SmokedDuck', color=p_util.clrsd)
            barPos += 1
        if xticks is not None:
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticks, fontsize=FONT_SIZE)
        else:
            ax.set_xticks([])
        ax.set_yscale('log')
        print(f"LEFT BARS?? {leftBars}")
        split_post = (offsets[leftBars-1] + offsets[leftBars]) / 2
        ax.axvline(x=split_post, color=p_util.clrsep, linestyle=p_util.stysep, linewidth=LINE_WIDTH)

        # ax.invert_yaxis()
        ax.set_xlabel(f'{gns[id]}', fontsize=FONT_SIZE)
        # -- set edge color and line width for all spines
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(LINE_WIDTH)
    axes[0][0].set_ylabel('Runtime (Sec)', fontsize=FONT_SIZE)
    axes[0][0].tick_params(axis='y', labelsize=FONT_SIZE)
    axes[1][0].set_ylabel('Storage\n(MB)', fontsize=FONT_SIZE)
    axes[1][0].tick_params(axis='y', labelsize=FONT_SIZE)
    # plt.legend()
    plt.tight_layout()

    plt.savefig(f'{os.getcwd()}/zackups/{saveName}_{sf}.png',
                bbox_inches='tight')
    plt.close()

def plotLegendWHRSUB():
    import matplotlib
    print(matplotlib.__version__)
    fig, ax = plt.subplots(figsize=(FIG_WIDTH1, FIG_HEIGHT))
    # handles = [
    #     plt.Rectangle((0, 0), 1, 1, color=p_util.clrgp),
    #     plt.Rectangle((0, 0), 1, 1, color=p_util.clrsp),
    #     # plt.Rectangle((0, 0), 1, 1, color=p_util.clrpr),
    #     # plt.Rectangle((0, 0), 1, 1, color=p_util.clrgd),
    #     # plt.Rectangle((0, 0), 1, 1, color=p_util.clrsd),
    #     # Line2D([0], [0], color=p_util.clrpg, linestyle='--', linewidth=4),
    #     Line2D([0], [0], color=p_util.clrdk, linestyle='--', linewidth=4),
    #     plt.Rectangle((0, 0), 1, 1, color=p_util.clrgp, hatch = '//'),

    # ]
    handles = [
        Patch(facecolor=p_util.clrgp, edgecolor='black', hatch='/', linewidth=0),
        Patch(facecolor=p_util.clrsd, edgecolor='black', hatch='/', linewidth=0),
        Patch(facecolor=p_util.clrgp, edgecolor='black', linewidth=0),
        Patch(facecolor=p_util.clrsp, edgecolor='black', linewidth=0),
        Line2D([0], [0], color=p_util.clrdk, linestyle='--', linewidth=4),
    ]
    labels = ['GProM w/ Sub. Prov.','SmokedDuck w/ Sub. Prov.', 'GProM w/o Sub. Prov.', 'SQLProv w/o Sub. Prov.', 'DB Execution']
    ax.legend(handles=handles, labels=labels, loc='center', ncol = 3,  fontsize=FONT_SIZE/1.5, frameon = False)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f'{os.getcwd()}/zackups/Fig_legend_qwhrsub.png', bbox_inches='tight')



if __name__ == '__main__':
    if PLOTTED_LEGEND:
        plotLegend()
        plotLegendWHRSUB()
    # plot(sf='sf1', whichbench=['FPAgg', 'FPAgg', 'FPAgg'], benchQOrders=[0, 1, 2], saveName='Fig_fpagg',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'provsql', 'smokedduck'], subfigNumTitles=['1M', '10K', '10'], Y_FLOOR=None, Y_INCREASE_RATIO=1.1)
    # plot(sf='sf1', whichbench=['FPDist', 'FPDist', 'FPDist'], benchQOrders=[0, 1, 2], saveName='Fig_fpdist',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'provsql', 'smokedduck'], subfigNumTitles=['1M', '10K', '10'], Y_FLOOR=None, Y_INCREASE_RATIO=1.4)
    # plot(sf='sf1', whichbench=['VPJC', 'VPJC', 'VPJC'], benchQOrders=[0, 1, 2], saveName='Fig_vpjc',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck', 'provsql'], subfigNumTitles=['1-1', '1-10', '1-50'], Y_FLOOR=None, Y_INCREASE_RATIO=5.5)
    # plot(sf='sf1', whichbench=['VPJS', 'VPJS', 'VPJS'], benchQOrders=[0, 1, 2], saveName='Fig_vpjs',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck', 'provsql'], subfigNumTitles=['1%', '10%', '50%'], Y_FLOOR=None, Y_INCREASE_RATIO=4.6)
    # plot(sf='sf1', whichbench=['VPGN', 'VPGN', 'VPGN'], benchQOrders=[0, 1, 2], saveName='Fig_vpgn',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck', 'provsql'], subfigNumTitles=['100', '1k', '10k'], Y_FLOOR=None, Y_INCREASE_RATIO=5.5)
    # plot(sf='sf1', whichbench=['VPGS', 'VPGS', 'VPGS'], benchQOrders=[0, 1, 2], saveName='Fig_vpgs',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck', 'provsql'], subfigNumTitles=['100', '1k', '10k'], Y_FLOOR=None, Y_INCREASE_RATIO=5.5)
    # plot(sf='sf1', whichbench=['QTopK2', 'QTopK2', 'QTopK2', 'QTopK2'], benchQOrders=[0, 1, 2, 3], saveName='Fig_fpqtopk',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck'], subfigNumTitles=['Top 0.1%', 'Top 1%', 'Top 10%', 'Top50%'], Y_FLOOR=None, Y_INCREASE_RATIO=1.25, plot_all_phase = True)
    # plot(sf='sf1', whichbench=['VPJS', 'VPJJ', 'VPJJJ'], benchQOrders=[1, 0, 0], saveName='Fig_vpjn', systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck', 'provsql'], subfigNumTitles=['One Join', 'Two Joins', 'Three Joins'], Y_FLOOR=None, Y_INCREASE_RATIO=3)
    # plot(sf='sf1', whichbench=['FPAgg', 'QAggNum', 'QAggNum'], benchQOrders=[1, 0, 1], saveName='Fig_qaggnum', systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck', 'provsql'], subfigNumTitles=['2 Aggregation', '4 Aggregation', '8 Aggregation'], Y_FLOOR=1e-2, Y_INCREASE_RATIO=3)
#---###disabled    plot(sf='sf1', whichbench=['FPSAgg', 'FPSAgg', 'FPSAgg'], benchQOrders=[0, 1, 2], saveName='Fig_qhavingJF',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck', 'provsql'], subfigNumTitles=['10% Filter In', '50% Filter In', '100% Filter In'], Y_FLOOR=2*1e-2, Y_INCREASE_RATIO=1.5, plot_all_phase = True)
#---###disabled    plot(sf='sf1', whichbench=['FPSAgg', 'FPSAgg', 'FPSAgg'], benchQOrders=[3, 4, 5], saveName='Fig_qhavingFJ',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck'], subfigNumTitles=['10% Filter In', '50% Filter In', '100% Filter In'], Y_FLOOR=1e-2, Y_INCREASE_RATIO=1.8)
    # plot(sf='sf1', whichbench=['FPSAgg', 'FPSAgg'], benchQOrders=[0, 2], saveName='Fig_qAJ_JA_10groups',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck'], subfigNumTitles=['Join Then Aggregation', 'Aggregation Then Join'], Y_FLOOR=3* 1e-2, Y_INCREASE_RATIO=1.3)
    # plot(sf='sf1', whichbench=['FPSAgg', 'FPSAgg'], benchQOrders=[1, 3], saveName='Fig_qAJ_JA_1kgroups',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck'], subfigNumTitles=['Join Then Aggregation', 'Aggregation Then Join'], Y_FLOOR=3* 1e-2, Y_INCREASE_RATIO=1.3)
#---###disabled    plot(sf='sf1', whichbench=['FPSAgg', 'FPSAgg'], benchQOrders=[0, 3], saveName='Fig_qhavingcmp10',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck'], subfigNumTitles=['Join Then Aggregation', 'Aggregation Then Join'], Y_FLOOR=3* 1e-2, Y_INCREASE_RATIO=10.8)
    # plot(sf='sf1', whichbench=['QCMPLDC', 'QCMPLDC', 'QCMPLDC'], benchQOrders=[0, 1, 2], saveName='Fig_qcmpldc',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck', 'provsql'], subfigNumTitles=['1 block', '2 Blocks', '3 Blocks'], Y_FLOOR=None, Y_INCREASE_RATIO=1.9)
    # plot(sf='sf1', whichbench=['QARGMIN', 'QARGMIN'], benchQOrders=[0, 1], saveName='Fig_qargmin',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck'], subfigNumTitles=['100 Groups', '1K Groups'], Y_FLOOR=None, Y_INCREASE_RATIO=5.7)
    # plot(sf='sf1', whichbench=['QLIMIT', 'QLIMIT', 'QLIMIT'], benchQOrders=[0, 1, 2], saveName='Fig_qlimit',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck', 'provsql'], subfigNumTitles=['Limit 0.1%', 'Limit 1%', 'Limit 10%'], Y_FLOOR=None, Y_INCREASE_RATIO=1.7)
    # plot(sf='sf1', whichbench=['QMLAgg', 'QMLAgg'], benchQOrders=[0, 1], saveName='Fig_qmlagg',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck'], subfigNumTitles=['1K Groups', '1M Groups'], Y_FLOOR=None, Y_INCREASE_RATIO=4.7)
    # plotSPOnly(sf='sf1', whichbench=['QWIN', 'QWIN', 'QWIN'], benchQOrders=[0, 1, 2], saveName='Fig_qwin',systems=['sqlprov', 'postgresql'], subfigNumTitles=['W/O partition', 'W/ partition (10)', 'W/ partition (1K)'], Y_FLOOR=3, Y_FLOOR2=0,Y_INCREASE_RATIO=1.2)
    # plotSPOnly(sf='sf1', whichbench=['QRCRW', 'QRCRW'], benchQOrders=[0, 1], saveName='Fig_qrcrw',systems=['sqlprov', 'postgresql'], subfigNumTitles=['Depth: 2', 'Depth: 3'], Y_FLOOR=2 * 1e-2, Y_FLOOR2=1e-1,Y_INCREASE_RATIO=15)
    # plot(sf='sf1', whichbench=['QSET', 'QSET', 'QSET'], benchQOrders=[0, 1, 2], saveName='Fig_qset',systems=['postgresql', 'duckdb', 'gprom', 'smokedduck', 'provsql'], subfigNumTitles=['Data Remove: 10%', 'Data Remove: 50%', 'Data Remove: 100%'], Y_FLOOR=1.2 * 1e-1, Y_FLOOR2=11,Y_INCREASE_RATIO=1.2)
#- 
    # plotProvPoly(sf = 'sf1', saveName='Fig_PP', subfigureTitles=['One Join', 'Two Joins', 'Three Joins', 'Join(10%) Agg.', 'Join(50%) Agg.'], whichbench='PP', benchQOrders=0, Y_FLOOR = 1.1 * 1e-1, Y_INCREASE_RATIO=1.7, Y_FLOOR2= 2)
    # plotApproProv(sf = 'sf1', saveName='Fig_AP', subfigureTitles=['10 Ranges', '100 Ranges', '500 Ranges'], whichbench='PP', benchQOrders=0, Y_INCREASE_RATIO=1.7, Y_FLOOR=1e-2)
#- 
#-     # -- join then distinct
    # plot(sf='sf1', whichbench=['FPSDist', 'FPSDist', 'FPSDist'], benchQOrders=[0, 1, 2], saveName='Fig_fsdistjd1',systems=['postgresql', 'duckdb', 'sqlprov', 'gprom', 'provsql'], subfigNumTitles=['1:1', '1:50', '1:1k'], Y_FLOOR=1e-3, Y_INCREASE_RATIO=1.5, SECOND_SYS_START_POST=0.87)
    # plot(sf='sf1', whichbench=['FPSDist', 'FPSDist'], benchQOrders=[3, 4], saveName='Fig_fsdistjd50',systems=['postgresql', 'duckdb', 'sqlprov', 'gprom', 'provsql'], subfigNumTitles=['50:50', '50:1k'], Y_FLOOR=5* 1e-3, Y_INCREASE_RATIO=1.5, Y_FLOOR2=100, SECOND_SYS_START_POST=0.87)
    # plot2(sf='sf1', whichbench=['FPSDist'], benchQOrders=[8], saveName='Fig_fsdistjd1k',systems=['postgresql', 'duckdb', 'sqlprov', 'gprom', 'provsql'], subfigNumTitles=['1k:1k'], Y_FLOOR=1e-3, Y_INCREASE_RATIO=1.2)
#-     # -- distinct then join distinct
    # plot(sf='sf1', whichbench=['FPSDist', 'FPSDist', 'FPSDist'], benchQOrders=[9, 10, 11], saveName='Fig_fsdistdj1',systems=['postgresql', 'duckdb', 'sqlprov', 'gprom', 'provsql'], subfigNumTitles=['1:1', '1:50', '1:1k'], Y_FLOOR=3*1e-4, Y_INCREASE_RATIO=1.2, SECOND_SYS_START_POST= 0.87)
    # plot(sf='sf1', whichbench=['FPSDist', 'FPSDist'], benchQOrders=[13, 14], saveName='Fig_fsdistdj50',systems=['postgresql', 'duckdb', 'sqlprov', 'gprom', 'provsql'], subfigNumTitles=['50:50', '50:1k'], Y_FLOOR=3*1e-4, Y_INCREASE_RATIO=1.2, Y_FLOOR2=1e-2, SECOND_SYS_START_POST= 0.87)
    # plot2(sf='sf1', whichbench=['FPSDist'], benchQOrders=[17], saveName='Fig_fsdistdj1k', systems=['postgresql', 'duckdb', 'sqlprov', 'gprom', 'provsql'], subfigNumTitles=['1k:1k'], Y_FLOOR=4*1e-4, Y_INCREASE_RATIO=1.1, Y_FLOOR2 = 1e-2)
#-     # --
    # plot(sf='sf1', whichbench=['FPSDist', 'FPSDist', 'FPSDist', 'FPSDist'], benchQOrders=[3, 12, 4, 13], saveName='Fig_fsdistcmp50', systems=['postgresql', 'duckdb', 'sqlprov', 'gprom', 'provsql'], subfigNumTitles=['50:50 Join First', '50:50 Distinct First', '50:1k Join First', '50:1k Distinct First'], Y_FLOOR=4*1e-4, Y_INCREASE_RATIO=1.2,INCREASE_WIDTH = 1.5, SECOND_SYS_START_POST = 0.87)
#     plot(sf='sf1', whichbench=['FPSDist', 'FPSDist'], benchQOrders=[8, 17], saveName='Fig_fsdistcmp1k', systems=['postgresql', 'duckdb', 'sqlprov', 'gprom', 'provsql'], subfigNumTitles=['1k:1k Join First', '1k:1k Distinct First'], Y_FLOOR=4*1e-4, Y_INCREASE_RATIO=1.2,INCREASE_WIDTH = 1.5)
    # plot(sf='sf1', whichbench=['FPSDist', 'FPSDist', 'FPSDist', 'FPSDist'], benchQOrders=[0, 1, 9, 10,], saveName='Fig_fsdistcmp1',  systems=['postgresql', 'duckdb', 'sqlprov', 'gprom', 'provsql'], subfigNumTitles=['1:1 Join First', '1:1 Distinct First', '1:50 Join First', '1:50 Distinct First'], Y_FLOOR=3*1e-4, Y_INCREASE_RATIO=1.3,INCREASE_WIDTH = 1.5, SECOND_SYS_START_POST=0.87)
#- 
    # plotsrd2(sf='sf1', saveName='Fig_PMRLIN2_WITMIN', subfigureTitles=['End-to-end', 'Capture', 'Query', 'Reproduce'], wichbench='PMRLIN2', benchQOrders=0, isRL=True, Y_INCREASE_RATIO=1.2, Y_FLOOR = 1.1*1e-3, Y_FLOOR2= 1.1 * 1e-1, hasSMD = True, GPSS = 0.57, GDSS = 1.0)
    # plotsrd2(sf='sf1', saveName='Fig_PMRLIN2_WITP1',  subfigureTitles=['End-to-end', 'Capture', 'Query', 'Reproduce'], wichbench='PMRLIN2', benchQOrders=1, isRL=True, Y_INCREASE_RATIO=1.2, Y_FLOOR=1.1 *1e-2,  Y_FLOOR2 = 1.1,  hasSMD = True, GPSS = 7, GDSS = 1.7)
    # plotsrd2(sf='sf1', saveName='Fig_PMRLIN2_WITP20', subfigureTitles=['End-to-end', 'Capture', 'Query', 'Reproduce'], wichbench='PMRLIN2', benchQOrders=2, isRL=True, Y_INCREASE_RATIO=1.2, Y_FLOOR=5* 1e-2, Y_FLOOR2= 11, hasSMD = True, GPSS = 130.71, GDSS = 15.7)
    # plotsrd2(sf='sf1', saveName='Fig_PMRLIN2_FL',     subfigureTitles=['End-to-end', 'Capture', 'Query', 'Reproduce'], wichbench='PMRLIN2', benchQOrders=0, isRL=False, Y_INCREASE_RATIO=1.2, Y_FLOOR= 5* 1e-1, Y_FLOOR2= 12, hasSMD = True, GPSS = 651.55, GDSS = 163)

    # plotDBG(sf = 'sf1', savename='Fig_BD', subfigureTitles=['Query Provenance', 'Data Affected 1%', 'Data Affected 10%', 'DataAffected 50%', 'DataAffected 90%'], whichbench='DBG', benchQOrders=0, isRL=True, Y_INCREASE_RATIO=1.5, Y_FLOOR=4*1e-3, SECOND_SYS_START_POST = 0.845)
    # plotFBG(sf = 'sf1', savename='Fig_pmfdq1', subfigureTitles=['Query Provenance', 'Data Affected 1%', 'Data Affected 10%', 'DataAffected 50%', 'DataAffected 90%'], whichbench='FBGQ1', benchQOrders=0, isRL=True, Y_INCREASE_RATIO=1.5, Y_FLOOR=1e-5, SECOND_SYS_START_POST = 0.845)
    # plotFBG(sf = 'sf1', savename='Fig_pmfdq2', subfigureTitles=['Query Provenance', 'Data Affected 1%', 'Data Affected 10%', 'DataAffected 50%', 'DataAffected 90%'], whichbench='FBGQ2', benchQOrders=1, isRL=True, Y_INCREASE_RATIO=1.5, Y_FLOOR=1e-5, SECOND_SYS_START_POST = 0.845)
    # plotFBG(sf = 'sf1', savename='Fig_pmfdq3', subfigureTitles=['Query Provenance', 'Data Affected 1%', 'Data Affected 10%', 'DataAffected 50%', 'DataAffected 90%'], whichbench='FBGQ3', benchQOrders=2, isRL=True, Y_INCREASE_RATIO=1.5, Y_FLOOR=1e-5, SECOND_SYS_START_POST = 0.845)

    # plotPM(sf = 'sf1', savename='Fig_PM', subfigureTitles=['Lineage', f'Minimal Witnesses', f'Provenance Polynomial', f'Approximate Provenance'], whichbench='PM', benchQOrders=0, isRL=True, Y_INCREASE_RATIO=1.5, Y_FLOOR=4* 1e-3)

    plotWHRSUB(sf='sf1', whichbench=['QWHRSUB', 'QWHRSUB', 'QWHRSUB'], benchQOrders=[0, 1, 2], saveName='Fig_qwhrsub',systems=['postgresql', 'duckdb', 'gprom', 'sqlprov', 'smokedduck'], subfigNumTitles=['1 Subquery', '2 Subqueries', '3 Subqueries'], Y_FLOOR=1.2 * 1e-3, Y_FLOOR2=1e-0,Y_INCREASE_RATIO=2.5)
