import os
import statistics

def parse_result_file(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    times = []
    for line in lines:
        if 'Execution Time: ' in line:
            time = line.strip().split(' ')[2].strip()
            print(time)
            times.append(((float) (time)) / 1000)
    return times

def get_median(filename, removeFirst = 3):
    times = parse_result_file(filename)
    Times = times[removeFirst:]
    return statistics.median(Times)

def get_statistics(filename, removeFirst = 3):
    times = parse_result_file(filename)
    Times = times[removeFirst:]
    median = statistics.median(Times)
    variance = statistics.variance(Times)

    return (median, variance)











# if __name__ == '__main__':
