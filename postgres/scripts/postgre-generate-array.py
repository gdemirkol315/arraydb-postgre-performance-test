import numpy as np
from sqlalchemy import create_engine, text
import time
import os

print("PostgreSQL starting deleting and inserting data")
# Start the timer
start_time = time.time()

# Generate a large 2D array
rows, cols = 10, 10  # Adjust the size as needed
data = np.random.randint(0, 100, size=(rows, cols))

# Create PostgreSQL connection
engine = create_engine(os.environ["DATABASE_URL"])

# Create a table
with engine.begin() as conn:
    # Drop the table if it exists
    conn.execute(text("DROP TABLE IF EXISTS large_array;"))
    
    # Create a new table
    conn.execute(text("""
        CREATE TABLE large_array (
            row INT,
            col INT,
            value INT
        );
    """))

# Flatten and insert data (convert numpy.int64 to Python int)
flattened_data = [{"row": int(r), "col": int(c), "value": int(data[r, c])}
                  for r in range(rows) for c in range(cols)]

# Use a connection for batch insertion
with engine.begin() as conn:
    # Perform batch insert using parameterized query
    insert_query = text("INSERT INTO large_array (row, col, value) VALUES (:row, :col, :value)")
    conn.execute(insert_query, flattened_data)

print("Data stored in PostgreSQL.")
# End the timer
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.4f} seconds")
