









import os


def cal(belowPercent, alist: list):
    Len = len(alist)
    cnt = 0
    for val in alist:
        if val <= belowPercent:
            cnt += 1

    return (cnt, len(alist))

def calB(belowPercent, blist):
    Len = 0
    cnt = 0
    for l in blist:
        Len += len(l)
        for val in l:
            if val <= belowPercent:
                cnt += 1

    return (cnt, Len)



ff = open (f'{os.getcwd()}/ana.md')
lines = ff.readlines()
ff.close()

gprom = []
smd = []
pr = []
sp = []
pos = []
duck = []

for line in lines:
    if ":" in line:
        Ls = line.split(':')
        sys = Ls[0].strip().replace('-', ' ').strip()
        val = Ls[1].strip().replace(',', ' ').strip()
        if sys == 'GProM':
            gprom.append(float(val))
        if sys == 'PostgreSQL':
            pos.append(float(val))
        if sys == 'SmokedDuck':
            smd.append(float(val))
        if sys == 'SQLProv':
            sp.append(float(val))
        if sys == 'DuckDB':
            duck.append(float(val))
        if sys == 'ProvSQL':
            pr.append(float(val))


belowP1 = 0.01
print(f"############################################\n## below {belowP1}\n############################################\n")
(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, gprom)
print(f'gprom below {belowP1 * 100}%: {float(cnt / Len)}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, smd)
print(f'smokedduck below {belowP1 * 100}%: {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, pr)
print(f'provsql below {belowP1 * 100} %: {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, sp)
print(f'muller below {belowP1 * 100} % : {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, pos)
print(f'postgresql below {belowP1 * 100}%: {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, duck)
print(f'duckdb below {belowP1 * 100}%: {cnt / Len}')

belowP1 = 0.05
print(f"############################################\n## below {belowP1}\n############################################\n")

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, gprom)
print(f'gprom below {belowP1 * 100}%: {float(cnt / Len)}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, smd)
print(f'smokedduck below {belowP1 * 100}%: {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, pr)
print(f'provsql below {belowP1 * 100} %: {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, sp)
print(f'muller below {belowP1 * 100} % : {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, pos)
print(f'postgresql below {belowP1 * 100}%: {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, duck)
print(f'duckdb below {belowP1 * 100}%: {cnt / Len}')


belowP1 = 0.1
print(f"############################################\n## below {belowP1}\n############################################\n")

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, gprom)
print(f'gprom below {belowP1 * 100}%: {float(cnt / Len)}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, smd)
print(f'smokedduck below {belowP1 * 100}%: {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, pr)
print(f'provsql below {belowP1 * 100} %: {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, sp)
print(f'muller below {belowP1 * 100} % : {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, pos)
print(f'postgresql below {belowP1 * 100}%: {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, duck)
print(f'duckdb below {belowP1 * 100}%: {cnt / Len}')


belowP1 = 0.2
print(f"############################################\n## below {belowP1}\n############################################\n")

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, gprom)
print(f'gprom below {belowP1 * 100}%: {float(cnt / Len)}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, smd)
print(f'smokedduck below {belowP1 * 100}%: {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, pr)
print(f'provsql below {belowP1 * 100} %: {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, sp)
print(f'muller below {belowP1 * 100} % : {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, pos)
print(f'postgresql below {belowP1 * 100}%: {cnt / Len}')

(cnt, Len) = (0.0, 0.0)
(cnt, Len) = cal(belowP1, duck)
print(f'duckdb below {belowP1 * 100}%: {cnt / Len}')

belowP1 = 0.01
print(f"############################################\n## below {belowP1}\n############################################\n")
(cnt, Len) = calB(0.01, [gprom, smd, pr, sp, pos, duck])
print(f'all below {belowP1 * 100}%: {cnt / Len}')


import json

def find_key(obj, target):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == target:
                yield v
            yield from find_key(v, target)

    elif isinstance(obj, list):
        for item in obj:
            yield from find_key(item, target)
def collect_var_time(obj, path=""):
    results = {}

    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key

            if key == "var-time":
                results[path] = value
            else:
                results.update(collect_var_time(value, new_path))

    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            results.update(collect_var_time(item, f"{path}[{i}]"))

    return results

benches = []

benches = ['FPAgg.json', 'FPDist.json', 'FPSAgg.json', 'FPSDist.json', 'PSDistSTORAGE.json', 'PMAP_bk.json', 'MAP.json', 'PMBD_gp.json', 'MBD_sppr.json', 'PMBDSTORAGE.json', 'MFD_gp.json', 'PMFD_sppr.json', 'MFD2.json', 'PMFD2STORAGE.json', 'MFD3.json', 'PMFD3STORAGE.json', 'MFDSTORAGE.json', 'PMPP_gp.json', 'MPP.json', 'PMPPSTORAGE.json', 'MRLIN2_flgpcap.json', 'PMRLIN2_flgpuse.json', 'MRLIN2_flsppr.json', 'PMRLIN2_gprom.json', 'MRLIN2_rlgpcap.json', 'PMRLIN2_rlgpuse.json', 'MRLIN2_rlsppr.json', 'PMRLIN2STORAGE.json', 'AggNum.json', 'QAggNumSTORAGE.json', 'ARGMIN.json', 'QARGMINSTORAGE.json', 'CMPLDC.json', 'QCMPLDCSTORAGE.json', 'LIMIT.json', 'QLIMITSTORAGE.json', 'MLAgg.json', 'QMLAggSTORAGE.json', 'RCRW.json', 'QRCRWSTORAGE.json', 'SET.json', 'QSETSTORAGE.json', 'Topk2.json', 'QTopK2STORAGE.json', 'TPCH.json', 'QTPCHSTORAGE.json', 'WHRSUB_bk.json', 'QWHRSUB.json', 'WHRSUBSTORAGE.json', 'QWIN.json', 'WINSTORAGE.json', 'VPGN.json', 'PGNSTORAGE.json', 'VPGS.json', 'PGSSTORAGE.json', 'VPJC.json', 'PJCSTORAGE.json', 'VPJJ.json', 'PJJJ.json', 'VPJJJSTORAGE.json', 'PJJSTORAGE.json', 'VPJS.json', 'PJSSTORAGE.json']




benches = ['FPAgg.json', 'FPDist.json', 'FPSAgg.json', 'FPSDist.json', 'PMAP.json', 'PMBD_gp.json', 'PMBD_sppr.json', 'PMFD_gp.json', 'PMFD_sppr.json', 'PMFD2.json', 'PMFD3.json', 'PMPP_gp.json', 'PMPP.json', 'PMRLIN2_flgpcap.json', 'PMRLIN2_flgpuse.json', 'PMRLIN2_flsppr.json', 'PMRLIN2_gprom.json', 'PMRLIN2_rlgpcap.json', 'PMRLIN2_rlgpuse.json', 'PMRLIN2_rlsppr.json', 'QAggNum.json', 'QARGMIN.json', 'QCMPLDC.json', 'QLIMIT.json', 'QMLAgg.json', 'QRCRW.json', 'QSET.json', 'QTopk2.json', 'QWHRSUB.json', 'QWIN.json', 'VPGN.json', 'VPGS.json', 'VPJC.json', 'VPJJ.json', 'VPJJJ.json', 'VPJS.json']









all_var_time = []
g = []
p = []
m = []
s = []
for bench in benches:
    with open (f'{os.getcwd()}/zackups/sf1/{bench}') as f:
        data = json.load(f)
    results = collect_var_time(data)
    for key, values in results.items():
        if 'gprom' in key.lower():
            g.extend( values )
        if 'smokedduck' in key.lower():
            s.extend(values)
        if 'provsql' in key.lower():
            p.extend(values)
        if 'sqlprov' in key.lower():
            m.extend(values)

    
        all_var_time.extend(values)

print(f"############################################\n## below 1 % \n############################################\n")

(cnt, Len) = (0, 0)
(cnt, Len) = cal(0.01, all_var_time)
print(f'all     below 1%: {cnt}, {Len}: {cnt / Len}')
(cnt, Len) = cal(0.01, g)
print(f'gprom   below 1%: {cnt}, {Len}: {cnt / Len}')
(cnt, Len) = cal(0.01, m)
print(f'muller  below 1%: {cnt}, {Len}: {cnt / Len}')
(cnt, Len) = cal(0.01, s)
print(f'smd     below 1%: {cnt}, {Len}: {cnt / Len}')
(cnt, Len) = cal(0.01, p)
print(f'provsql below 1%: {cnt}, {Len}: {cnt / Len}')


print(f"############################################\n## below 5 % \n############################################\n")

(cnt, Len) = cal(0.05, all_var_time)
print(f'all     below 5%: {cnt}, {Len}: {cnt / Len}')
(cnt, Len) = cal(0.05, g)
print(f'gprom   below 5%: {cnt}, {Len}: {cnt / Len}')
(cnt, Len) = cal(0.05, m)
print(f'muller  below 5%: {cnt}, {Len}: {cnt / Len}')
(cnt, Len) = cal(0.05, s)
print(f'smd     below 5%: {cnt}, {Len}: {cnt / Len}')
(cnt, Len) = cal(0.05, p)
print(f'provsql below 5%: {cnt}, {Len}: {cnt / Len}')

print(f"############################################\n## below 10% \n############################################\n")

(cnt, Len) = cal(0.10, all_var_time)
print(f'all     below 10%: {cnt}, {Len}: {cnt / Len}')
(cnt, Len) = cal(0.10, g)
print(f'gprom   below 10%: {cnt}, {Len}: {cnt / Len}')
(cnt, Len) = cal(0.10, m)
print(f'muller  below 10%: {cnt}, {Len}: {cnt / Len}')
(cnt, Len) = cal(0.10, s)
print(f'smd     below 10%: {cnt}, {Len}: {cnt / Len}')
(cnt, Len) = cal(0.10, p)
print(f'provsql below 10%: {cnt}, {Len}: {cnt / Len}')








# ['FPAgg.json', 'PAggSTORAGE.json', 'FPDist.json', 'PDistSTORAGE.json', 'FPSAgg.json', 'PSAggSTORAGE.json', 'FPSDist.json', 'PSDistSTORAGE.json', 'PMAP_bk.json', 'MAP.json', 'PMBD_gp.json', 'MBD_sppr.json', 'PMBDSTORAGE.json', 'MFD_gp.json', 'PMFD_sppr.json', 'MFD2.json', 'PMFD2STORAGE.json', 'MFD3.json', 'PMFD3STORAGE.json', 'MFDSTORAGE.json', 'PMPP_gp.json', 'MPP.json', 'PMPPSTORAGE.json', 'MRLIN2_flgpcap.json', 'PMRLIN2_flgpuse.json', 'MRLIN2_flsppr.json', 'PMRLIN2_gprom.json', 'MRLIN2_rlgpcap.json', 'PMRLIN2_rlgpuse.json', 'MRLIN2_rlsppr.json', 'PMRLIN2STORAGE.json', 'AggNum.json', 'QAggNumSTORAGE.json', 'ARGMIN.json', 'QARGMINSTORAGE.json', 'CMPLDC.json', 'QCMPLDCSTORAGE.json', 'LIMIT.json', 'QLIMITSTORAGE.json', 'MLAgg.json', 'QMLAggSTORAGE.json', 'RCRW.json', 'QRCRWSTORAGE.json', 'SET.json', 'QSETSTORAGE.json', 'Topk2.json', 'QTopK2STORAGE.json', 'TPCH.json', 'QTPCHSTORAGE.json', 'WHRSUB_bk.json', 'QWHRSUB.json', 'WHRSUBSTORAGE.json', 'QWIN.json', 'WINSTORAGE.json', 'VPGN.json', 'PGNSTORAGE.json', 'VPGS.json', 'PGSSTORAGE.json', 'VPJC.json', 'PJCSTORAGE.json', 'VPJJ.json', 'PJJJ.json', 'VPJJJSTORAGE.json', 'PJJSTORAGE.json', 'VPJS.json', 'PJSSTORAGE.json']

# ['FPAgg.json', 'PDist.json', 'FPSAgg.json', 'PSDist.json', 'PMAP.json', 'MBD_gp.json', 'PMBD_sppr.json', 'MFD_gp.json', 'PMFD_sppr.json', 'MFD2.json', 'PMFD3.json', 'MPP_gp.json', 'PMPP.json', 'MRLIN2_flgpcap.json', 'PMRLIN2_flgpuse.json', 'MRLIN2_flsppr.json', 'PMRLIN2_gprom.json', 'MRLIN2_rlgpcap.json', 'PMRLIN2_rlgpuse.json', 'MRLIN2_rlsppr.json', 'QAggNum.json', 'ARGMIN.json', 'QCMPLDC.json', 'LIMIT.json', 'QMLAgg.json', 'RCRW.json', 'QSET.json', 'Topk2.json', 'QTPCH.json', 'WHRSUB.json', 'QWIN.json', 'PGN.json', 'VPGS.json', 'PJC.json', 'VPJJ.json', 'PJJJ.json', 'VPJS.json']
