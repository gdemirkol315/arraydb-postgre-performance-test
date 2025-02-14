import tiledb
import numpy as np
import logging

def execute_operations(array_name, row_start=0, row_end=49, col_start=0, col_end=49):
    logger = logging.getLogger("TileDB")
    
    try:
        with tiledb.DenseArray(array_name, mode="r") as array:
            data_slice = array[row_start:row_end+1, col_start:col_end+1]["a"]
            total_sum = np.sum(data_slice)
            average = np.mean(data_slice)
    except Exception as e:
        logger.error(f"Error querying array: {str(e)}")
        raise
        

    # Log the results in consistent format
    logger.info("Calculation Results:")
    logger.info(f"Sum of values in slice: {total_sum}")
    logger.info(f"Mean of values in slice: {average}")
    logger.info("")
    

if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    array_name = os.path.join(current_dir, "large_tiledb_array")
    execute_operations(array_name)
