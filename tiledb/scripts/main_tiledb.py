#!/usr/bin/env python3

import sys
import os

# Add the scripts directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from arraydb_generate_array import create_array
from arraydb_calculation import execute_operations

experiment_no:int=1

def main():
    try:
        # Define array parameters
        array_name = os.path.join(current_dir, "large_tiledb_array")
        tiledb_experiment(array_name,100,100)
        #tiledb_experiment(array_name,200,200)

    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

def tiledb_experiment(array_name, rows: int, cols:int):
        global experiment_no
        print(f"\nExperiment {str(experiment_no)}: TileDb Creating and generating array data with {str(rows)} x {str(cols)} array ...")
        create_array(
            array_name=array_name,
            rows=rows,
            cols=cols
        )
        print(f"\n\tCalculating array operations with {str(rows)} x {str(cols)} array ...")
        execute_operations(array_name)
        experiment_no = experiment_no + 1


if __name__ == "__main__":
    main()
