
import subprocess
import fileUtils as f_util
import queryUtils as q_util

SHOW_LOG = True
def log(msg):
    if SHOW_LOG:
        print(msg)

################################################################################
# Postgresql Utils
################################################################################
def getPostgresqlCmdFromJson(jsonFile):
    return [ jsonFile["postgresql_bin"],
            '-h', jsonFile["host"],
            '-U', jsonFile["user"],
            '-d', jsonFile["db"],
            '-p', jsonFile["port"] ]

def get_shell_command_results(cmd):
    process = subprocess.run(cmd, stdout= subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return (process.returncode, process.stdout, process.stderr)

def psql_time(psqlcmd, infile, outfile, repeat, prepare = None):
    cmd = (psqlcmd + ['-f', infile])
    with open(outfile, 'w') as f:
        for i in range(repeat):
            print(f'the {(i+1)}-th execution of command')
            if prepare is not None:
                (rt, out, err) = get_shell_command_results(psqlcmd + ['-f', prepare])
                if rt:
                    print(f"Error running PREPARE command in postgresql [{rt}]: \n{err}\n{out}")
                    exit(rt)

            (rt, out, err) = get_shell_command_results(cmd)
            if rt:
                print(f"Error running command in postgresql [{rt}]: \n{err}\n{out}")
                exit(rt)
            f.write(out)

def psql_dashC(psqlcmd, inStr, outfile, repeat = 1):
    cmd = (psqlcmd + ['-c', '\\timing on'] + ['-c', inStr])
    (rt, out, err) = get_shell_command_results(cmd)
    if rt:
        print(f"Error running command in postgresql [{rt}]: \n{err}\n{out}")
        exit()
    with open(outfile, 'w') as f:
        f.write(out)

################################################################################
# DuckDB Shell Running
################################################################################
def duckdb_run(cmd, infile, outfile, repeat, MODE = 'w', cleanLineageTable=True, ReturnSpecificError=False):
    cmdStr = f'{cmd[0]} {cmd[1]}'
    sqlc = ''
    with open(infile, 'r') as f:
        sqlc = f.read()

    print(f'cmd to be executed: {cmdStr} < {sqlc}')
    with open(outfile, 'w') as f:
        for i in range(repeat):
            if cleanLineageTable:
                q_util.rmSMDLineageTables(cmd[0], cmd[1])
            process = subprocess.run(cmdStr,
                shell=True,
                input=sqlc,
                stdout= subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True)
            (rt, out, err) = (process.returncode, process.stdout, process.stderr)
            if rt:
                print(f"Error running command in duckdb [{rt}]: \n{err}\n{out}")
                if ReturnSpecificError:
                    return ('RORRE', i)
                else:
                    exit(rt)
            f.write(out)
    if ReturnSpecificError:
        return ('ENOD', repeat)

