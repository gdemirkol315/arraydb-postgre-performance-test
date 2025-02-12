import numpy as np
import tiledb
import shutil
import os
import time

print("TileDB starting deleting and inserting data")
# Start the timer
start_time = time.time()

if os.path.exists("large_tiledb_array"):
    print("Removing existing TileDB array...")
    shutil.rmtree("large_tiledb_array")

# Generate a large 2D array
rows, cols = 10000, 10000
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
tiledb.DenseArray.create("large_tiledb_array", schema)

# Write data to TileDB
with tiledb.DenseArray("large_tiledb_array", mode="w") as array:
    array[:] = {"a": data}

print("Data stored in TileDB.")
# End the timer
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds")
