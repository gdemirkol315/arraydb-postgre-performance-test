#!/usr/bin/env python3

import sys
import os

# Add the scripts directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from sqlalchemy import create_engine
from postgre_generate_array import create_array, calculate_slice


def main():
    try:
        # Get database URL from environment variable
        DATABASE_URL = os.environ["DATABASE_URL"]
        
        # Create the SQLAlchemy engine
        engine = create_engine(DATABASE_URL)
        
        print("\nStep 1: Postgre Creating and generating array data with 100 x 100 array ...")
        # Create the array
        create_array(engine, 100, 100)
        print("\nStep 2: Postgre Calculating array operations with 100 x 100 array ...")
        # Calculate slice statistics
        calculate_slice(engine)
        
        print("\nStep 3: Postgre Creating and generating array data with 100 x 100 array ...")
                # Create the array
        create_array(engine, 1000, 1000)
        
        print("\nStep 4: Postgre Calculating array operations with 100 x 100 array ...")
        # Calculate slice statistics
        calculate_slice(engine)

        print("\nStep 5: Postgre Creating and generating array data with 100 x 100 array ...")
        create_array(engine, 10000, 10000)
        
        print("\nStep 6: Postgre Calculating array operations with 100 x 100 array ...")
        calculate_slice(engine)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
