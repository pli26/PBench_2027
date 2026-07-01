# Systems

## ProvSQL
[ProvSQL GitHub links](https://github.com/PierreSenellart/provsql)

### Installation on Ubuntu

#### Postgresql 16 Installation:
1. Packages:
`build-essential libreadline-dev zlib1g-dev flex bison libicu-dev libossp-uuid-dev`
2. Customerized installation folder:
`./configure --prefix=/path/to/install --with-uuid=ossp`
3. `make` and `make install`
4. Install extension `uuid-ossp` inside `contrib/uuid-ossp`: `make` and `make install`
  (On MacOs, uuid should be `e2fs` not `ossp`, since `--with-uuid=ossp` cannot be compiled when executing `make` which is `./configure --prefix=/path/to/install with-uuid=e2fs`)


#### ProvSql Installation:
1. Set `PG_CONFIG` to the installed folder in `Makefile.internal`: `PG_CONFIG = pg_config` ==> `PG_CONFIG = /path/to/install/bin/pg_config`
2. `make` and `make install`
3. add `shared_preload_libraries = 'provsql'` in `postgresql.conf`(Typically, this file is in the `data` folder created for data storing)
4. Install Missing libs if necessary:
	* `boost` -> `sudo apt install libboost-all-dev`
5. For MacOS only:
   If the `make` reports errors like the following:
   ```
   	make[1]: *** No rule to make target `provsql.so', needed by `all'.  Stop.
   	make: *** [default] Error 2
   ```

   Then need to Add/Modify the following to `Makefile.internal` and `gmake` again
   ```
   ADD:
   		ifeq ($(OS), Darwin)
   		SHLIB = $(MODULE_big).dylib
   		else
   		SHLIB = $(MODULE_big).so
   		endif
   MODIFY:
	  	UPDATE the line: "all: $(DATA) $(MODULE_big).so test/schedule"
	 	TO: "all: $(DATA) $(SHLIB) test/schedule"
   ```
#### Enabling ProvSQL in PostgreSQL
`CREATE EXTENSION provsql CASCADE` in the database that used.

#### Check if the extensions are there:
`select * from pg_extension;`

```
oid    |    extname    | extowner | extnamespace | extrelocatable | extversion | extconfig | extcondition
-------+---------------+----------+--------------+----------------+------------+-----------+--------------
 12792 | plpgsql       |       10 |           11 | f              | 1.0        |           |
 ...   | binary_search |       10 |         2200 | t              | 1.0        |           |
 16665 | uuid-ossp     |       10 |         2200 | t              | 1.1        |           |
 16676 | provsql       |       10 |         2200 | f              | 1.0.0-dev  |           |
(4 rows)

```

#### A simple ProvSQL example:
* Suppose we have tables `R(a, b)`, and `S(c, d)` look like the following:

	```
	R                              S:
	a  | b                       c  | d
	---+----                     ---+----
 	1  | 1 			             2  | 10
 	2  | 2                       40 |  8
 	3  | 3
 	1  | 8
 	```

* Annotation `provsql.add_provenance`:
	* `SELECT provsql.add_provenance('r')` and `SELECT provsql.add_provenance('s')`

	```
	R:
	a | b |               provsql
	---+---+--------------------------------------

 	1 | 1 | 3cedc97a-558e-45b7-be30-ad5ac1359904
 	2 | 2 | 719f93c3-0ab2-4b07-859b-1283d35ef060
 	3 | 3 | 03f15cda-4ea6-4e4e-a718-727e3d7fbafb
 	1 | 8 | 0be9d683-8e94-440d-9a31-c6ea0cae313c
 	(4 rows)

 	S:
 	 c  | d  |               provsql
 	----+----+--------------------------------------
 	2   | 10 | 85f627f6-396d-4e3a-998b-2ca32df3f86a
 	40  |  8 | 3f27dc2b-fb05-4b92-bf75-58a99e6f1912
 	```

* Execution a query `SELECT a, avg(b) as avg_b FROM R JOIN S ON (a = c) GROUP BY a;`

	```
	 a |         avg_b          |               provsql
	---+------------------------+--------------------------------------

 	2  | 2.0000000000000000 (*) | 1b366730-fa13-5600-8385-71841caf3a42
 	(1 row)
 	```
## GProM
[GProM GitHub Link](https://github.com/IITDBGroup/gprom)

### Install
```sh
./autogen
./configure --enable-xxx (xxx:database, e.g., oracle, sqlite) --with-xxx(libraries for databases, e.g., --with-libpq=/path/to/postgresql/lib/)
make
make install
```
### Example:
- Suppose we have a table `R(a int, b int)`, a query to find all `a`: `SELECT a FROM R`:
- GProM will rewrite the query in to:

	```
	SELECT /*+ materialize */ F0_0."a" AS "a", F0_0."b" AS "b", F0_0."a" AS "prov_r_a", F0_0."b" AS "prov_r_b"
	FROM "r" F0_0)
	SELECT F0_0."a" AS "a", F0_0."prov_r_a" AS "prov_r_a", F0_0."prov_r_b" AS "prov_r_b"
	FROM (SELECT * FROM temp_view_0) F0_0;
	```

- Execute the rewrite query will produce the result with the provenance:

## Smoked Duck
1. Clone the repo and use `lineage_capture_v5` branch to test
2. Config and build
   - Configure
	 - MacOS
	   ```sh
	   cmake -DCMAKE_CXX_FLAGS="-Wno-missing-template-arg-list-after-template-kw" \
        -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
        -DDISABLE_VPTR_SANITIZER=ON \
        -DBUILD_LINEAGE_EXTENSION=ON \
        -DSKIP_EXTENSIONS="jemalloc" \
        -DBUILD_EXTENSIONS='parquet;json' \
        -B your build folder
	    ```
		- For nix package manager (if used), should tell explicitly to ignore the Nix compilers and use Apple compilers with the --cc and --cxx
		  ```sh
		  cmake -B build \
 			-DCMAKE_C_COMPILER=/usr/bin/cc \
 			-DCMAKE_CXX_COMPILER=/usr/bin/c++ \
 			-DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
 			-DDISABLE_VPTR_SANITIZER=ON \
 			-DBUILD_LINEAGE_EXTENSION=ON \
 			-DSKIP_EXTENSIONS="jemalloc" \
 			-DBUILD_EXTENSIONS='parquet;json'
		  ```
	 - Linux
	   ```sh
		cmake -DBUILD_LINEAGE_EXTENSION=ON \
        -DSKIP_EXTENSIONS="jemalloc" \
        -DBUILD_EXTENSIONS='parquet;json' \
        -B your build folder
	   ```
   - Build
   `cmake --build . -j 6`

3. Make data persistent
	1. open duckdb `./duckdb`
	2. attach to a persistent db called `mydb.db`
	   ```sh
	   attach 'mydb.db' as db;
	   ```
	3. load data
	   ```sh
		.read xxxx/createAndLoad.sql;
        OR
        create table T and Insert into t values (...), ...;
	   ```
	   checkpoint
	   ```sh
	   copy from database memory to db;
	4. detach the db
	   ```sh
	   detach db;
	   ```
	5. reuse the data
	   ```sh
	   ./duckdb /path/to/my.db
	   ```

[Smoked Duck Link](https://pypi.org/project/smokedduck/)

**When install the python library, please use python 3.11 version**

Using tools like `pyenv` to manage version of `Python`

### DuckDB

#### Installation (CLI)
```
curl https://install.duckdb.org | sh
```

#### Accessing DB
```
/home/NAME/./duckdb/cli/latest/duckdb
```

#### Example:
* In-Memory
	* Run DB `/path/to/duckdb/`

	```
	Connected to a transient in-memory database.
	Use ".open FILENAME" to reopen on a persistent database.
	```

	* Create tables and insert values: `create table r (a int, b int);`, `INSERT INTO R VALUES(1, 1);`
	* Query a table `SELECT * FROM R;`

* Persistent DB
	* Run DB `/path/to/duckdb/ /path/to/xxx.duckdb`
### SmokedDuck
SmokedDuck is implemented as a fork of DuckDB.
[SmokedDuck Link](https://github.com/cudbg/sd/tree/whatif?tab=readme-ov-file)

