import os

def buildSQLProv(sf, table, attributes):

    with open(f'{os.getcwd()}/data/sf{sf}/{table}_sqlprov.sql', 'w') as f:
        f.write(f'drop materialized view if exists {table}_1 cascade;\n')
        f.write(f'create materialized view {table}_1 as select nextval(\'prov_ids\')::int tuid, * from {table};\n')
        for attr in attributes[1:]:
            f.write(f'create index idx_{table}_1_{attr} on {table}_1 ({attr});\n')

        f.write(f'drop materialized view if exists {table}_2 cascade;\n')
        f.write(f'create materialized view {table}_2 as select tuid \n')
        for attr in attributes:
            f.write(f',  array[nextval(\'prov_ids\')::int] {attr} \n')

        f.write(f'from {table}_1;\n')
        f.write(f'drop index if exists idx_{table}_2_tuid;\n')
        f.write(f'create index idx_{table}_2_tuid on {table}_2 (tuid);\n')

def buildProvMapping(sf, mapping_tbl, table, attribute):
    with open(f'{os.getcwd()}/data/sf{sf}/{table}_mapping.sql', 'w') as f:
        f.write(f'\\timing \n')
        f.write(f'drop table if exists {mapping_tbl} cascade;\n')
        f.write(f'select create_provenance_mapping(\'{mapping_tbl}\', \'{table}\', \'{attribute}\');\n')

def buildProvSQL(sf, table):

    with open(f'{os.getcwd()}/data/sf{sf}/{table}_provsql.sql', 'w') as f:
        f.write(f'\\timing \n')
        f.write(f'select add_provenance(\'{table}\');\n')

def buildDDL(sf, table, attributes, id):
    with open(f'{os.getcwd()}/data/sf{sf}/{table}_postgresql.sql', 'w') as f:
        f.write(f'drop table if exists {table} cascade;\n')
        f.write(f'create table {table} (\n')
        for idx, attr in enumerate(attributes):
            if idx > 0:
                f.write(f', ')
            if attr == id:
                f.write(f'{attr} int primary key \n')
            else:
                f.write(f'{attr} int not null \n')
        f.write(f');\n')
        f.write(f'copy {table} from \'{os.getcwd()}/data/sf{sf}/{table}.csv\' delimiter \',\' csv header;\n')
        for attr in attributes[1:]:
            f.write(f'create index idx_{table}_{attr} on {table} ({attr});\n')
        f.write(f'analyze {table};\n')

    with open(f'{os.getcwd()}/data/sf{sf}/{table}_duckdb.sql', 'w') as f:
        f.write(f'drop table if exists {table} cascade;\n')
        f.write(f'create table {table} (\n')
        for idx, attr in enumerate(attributes):
            if idx > 0:
                f.write(f', ')
            if attr == id:
                f.write(f'{attr} int primary key \n')
            else:
                f.write(f'{attr} int not null \n')
        f.write(f');\n')
        f.write(f'copy {table} from \'{os.getcwd()}/data/sf{sf}/{table}.csv\' (format csv, header);\n')