import numpy as np
from sqlalchemy import create_engine, text
import time
import os

def create_and_generate_array(rows:int, cols:int):
    print("Step 1: Creating and generating array data...")
    print("PostgreSQL starting deleting and inserting data")
    # Start the timer
    start_time = time.time()

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


    print("Step 2: Calculating sum and mean within slice...")
    # Define the slice
    row_start, row_end = 100, 200
    col_start, col_end = 300, 400

    # Query to calculate the sum and mean within the slice
    query = text("""
        SELECT SUM(value) AS total_sum, AVG(value) AS average
        FROM large_array
        WHERE row BETWEEN :row_start AND :row_end
        AND col BETWEEN :col_start AND :col_end;
    """).bindparams(row_start=row_start, row_end=row_end, col_start=col_start, col_end=col_end)

    # Time the query execution
    start_time = time.time()

    with engine.connect() as conn:
        result = conn.execute(query).fetchone()
    end_time = time.time()

    # Access the results using indices
    total_sum = result[0]
    average = result[1]

    # Print the results
    print("PostgreSQL Results for Calculation:")
    print("Sum of values in slice:", total_sum)
    print("Mean of values in slice:", average)
    print(f"PostgreSQL slice calculation time: {end_time - start_time:.4f} seconds")
