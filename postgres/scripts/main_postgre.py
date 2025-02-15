#!/usr/bin/env python3
import logging
import sys
import os

# Add the scripts directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if current_dir not in sys.path:
    sys.path.append(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from sqlalchemy import create_engine
from postgre_generate_array import create_array
from postgre_calculation import execute_operations
from utils.performance_monitor import PerformanceMonitor  # Now accessible through PYTHONPATH

experiment_no: int = 1
monitor = PerformanceMonitor("PostgreSQL")

def main():
    try:
        # Get database URL from environment variable
        DATABASE_URL = os.environ["DATABASE_URL"]
        
        # Create the SQLAlchemy engine
        engine = create_engine(DATABASE_URL)
        
        postgre_experiment(engine,100,100)
        postgre_experiment(engine,500,500)
        postgre_experiment(engine,2000,2000)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

def postgre_experiment(database, rows: int, cols: int):
    global experiment_no
    operation_name = f"Experiment {experiment_no} ({rows}x{cols})"
    
    # Monitor array creation
    monitor.start_operation(f"Array Creation - {operation_name}")
    create_array(database, rows, cols)
    monitor.end_operation(f"Array Creation - {operation_name}")

    # Monitor operations execution
    monitor.start_operation(f"Array Operations - {operation_name}")
    execute_operations(database)
    monitor.end_operation(f"Array Operations - {operation_name}")
    
    experiment_no = experiment_no + 1
    logger = logging.getLogger("PostgreSQL")
    logger.info("-" * 50)

if __name__ == "__main__":
    main()
