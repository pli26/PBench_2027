# Run Microbenchmarks

# I. Generating Data
- Run `python GenData.py` in folder **GenData**
- Importing to DBs:
  - run the xxx_postgresql.sql in PostgreSQL to import data into PostgreSQL DB
  - run the xxx_duckdb.sql in PostgreSQL to import data into DuckDB
- For ProvSQL
  - Install the extension first.
  - After importing data, activate the extension `CREATE EXTENSION provsql cascade;`.
  - Modify the search path, let us say the db name is provsqldata, `ALTER DATABASE provsqldata set search_path to public, provsql;`.
  - Add `provsql` column for each table by running xxx_provsql.sql.
  - For provenance specific (checking the category in the following table), please add the mapping table by running xxx_mapping.sql for table xxx.
- For SQLProv
  - Create the necessary logging tables by importing `pre1.sql` and `pre2.sql` in `../DB-related/SQLProv/`
  - Create tables for phase I and phase II by running xxx_sqlprov.sql for table xxx.

- For GProM
  - Please install the PostgreSQL extension binary search in `../DB-related/pg16-binary-search.zip` for the coarse-grained task.

# II. Microbenchmark

Below shows the tasks each folder belongs to:

| Folder           | Category                  | Task Name                                                                  |
| ---------------- | ------------------------- | -------------------------------------------------------------------------- |
| PMAP             | Use-case specific tasks   | Coarse-grained provenance (capture + use)                                  |
| PMBD             | Use-case specific tasks   | Backward debugging                                                         |
| PMFD/PMFD2/PMFD3 | Use-case specific tasks   | Forward debugging                                                          |
| PMPP             | Use-case specific tasks   | Provenance polynomials                                                     |
| PMRLIN2          | Use-case specific tasks   | Reproducibility(Lineage and reduced size of lineage)                       |
| FPAgg            | Provenance specific tasks | Fix provenance varying per tuple provenance size using aggregation queries |
| FPDist           | Provenance specific tasks | Fix provenance varying per tuple provenance size using DISTINCT  queries   |
| FPSAgg           | Provenance specific tasks | Provenance factorization using aggregation queries                         |
| FPSDist          | Provenance specific tasks | Provenance factorization using DISTINCT queries                            |
| VPGN             | Provenance specific tasks | Vary total provenance size by varying group number                         |
| VPGS             | Provenance specific tasks | Vary total provenance size by varying group size                           |
| QTopK2           | Provenance specific tasks | Intermediate provenance size                                               |
| QAggNum          | Query specific tasks      | Vary number of aggregation functions                                       |
| QARGMIN          | Query specific tasks      | Arg-min queries                                                            |
| QCMPLDC          | Query specific tasks      | Complex join condition queries                                             |
| QLIMIT           | Query specific tasks      | Aggregation-LIMIT queries                                                  |
| QMLAgg           | Query specific tasks      | Multi-level aggregation queries                                            |
| QRCRW            | Query specific tasks      | Recursive queries                                                          |
| QSET             | Query specific tasks      | Set difference  queries                                                    |
| QWHRSUB          | Query specific tasks      | Sub-queries                                                                |
| QWIN             | Query specific tasks      | Window Operators                                                           |
| VPJC             |                           | Vary join cardinality                                                      |
| VPJS             |                           | Vary join selectivity                                                      |
| VPJJ/VPJJJ       |                           | Multiple join operators                                                    |

## A. Add configuration in `utils/systems.cfg`
Add your corresponding configuration for PostgreSQL, Duckdb (two version).

## B. Gen Queries
Run `python genQ.py` in the folder of tasks.

## C. Run a task

### i. For GProM
- GProM on PostgreSQL
```sh
python Performances.py --microbenchmark 'FPAGG'  --runrepeat 10 --systems 'gprom' --gprombackend 'postgresql' --db_bin 'psql' --db_name 'sf1' --db_port '5456' --db_user 'username' --db_password 'test' --db_host 'localhost'
```
- GProM on Duckdb
```shell
python Performances.py --microbenchmark 'QARGMIN'  --runrepeat 10 --systems 'gprom' --gprombackend 'duckdb' --db_bin '/PATH/TO/build/duckdb' --db_path '/PATH/TO/DATA/dt.db'
```

### ii. For SQLProv
```shell
python Performances.py --microbenchmark 'QWHRSUB'  --runrepeat 10 --systems 'sqlprov' --db_bin 'psql' --db_name 'g1' --db_port '5454' --db_user 'aUserName' --db_password 'test' --db_host 'localhost'
```

### iii. For ProvSQL
```sh
python Performances.py --microbenchmark 'VPJJ'  --runrepeat 5 --systems 'provsql' --db_bin 'psql' --db_name 'sqlprovdbname' --db_port '5454' --db_user 'it_is_me' --db_password 'test' --db_host 'localhost' --provsqlmmap 'provsql mmap files store location' --provsqlStoreAfter aIntger
```
### iv. For Smokedduck
- For the best practices, please store the same data twice for phaseI and phaseII. Do not use one copy for two phases.
```shell
python Performances.py --microbenchmark 'QLIMIT'  --runrepeat 10 --systems 'smokedduck' --db_bin '/PATH/TO/smokedduck-2025-f/build/duckdb' --db_path '/PATH/TO/DATA/FOR/PHASEI.db' --db_bin_storage '/PATH/TO/lineage_capture_v5/build/duckdb' --db_path_storage '/PATH/TO/DATA/FOR/PHASEII.db'
```
### v. For PostgreSQL
```shell
python Performances.py --microbenchmark 'VPGN'  --runrepeat 10 --systems 'postgresql' --db_bin 'psql' --db_name 'g1' --db_port '5454' --db_user 'uicdbgroup' --db_password 'test' --db_host 'localhost'
```
### vi. For DuckDB
```shell
python Performances.py --microbenchmark 'VPGS'  --runrepeat 10 --systems 'duckdb' --db_bin '/PATH/TO/DUCKDB/BUILD/FOR/PHASEI' --db_path '/PATH/TO/DATA/FOR/PHASEI.db'
```

### Run single query
If a microbenchmark contains multiple queries, let us say 5, you can run part of them by adding option `--querylist '2,3'` to run Q2 and Q3.

