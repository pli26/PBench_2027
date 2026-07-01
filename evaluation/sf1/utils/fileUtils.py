import json

SYS_GProM = 'gprom'
SYS_ProvSQL = 'provsql'
SYS_SmokedDuck = 'smokedduck'
SYS_Links = 'links'
SYS_SQLProv = 'sqlprov'

removeTopN = 2


def resStructures():
    res = {}
    res[SYS_GProM] = {
        "p": {
            "sf1": {"times": [], "variances": []},
            "sf2": {"times": [], "variances": []},
            "sf10": {"times": [], "variances": []},
            "sf20": {"times": [], "variances": []}
        },
        "d": {
            "sf1": {"times": [], "variances": []},
            "sf2": {"times": [], "variances": []},
            "sf10": {"times": [], "variances": []},
            "sf20": {"times": [], "variances": []}
        }
    }
    res[SYS_SmokedDuck] = {
        "1": {
            "sf1": {"times": [], "variances": []},
            "sf2": {"times": [], "variances": []},
            "sf10": {"times": [], "variances": []},
            "sf20": {"times": [], "variances": []}
        },
        "2": {
            "sf1": {"times": [], "variances": []},
            "sf2": {"times": [], "variances": []},
            "sf10": {"times": [], "variances": []},
            "sf20": {"times": [], "variances": []}
        }
    }
    res[SYS_SQLProv] = {
        "1": {
            "sf1": {"times": [], "variances": []},
            "sf2": {"times": [], "variances": []},
            "sf10": {"times": [], "variances": []},
            "sf20": {"times": [], "variances": []}
        },
        "2": {
            "sf1": {"times": [], "variances": []},
            "sf2": {"times": [], "variances": []},
            "sf10": {"times": [], "variances": []},
            "sf20": {"times": [], "variances": []}
        }
    }

    res[SYS_ProvSQL] = {
        "sf1": {"times": [], "variances": []},
        "sf2": {"times": [], "variances": []},
        "sf10": {"times": [], "variances": []},
        "sf20": {"times": [], "variances": []}
    }

    res[SYS_Links] = {
        "sf1": {"times": [], "variances": []},
        "sf2": {"times": [], "variances": []},
        "sf10": {"times": [], "variances": []},
        "sf20": {"times": [], "variances": []}
    }

    return res

def appendToFile(filename, content):
    with open(filename, 'a') as f:
        f.write(content)

def loadJsonConfig(jsonPath):
    with open(jsonPath, 'r') as f:
        jsonFile = json.load(f)
    return jsonFile

def getDataFromJson(sys, sf, whichBench):
    data = loadJsonConfig(f'./zackups/{whichBench}.json')
    if sys == f_util.SYS_GProM:
        gd = data[sys]["d"][sf]
        gp = data[sys]["p"][sf]
        return (gd, gp)
    elif sys == f_util.SYS_SmokedDuck or sys == f_util.SYS_SQLProv:
        p1 = data[sys]["1"][sf]
        p2 = data[sys]["2"][sf]
        return (p1, p2)
    else:
        return data[sys][sf]