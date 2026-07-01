#!/bin/zsh

# ------------------------------------
# Stop all connections
# ------------------------------------

pg_ctl -D /Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf1/ -l logfile -o "-F -p 5454" stop
pg_ctl -D /Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf2/ -l logfile -o "-F -p 5455" stop
pg_ctl -D /Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf10/ -l logfile -o "-F -p 5456" stop
pg_ctl -D /Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf20/ -l logfile -o "-F -p 5457" stop



# -- provsql
pg_ctl -D /Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf10/ -l logfile -o "-F -p 5456" start
REPEAT=10 # repeats for each experiment
DBPORT=5456 # port for postgresql
DBNAME='p1' # databse name
MMAPPATH='xxx' # the folder name inside base that stored the data of "DBNAME" databse
STOREAFTER=6 # Since we do not want to keep too large provsql_xxxx.mmap, we need to restore them from backup files
# echo "python Performances.py --microbenchmark 'VPGN'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}"
python Performances.py --microbenchmark 'VPGN'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}

python Performances.py --microbenchmark 'VPGS'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}
python Performances.py --microbenchmark 'VPJJ'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}
python Performances.py --microbenchmark 'VPJJJ'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}
python Performances.py --microbenchmark 'VPJC'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}
python Performances.py --microbenchmark 'VPJS'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}
python Performances.py --microbenchmark 'FPAgg'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}
python Performances.py --microbenchmark 'FPSAgg'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}
python Performances.py --microbenchmark 'QAggNum'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}
python Performances.py --microbenchmark 'QCMPLDC'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}
python Performances.py --microbenchmark 'FPDist'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}
python Performances.py --microbenchmark 'FPSDist'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '${MMAPPATH}' --provsqlStoreAfter ${STOREAFTER}
# -- python Performances.py --microbenchmark 'QMLAgg'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost'
# -- python Performances.py --microbenchmark 'QTopK'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost'
# ----- Provenance Models
# python Performances.py --microbenchmark 'PMRLIN'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --querylist '1,2,3' --provsqlmmap '/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf1'
# python Performances.py --microbenchmark 'PMRLIN'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --querylist '1,2,3' --provsqlmmap '/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf1'
# python Performances.py --microbenchmark 'QARGMIN'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf1'
# python Performances.py --microbenchmark 'PMBD'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf1'
# python Performances.py --microbenchmark 'PMPP'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf1'
# python Performances.py --microbenchmark 'PMFD'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf1'
# python Performances.py --microbenchmark 'PMFD2'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf1'
# python Performances.py --microbenchmark 'PMFD3'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf1'
# python Performances.py --microbenchmark 'PMRLIN'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '${DBPORT}' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf1'
# python Performances.py --microbenchmark 'PMRLIN2'  --runrepeat ${REPEAT} --systems 'provsql' --db_bin 'psql' --db_name '${DBNAME}' --db_port '5454' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost' --provsqlmmap '/Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf1'


pg_ctl -D /Users/uicdbgroup/pengyuan/DBs/installed/nixDB/sf10/ -l logfile -o "-F -p 5456" stop
