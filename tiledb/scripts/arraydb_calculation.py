import tiledb
import numpy as np
import time

def execute_operations(array_name, row_start=0, row_end=49, col_start=0, col_end=49):
   
    start_time = time.time()
    
    try:
        with tiledb.DenseArray(array_name, mode="r") as array:
            data_slice = array[row_start:row_end+1, col_start:col_end+1]["a"]
            total_sum = np.sum(data_slice)
            average = np.mean(data_slice)
    except Exception as e:
        print(f"Error querying array: {str(e)}")
        raise
        
    end_time = time.time()
    query_time = end_time - start_time

    # Print the results
    print("\tResults for Calculation:")
    print("\tSum of values in slice:", total_sum)
    print("\tMean of values in slice:", average)
    print(f"\tSlice calculation time: {query_time:.4f} seconds")
    

if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    array_name = os.path.join(current_dir, "large_tiledb_array")
    execute_operations(array_name)
