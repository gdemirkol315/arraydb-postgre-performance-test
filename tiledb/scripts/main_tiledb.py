#!/usr/bin/env python3

import sys
import os

# Add the scripts directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from arraydb_generate_array import create_and_generate_array
from arraydb_calculation_query import query_array

def main():
    try:
        # Define array parameters
        array_name = os.path.join(current_dir, "large_tiledb_array")
        # Step 1: Create and generate the array
        print("\nStep 1: Tiledb Creating and generating array data with 100 x 100 array ...")
        generation_time = create_and_generate_array(
            array_name=array_name,
            rows=100,
            cols=100
        )
        print(f"Array creation and data generation completed in {generation_time:.4f} seconds")

        # Step 2: Perform the calculation query
        print("\nStep 2: Tiledb Performing calculation query with 100 x 100 array ...")
        total_sum, average, query_time = query_array(array_name)
        print("\nAll operations completed successfully!")
        print(f"Total execution time: {generation_time + query_time:.4f} seconds")

        # Step 3: Create and generate the array
        print("\nStep 3: Tiledb Creating and generating array data with 1.000 x 1.000 array ...")
        generation_time = create_and_generate_array(
            array_name=array_name,
            rows=1000,
            cols=1000
        )
        print(f"Array creation and data generation completed in {generation_time:.4f} seconds")

        # Step 4: Perform the calculation query
        print("\nStep 4: Tiledb Performing calculation query with 1.000 x 1.000 array ...")
        total_sum, average, query_time = query_array(array_name)
        print("\nAll operations completed successfully!")
        print(f"Total execution time: {generation_time + query_time:.4f} seconds")

        # Step 5: Create and generate the array
        print("\nStep 5: Tiledb Creating and generating array data with 10.000 x 10.000 array ...")
        generation_time = create_and_generate_array(
            array_name=array_name,
            rows=10000,
            cols=10000
        )
        print(f"Array creation and data generation completed in {generation_time:.4f} seconds")

        # Step 6: Perform the calculation query
        print("\nStep 6: Tiledb Performing calculation query with 10.000 x 10.000 array ...")
        total_sum, average, query_time = query_array(array_name)
        print("\nAll operations completed successfully!")
        print(f"Total execution time: {generation_time + query_time:.4f} seconds")

    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
