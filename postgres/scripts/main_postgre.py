#!/usr/bin/env python3

import sys
import os

# Add the scripts directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from sqlalchemy import create_engine
from postgre_generate_array import create_array
from postgre_calculation import execute_operations

experiment_no: int = 1

def main():
    try:
        # Get database URL from environment variable
        DATABASE_URL = os.environ["DATABASE_URL"]
        
        # Create the SQLAlchemy engine
        engine = create_engine(DATABASE_URL)
        
        postgre_experiment(engine,100,100)
        #postgre_experiment(engine,200,200)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

def postgre_experiment(database, rows: int, cols: int):
    global experiment_no
    
    print(f"\nExperiment {str(experiment_no)}: Postgre Creating and generating array data with {str(rows)} x {str(cols)} array ...")
    create_array(database, rows, cols)

    print(f"\n\tCalculating array operations with {str(rows)} x {str(cols)} array ...")
    execute_operations(database)
    experiment_no = experiment_no + 1

if __name__ == "__main__":
    main()
