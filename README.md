# LRDC
Codebase for the bachelor thesis project "DIfference Checker for Logic Rules"

This repo contains the code for the project

usage: "python3 comparator.py [random/filename1 filename2] [greedy/full]"

Will print made or given CNF sets, followed by a score of similarity between the two


## Output
result of the program is the object created in __main__ of ```comparator.py```:
```diff_exp```

It is an object containing both rulesets that are compared (expressions), and characteristics of their differences as made by the algorithms present in this project
Also contains said score

Important note, the negation of a Literal is counted as a half overlap, meaning it contributes to similarity of clauses, but only half as much as actual overlap of Literals


## Experimentation
A file containing code for experimentation of performance of the two proposed algorithms for the project: fullsearch and greedy, is included in ```experiment.py```
Here various experiments of running each of the algorithms (or greedy only) for generated pairs of rulesets are located, and the parameters of the algorithms are varied aswell (k: amount of Literals per clause, n: Amount of variables to choose from when creating clauses, and m: the amount of clauses to generate for a set)

For experimentation a random clause generation tool was used: cnfgen
https://github.com/MassimoLauria/cnfgen

## Analysis
Finally a notebook is included containing analysis of made results by the experimentation. It is however reliant on results generated locally, so rerunning the notebook is likely not possible.
