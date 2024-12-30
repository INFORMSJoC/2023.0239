[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)

# Heuristic Methods for $\Gamma$-Robust Mixed-Integer Linear Bilevel Problems

This archive is distributed in association with the [INFORMS Journal on
Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).

The software and data in this repository are a snapshot of the software and data
that were used in the research reported on in the paper 
[Heuristic Methods for Gamma-Robust Mixed-Integer Linear Bilevel Problems](https://doi.org/10.1287/ijoc.2023.0239) by Yasmine Beck, Ivana Ljubić, and Martin Schmidt. 

## Cite

To cite the contents of this repository, please cite both the paper and this repository, using their respective DOIs.

https://doi.org/10.1287/ijoc.2023.0239

https://doi.org/10.1287/ijoc.2023.0239.cd

Below is the BibTex for citing this snapshot of the repository.

```
@misc{Beck_et_al:2025,
  author =        {Yasmine Beck and Ivana Ljubić and Martin Schmidt},
  publisher =     {INFORMS Journal on Computing},
  title =         {{Heuristic Methods for $\Gamma$-Robust Mixed-Integer Linear Bilevel
                  Problems}},
  year =          {2025},
  doi =           {10.1287/ijoc.2023.0239.cd},
  url =           {https://github.com/INFORMSJoC/2023.0239},
  note =          {Available for download at https://github.com/INFORMSJoC/2023.0239},
}  
```

## Description  
This repository contains the code accompanying the paper [Heuristic Methods for Gamma-Robust Mixed-Integer Linear Bilevel Problems](https://doi.org/10.1287/ijoc.2023.0239) by Yasmine Beck, Ivana Ljubić, and Martin Schmidt.

## Prerequisites  
The methods are implemented in `Python 3.7.11` and `Gurobi 11.0.0` is used to solve all arising optimization problems. Visit [Gurobi's official website](https://www.gurobi.com/academia/academic-program-and-licenses) for details on how to obtain a license. In addition to Gurobi, the following Python packages and modules are required:

* argparse
* json
* numpy
* os
* subprocess
* time

Moreover, the heuristics use the `bkpsolver` presented in [Weninger and Fukasawa (2023)](https://link.springer.com/chapter/10.1007/978-3-031-32726-1_31). To install the `bkpsolver`, follow the instructions at https://github.com/nwoeanhinnogaehr/bkpsolver. 

## Usage  
In the following, we elaborate on how to use the exact and heuristic approaches considered in the computational study of [the paper](https://doi.org/10.1287/ijoc.2023.0239). We distinguish between the min-max and the more general bilevel setting.  

## Approaches for $\Gamma$-Robust Min-Max Problems Applied to the $\Gamma$-Robust Knapsack Interdiction Problem  

### 1. Heuristics Presented in [the Paper](https://doi.org/10.1287/ijoc.2023.0239)  
From [the main directory](./), run

```
python3 -m src.min_max_heuristic --instance_file file.txt --conservatism conservatism_value --deviations deviation_values --output_file outfile.json
```

to build a $\Gamma$-robust knapsack interdiction problem and solve it heuristically by solving a linear number of knapsack interdiction problems of the nominal type.

#### Necessary arguments:
`--instance_file`  
The file containing the nominal instance data.

`--conservatism`  
Level of conservatism (in percent) must be a scalar between 0 and 1.

`--output_file`  
The .json file to write the output to.

and either  

`--deviations`  
The deviations for the objective function coefficients, e.g., `1 2 1` for a problem of size 3.

or  

`--uncertainty`  
Uncertainty value (in percent) must be a scalar between 0 and 1.  

A detailed description of the instance data format and the uncertainty parameterization can be found in the [data directory](data).

#### Optional arguments:  
`--solver`  
The solver to use for the solution of the problems of the nominal type. The default is the combinatorial approach (`--solver bkp`) by [Weninger and Fukasawa (2023)](https://link.springer.com/chapter/10.1007/978-3-031-32726-1_31). To use the branch-and-cut approach based on [Fischetti et al. (2019)](https://pubsonline.informs.org/doi/10.1287/ijoc.2018.0831), specify `--solver ic`.  

To install the `bkpsolver` by Weninger and Fukasawa (2023), follow the instructions at https://github.com/nwoeanhinnogaehr/bkpsolver. The best performance is achieved if the `bkpsolver` is located in the parent directory of this repository. Alternatively, you can modify the path to the solver in the `__init__` section of [min_max_heuristic.py](src/min_max_heuristic.py) to match its location.

`--modify`  
Use the modified variant of the heuristic in which all bilevel sub-problems are solved first (`True`) or use the variant that alternates between solving bilevel and single-level problems (`False`). The default is `False`.

`--time_limit`  
The time limit in seconds. The default is 3600 seconds.

### 2. Greedy Interdiction Heuristic  
To apply a "Greedy Interdiction" heuristic in the spirit of the one presented in Algorithm 4.2 in the [PhD thesis by S. DeNegre](https://coral.ise.lehigh.edu/~ted/files/papers/ScottDeNegreDissertation11.pdf) to the $\Gamma$-robust knapsack interdiction problem, run

```
python3 -m src.greedy_interdiction --instance_file file.txt --conservatism conservatism_value --deviations deviation_values --output_file outfile.json
```

from [the main directory](./) using the same arguments as specified in the necessary arguments section above.

### 3. Exact and Problem-Tailored Branch-and-Cut Approach
To apply the exact and problem-tailored branch-and-cut approach presented in [our earlier work](https://link.springer.com/article/10.1007/s12532-023-00244-6), follow the instructions at https://github.com/YasmineBeck/gamma-robust-knapsack-interdiction-solver (DOI: 10.5281/zenodo.7965281).

## Approaches for General $\Gamma$-Robust Bilevel Problems Applied to the Generalized $\Gamma$-Robust Knapsack Interdiction Problem  

### 1. Heuristics Presented in [the Paper](https://doi.org/10.1287/ijoc.2023.0239)  
From [the main directory](./), run

```
python3 -m src.general_heuristic --instance_file file.txt --conservatism conservatism_value --deviations deviation_values --output_file outfile.json
```

to build a generalized $\Gamma$-robust knapsack interdiction problem and solve it heuristically by solving a linear number of generalized knapsack interdiction problems of the nominal type.

#### Necessary arguments:
Same as for the min-max setting, see above.

#### Optional arguments:
`--refine`  
Include a refinement step (`True`) to account for an optimistic follower or not (`False`). The default is `True`.

`--time_limit`  
The time limit in seconds. The default is 3600 seconds.

### 2. ONE-SHOT and ITERATE Heuristics  
To apply the ITERATE heuristic presented in [Fischetti et al. (2018)](https://doi.org/10.1016/j.ejor.2017.11.043) to an instance of the generalized $\Gamma$-robust knapsack interdiction problem, run

```
python3 -m src.iterate_heuristic --instance_file file.txt --conservatism conservatism_value --deviations deviation_values --output_file outfile.json
```

from [the main directory](./) using the same arguments as specified in the necessary arguments section above. The default time limit is 3600 seconds. You can change it using the optional argument `--time_limit TL`, where TL is a scalar specifying the time limit in seconds.

To run the ONE-SHOT variant of the method presented in [Fischetti et al. (2018)](https://doi.org/10.1016/j.ejor.2017.11.043), add the optional argument

```
--one_shot True
```

### 3. Exact and Problem-Tailored Branch-and-Cut Approach
To apply the exact and problem-tailored branch-and-cut approach outlined in [the paper](https://doi.org/10.1287/ijoc.2023.0239), run

```
python3 -m src.gamma_robust_extended_model --instance_file file.txt --conservatism conservatism_value --deviations deviation_values --output_file outfile.json
```

from [the main directory](./) using the same arguments as specified in the necessary arguments section above. The default time limit is 3600 seconds. You can change it using the optional argument `--time_limit TL`, where TL is a scalar specifying the time limit in seconds.  

Further details on this approach can also be found in Section 3.5 of the PhD thesis by Yasmine Beck.

## Replicating
The results of the computational study in [the paper](https://doi.org/10.1287/ijoc.2023.0239) can be replicated using the scripts and documentation provided in the [scripts directory](scripts).

## Results
The figures and tables summarizing the results of the computational study in [the paper](https://doi.org/10.1287/ijoc.2023.0239) are provided in [figures_and_tables.pdf](results/figures_and_tables.pdf).