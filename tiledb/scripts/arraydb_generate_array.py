import numpy as np
import tiledb
import shutil
import os
import time

def create_and_generate_array(array_name="large_tiledb_array", rows=10000, cols=10000):
    """
    Create and generate a TileDB array with random data.
    
    Args:
        array_name (str): Name of the TileDB array
        rows (int): Number of rows in the array
        cols (int): Number of columns in the array
    """
    print("TileDB starting deleting and inserting data")
    start_time = time.time()

    # Clean up existing array if it exists
    if os.path.exists(array_name):
        print("Removing existing TileDB array...")
        shutil.rmtree(array_name)

    # Generate a large 2D array
    data = np.random.randint(0, 100, size=(rows, cols))
    print("Generated a large array with shape:", data.shape)

    # Define the TileDB schema
    schema = tiledb.ArraySchema(
        domain=tiledb.Domain(
            tiledb.Dim(name="rows", domain=(0, rows - 1), tile=1000, dtype="int32"),
            tiledb.Dim(name="cols", domain=(0, cols - 1), tile=1000, dtype="int32"),
        ),
        sparse=False,
        attrs=[tiledb.Attr(name="a", dtype="int32")],
    )

    # Create the TileDB array
    tiledb.DenseArray.create(array_name, schema)

    # Write data to TileDB
    with tiledb.DenseArray(array_name, mode="w") as array:
        array[:] = {"a": data}

    print("Data stored in TileDB.")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")
    
    return elapsed_time

if __name__ == "__main__":
    create_and_generate_array()
