##################################################################
# This file is part of the code used for the computational study #
# in the paper                                                   #
#                                                                #
#  "Heuristic Methods for Gamma-Robust Mixed-Integer Linear      #
#   Bilevel Problems"                                            #
#                                                                #
# by Yasmine Beck, Ivana Ljubic, and Martin Schmidt (2025).      #
##################################################################

# Global imports
import argparse
import json
import numpy as np
import os
import subprocess

def generate_deviations(instance_file, uncertainty, randint):
    """Randomly generate deviations for an instance."""
    # Load instance data.
    with open(instance_file, 'r') as file:
        data_from_file = file.read()
    file.close()
    instance_data = json.loads(data_from_file)
    profits = instance_data['profits']

    # Randomly generate deviations.
    size = len(profits)
    deviations = [0]*size
    for idx in range(size):
        np.random.seed(idx*size)
        if 'True' in randint:
            deviations[idx] = np.random.randint(
                0, high=np.ceil(uncertainty*profits[idx]) + 1
            )
        else:
            deviations[idx] = np.round(
                np.random.uniform(0, uncertainty)*profits[idx], 1
            )

    deviations = ' '.join(map(str, deviations))
    return deviations

def instance_cmd(ins, cons, devs):
    cmd = f"--instance_file {ins} --conservatism {cons} --deviations {devs}"
    return cmd

def get_files(min_max, size, instance, setting):
    if 'True' in min_max:
        instance_file = f"data/BKIP/BKIP_{size}_{instance}.txt"
        output_file = f"BKIP_{size}_{instance}_{setting}.json"
        
    if 'False' in min_max:
        instance_file = f"data/generalized-BKIP/generalized_BKIP_{size}_{instance}.txt"
        output_file = f"generalized_BKIP_{size}_{instance}_{setting}.json"
    return instance_file, output_file

def get_uncertainty_parameters(setting):
    if setting == 1 or setting == 2:
        uncertainty = 0.1
    else:
        uncertainty = 0.1

    if setting == 1 or setting == 3:
        conservatism = 0.1
    else:
        conservatism = 0.5
    return uncertainty, conservatism

def min_max_main(sizes, instances, settings, randint):
    for size in sizes:
        for instance in instances:
            for setting in settings:
                uncertainty, conservatism = get_uncertainty_parameters(setting)
                # Get the instance data.
                instance_file, result = get_files(
                    'True',
                    size,
                    instance,
                    setting
                )
                    
                devs = generate_deviations(
                    instance_file,
                    uncertainty,
                    randint
                )
                
                ins_cmd = instance_cmd(
                    instance_file,
                    conservatism,
                    devs
                )
                
                # Run the heuristic with the bkpsolver.
                if 'True' in randint:
                    output_dir = 'results/BKIP/bkp/randint'
                if 'False' in randint:
                    output_dir = 'results/BKIP/bkp/cont'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_file = f"{output_dir}/{result}"
                cmd = f"python3 -m src.min_max_heuristic --modify True {ins_cmd} --output_file {output_file}"
                out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

                # Run the heuristic with the BnC approach.
                if 'True' in randint:
                    output_dir = 'results/BKIP/bnc/randint'
                else:
                    output_dir = 'results/BKIP/bnc/cont'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_file = f"{output_dir}/{result}"
                cmd = f"python3 -m src.min_max_heuristic --solver ic --modify True {ins_cmd} --output_file {output_file}"
                out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

                # Run the greedy heuristic.
                if 'True' in randint:
                    output_dir = 'results/BKIP/greedy/randint'
                else:
                    output_dir = 'results/BKIP/greedy/cont'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_file = f"{output_dir}/{result}"
                cmd = f"python3 -m src.greedy_interdiction {ins_cmd} --output_file {output_file}"
                out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
        
def run_one_shot_heuristic(instance_file, conservatism, deviations, output_file):
    """Run the ONE-SHOT heuristic."""
    cmd = 'python3 -m src.iterate_heuristic --instance_file {} --conservatism {} --deviations {} --output_file {} --one_shot True'.format(
        instance_file,
        conservatism,
        deviations,
        output_file
    )
    out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

