import tiledb
import numpy as np
import time

# Define the slice
row_start, row_end = 100, 200
col_start, col_end = 300, 400

start_time = time.time()
with tiledb.DenseArray("large_tiledb_array", mode="r") as array:
    data_slice = array[row_start:row_end+1, col_start:col_end+1]["a"]
    total_sum = np.sum(data_slice)
    average = np.mean(data_slice)
end_time = time.time()

print("TileDB Results for Calculation:")
print("Sum of values in slice:", total_sum)
print("Mean of values in slice:", average)
print(f"TileDB slice calculation time: {end_time - start_time:.4f} seconds")
