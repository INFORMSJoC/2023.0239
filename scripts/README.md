# Replicating  
To replicate the results in the computational study of [the paper](https://doi.org/10.1287/ijoc.2023.0239), run

```
python3 scripts/replicate_results.py
```

from [the main directory](../). Calling this script will run all considered approaches on the 560 robustified knapsack interdiction instances in the classic (min-max) and the more general setting, respectively. As per default, the deviations take random integer values. To consider the instances with continuous deviations, use the optional argument `--randint False`.

**Important:** Before changing from the integer-valued to the continuous-valued setting (or vice versa), ensure that all files with the `.ki` extension in the [BKIP directory](../data/BKIP) are removed or re-named. Previously generated files are not overwritten, and failure to remove them may lead to unreliable results.

# Counterexample
As discussed in [the paper](https://doi.org/10.1287/ijoc.2023.0239), the main result by [Bertsimas and Sim (2003)](https://link.springer.com/article/10.1007/s10107-003-0396-4) cannot be carried over to the bilevel setting. For the case of general $\Gamma$-robust mixed-integer linear bilevel problems, it may even be the case that none of the solutions to the deterministic bilevel sub-problems solved in Line 3 of Algorithm 3 in the paper is feasible for the $\Gamma$-robust bilevel problem. We observe this behavior for the nominal instance of size `n = 40` given in [counterexample.txt](../counterexample/counterexample.txt) with the uncertainty parameterization given by `uncertainty = 0.1` and `conservatism = 0.5`. The latter implies that $\Gamma = 20$ and that all lower-level objective function coefficients are equally perturbed by 10% of the nominal value. To verify that indeed none of the solutions to the deterministic bilevel sub-problems solved within the heuristic framework is $\Gamma$-robust feasible, simply run

```
python3 -m scripts.check_counterexample
```

from [the main directory](../).
Here, for each fixed leader's decision obtained from solving a bilevel sub-problem of the nominal type, all lower-level sub-problems are solved (cf. Lemma 1 in the paper) to determine whether the pair $(x,y)$ that is output as a solution of the bilevel sub-problem is $\Gamma$-robust feasible. Running the above script returns the message that there is no bilevel sub-problem for which the solution is $\Gamma$-robust feasible.