def run_iterate_heuristic(instance_file, conservatism, deviations, output_file):
    """Run the ITERATE heuristic."""
    cmd = 'python3 -m src.iterate_heuristic --instance_file {} --conservatism {} --deviations {} --output_file {}'.format(
        instance_file,
        conservatism,
        deviations,
        output_file
    )
    out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

def run_heuristic(instance_file, conservatism, deviations, output_file, refine):
    """Run the general heuristic presented in the paper."""
    cmd = 'python3 -m src.general_heuristic --instance_file {} --conservatism {} --deviations {} --output_file {}'.format(
        instance_file,
        conservatism,
        deviations,
        output_file
    )
    out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

def run_refined_heuristic(instance_file, conservatism, deviations, output_file):
    """Run the general heuristic presented in the paper."""
    cmd = 'python3 -m src.general_heuristic --instance_file {} --conservatism {} --deviations {} --output_file {} --refine True'.format(
        instance_file,
        conservatism,
        deviations,
        output_file
    )
    out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    
def run_general_exact(instance_file, conservatism, deviations, output_file):
    cmd = 'python3 -m src.gamma_robust_extended_model --instance_file {} --conservatism {} --deviations {} --output_file {}'.format(
        instance_file,
        conservatism,
        deviations,
        output_file
    )
    out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

def general_main(sizes, instances, settings, randint):
    for size in sizes:
        for instance in instances:
            for setting in settings:
                uncertainty, conservatism = get_uncertainty_parameters(setting)
                # Get the instance data.
                instance_file, result = get_files(
                    'False',
                    size,
                    instance,
                    setting
                )
                    
                devs = generate_deviations(
                    instance_file,
                    uncertainty,
                    randint
                )
                
                ins_cmd = instance_cmd(
                    instance_file,
                    conservatism,
                    devs
                )
                
                # Run the heuristic presented in the paper.
                if 'True' in randint:
                    output_dir = 'results/generalized-BKIP/heuristic/randint'
                if 'False' in randint:
                    output_dir = 'results/generalized-BKIP/heuristic/cont'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_file = f"{output_dir}/{result}"
                cmd = f"python3 -m src.general_heuristic {ins_cmd} --output_file {output_file}"
                out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

                # Run the ONE-SHOT heuristic.
                if 'True' in randint:
                    output_dir = 'results/generalized-BKIP/one-shot/randint'
                else:
                    output_dir = 'results/generalized-BKIP/one-shot/cont'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_file = f"{output_dir}/{result}"
                cmd = f"python3 -m src.iterate_heuristic --one_shot True {ins_cmd} --output_file {output_file}"
                out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

                # Run the ITERATE heuristic.
                if 'True' in randint:
                    output_dir = 'results/generalized-BKIP/iterate/randint'
                else:
                    output_dir = 'results/generalized-BKIP/iterate/cont'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_file = f"{output_dir}/{result}"
                cmd = f"python3 -m src.iterate_heuristic {ins_cmd} --output_file {output_file}"
                out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

                # Run the exact branch-and-cut.
                if 'True' in randint:
                    output_dir = 'results/generalized-BKIP/exact/randint'
                else:
                    output_dir = 'results/generalized-BKIP/exact/cont'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_file = f"{output_dir}/{result}"
                cmd = f"python3 -m src.gamma_robust_extended_model {ins_cmd} --output_file {output_file}"
                out = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--randint', default='True',
                        help='Integer deviations (True) or continuous deviations (False).')
    arguments = parser.parse_args()
    randint = arguments.randint
    
    sizes = [5*idx for idx in range(7,21)]
    instances = [idx for idx in range(1,11)]
    settings = [idx for idx in range(1,5)]
    min_max_main(sizes, instances, settings, randint)
    general_main(sizes, instances, settings, randint)
