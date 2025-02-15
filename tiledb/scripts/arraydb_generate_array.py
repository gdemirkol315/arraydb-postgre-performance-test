import numpy as np
import tiledb
import shutil
import os

def create_array(array_name="large_tiledb_array", rows=100, cols=100):

    # Clean up existing array if it exists
    if os.path.exists(array_name):
        print("\tRemoving existing TileDB array...")
        shutil.rmtree(array_name)

    # Generate a large 2D array
    data = np.random.randint(0, 100, size=(rows, cols))

    # Calculate tile size based on array dimensions
    min_dimension = min(rows, cols)
    if min_dimension <= 100:
        tile_size = 2  # Fixed very small tile size for small arrays
    else:
        tile_size = min(min_dimension // 10, min_dimension - 2)  # Ensure we stay well below domain size
    logger = logging.getLogger("TileDB")
    logger.info(f"Used tile size: {tile_size} for array dimensions: {rows}x{cols}")
    
    # Define the TileDB schema
    schema = tiledb.ArraySchema(
        domain=tiledb.Domain(
            tiledb.Dim(name="rows", domain=(0, rows - 1), tile=tile_size, dtype="int32"),
            tiledb.Dim(name="cols", domain=(0, cols - 1), tile=tile_size, dtype="int32"),
        ),
        sparse=False,
        attrs=[tiledb.Attr(name="a", dtype="int32")],
    )

    # Create the TileDB array
    tiledb.DenseArray.create(array_name, schema)

    # Write data to TileDB
    with tiledb.DenseArray(array_name, mode="w") as array:
        array[:] = {"a": data}

if __name__ == "__main__":
    create_array()
