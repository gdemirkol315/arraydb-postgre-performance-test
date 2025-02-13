import tiledb
import numpy as np
import time

def query_array(array_name, row_start=0, row_end=49, col_start=0, col_end=49):
    """
    Query a TileDB array and calculate sum and average for a specific slice.
    
    Args:
        array_name (str): Path to the TileDB array
        row_start (int): Start index for rows
        row_end (int): End index for rows
        col_start (int): Start index for columns
        col_end (int): End index for columns
        
    Returns:
        tuple: (total_sum, average, query_time)
    """
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

    print("TileDB Results for Calculation:")
    print(f"Slice dimensions: {data_slice.shape}")
    print(f"Sum of values in slice: {total_sum}")
    print(f"Mean of values in slice: {average}")
    print(f"Query calculation time: {query_time:.4f} seconds")
    
    return total_sum, average, query_time

if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    array_name = os.path.join(current_dir, "large_tiledb_array")
    query_array(array_name)
