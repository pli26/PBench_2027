# PBench_2027
PBench 

## File structure
### Extended version of the main paper (main.pdf)

### evaluation

This folder contains all evaluation result using SF = 1, including

- Data fetched from result 
- Storage fetched from result
- Plot the figures used in the paper

### performance

This folder contains all scripts to:

- Generate Data
- Generate SQLs for each task
- Run SQLs for each task

Please refer to the README.md in `./performance/`

### Systems

This folder contains a file containing simple instructions to make systems work.

### DB-related

This folder contains a pg16 extension, binary search, that enables GProM to work for coarse-grained provenance model and the prerequisite code for SQLProv.
