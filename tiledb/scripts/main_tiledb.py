#!/usr/bin/env python3

import sys
import os
import logging
# Add the scripts directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if current_dir not in sys.path:
    sys.path.append(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from arraydb_generate_array import create_array
from arraydb_calculation import execute_operations
from utils.performance_monitor import PerformanceMonitor  # Now accessible through PYTHONPATH

experiment_no:int=1
monitor = PerformanceMonitor("TileDB")

def main():
    try:
        # Define array parameters
        array_name = os.path.join(current_dir, "large_tiledb_array")
        tiledb_experiment(array_name,100,100)
        tiledb_experiment(array_name,500,500)
        tiledb_experiment(array_name,2000,2000)

    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

def tiledb_experiment(array_name, rows: int, cols:int):
        global experiment_no
        logger = logging.getLogger("TileDB")
        operation_name = f"Experiment {experiment_no} ({rows}x{cols})"
        
        # Monitor array creation
        monitor.start_operation(f"Array Creation - {operation_name}")
        create_array(
            array_name=array_name,
            rows=rows,
            cols=cols
        )
        monitor.end_operation(f"Array Creation - {operation_name}")
        
        # Monitor operations execution
        monitor.start_operation(f"Array Operations - {operation_name}")
        execute_operations(array_name)
        monitor.end_operation(f"Array Operations - {operation_name}")
        
        experiment_no = experiment_no + 1
        logger.info("-" * 50)

if __name__ == "__main__":
    main()
