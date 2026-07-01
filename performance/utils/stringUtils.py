
def buildSQLFromTemplate(template: str, toReplace: list, replaceWith: list) -> str :
    sql = template
    for i in range(len(toReplace)):
        sql = sql.replace(toReplace[i], replaceWith[i])
    return sql

def writeStrToFile(string: str, filePath: str):
    with open(filePath, 'w') as f:
        f.write(string)

def partitionToFrag(start, end, numPartitions):
    partitionSize = (end - start) // numPartitions
    partitions = []
    for i in range(numPartitions):
        lower = start + i * partitionSize
        upper = start + (i + 1) * partitionSize if i != numPartitions - 1 else end
        partitions.append((lower, upper))

    print(partitions)
    return partitions