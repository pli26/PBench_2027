from utils import fileUtils as f_util
import statistics as sta
import re

def getMedianPostgresql(filepath, removeFirst=f_util.removeTopN):
    time = 0.0
    variance = 0.0

    tmpTimes = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if len(line) > len('Execution Time') and 'Execution Time' in line:
                timeValue = line.strip().split(':')[1].strip()
                if timeValue.endswith('ms'):
                    timeValue = timeValue[:-2].strip()
                else:
                    print(f"Unexpected time format: {timeValue}")
                    exit()
                time = float(timeValue) / 1000
                tmpTimes.append(float(timeValue) / 1000)
    if len(tmpTimes) == 0:
        f_util.appendToFile('./zackups/genlogs.txt', f"Warning: No valid execution times found in file {filepath}. Returning (0.0, 0.0).\n")
        print(f"Warning: No valid execution times found in file {filepath}. Returning (0.0, 0.0).")
        return (0.0, 0.0)
    tmpTimes = tmpTimes[removeFirst:]
    if len(tmpTimes) == 0:
        f_util.appendToFile('./zackups/genlogs.txt', f"Warning: No valid execution times left after removing the first {removeFirst} entries in file {filepath}. Returning (0.0, 0.0).\n")
        print(f"Warning: No valid execution times left after removing the first {removeFirst} entries in file {filepath}. Returning (0.0, 0.0).")
        return (0.0, 0.0)
    time = sta.median(tmpTimes)

    variance = sta.variance(tmpTimes)
    return (time, variance)


def getMedianDuckdb(filepath, removeFirst=f_util.removeTopN):
    time = 0.0
    varianbce = 0.0

    tmpTimes = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if len(line) > len('Total Time:') and 'Total Time:' in line:
                match = re.search(r'Total Time:\s*([\d.]+)s', line)
                if match:
                    timeValue = match.group(1)
                else:
                    print(f"Unexpected time format in line: {line}")
                    exit()
                time = float(timeValue)
                tmpTimes.append(float(timeValue))
    if len(tmpTimes) == 0:
        f_util.appendToFile('./zackups/genlogs.txt', f"Warning: No valid execution times found in file {filepath}. Returning (0.0, 0.0).\n")
        print(f"Warning: No valid execution times found in file {filepath}. Returning (0.0, 0.0).")
        return (0.0, 0.0)
    tmpTimes = tmpTimes[removeFirst:]
    time = sta.median(tmpTimes)
    variance = sta.variance(tmpTimes)
    return (time, variance)

def getMedianDuckdbSpecial(filepath, identifier: str, theNTh, removeFirst=f_util.removeTopN):
    time = 0.0
    varianbce = 0.0

    tmpTimes = []
    Seen = False
    nth = 0
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if len(line) > len(identifier) and identifier in line:
                Seen = True
                nth = 0
                # print(f"Found identifier '{identifier}' in line: {line.strip()}")
            if len(line) > len('Run Time (s):') and 'Run Time (s):' in line:
                if Seen == True:
                    nth += 1
                    # print(f"Found 'Run Times (s):' in line: {line.strip()} (nth={nth})")
            if Seen == True and nth == theNTh:
                aLine = line.strip().split(':')[1].strip()

                timeValue = aLine.split(' ')[1].strip()
                # print(timeValue)
                tmpTimes.append(float(timeValue))
                Seen = False
                nth = 0

    if len(tmpTimes) == 0:
        f_util.appendToFile('./zackups/genlogs.txt', f"Warning: No valid execution times found in file {filepath}. Returning (0.0, 0.0).\n")
        print(f"Warning: No valid execution times found in file {filepath}. Returning (0.0, 0.0).")
        return (0.0, 0.0)
    tmpTimes = tmpTimes[removeFirst:]
    time = sta.median(tmpTimes)
    variance = sta.variance(tmpTimes)
    return (time, variance)