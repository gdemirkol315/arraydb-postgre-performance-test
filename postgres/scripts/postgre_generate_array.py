import numpy as np
from sqlalchemy import text
import time

def create_array(engine, rows:int, cols:int):
    # Start the timer
    start_time = time.time()

    data = np.random.randint(0, 100, size=(rows, cols))

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

    # Insert data in batches of 100 rows
    batch_size = 100
    total_batches = (rows + batch_size - 1) // batch_size  # Calculate total number of batches
    
    with engine.begin() as conn:
        insert_query = text("INSERT INTO large_array (row, col, value) VALUES (:row, :col, :value)")
        
        for batch_num in range(total_batches):
            start_row = batch_num * batch_size
            end_row = min(start_row + batch_size, rows)
            
            # Create batch for current rows
            batch_data = [
                {"row": int(r), "col": int(c), "value": int(data[r, c])}
                for r in range(start_row, end_row)
                for c in range(cols)
            ]
            
            # Execute batch insert
            conn.execute(insert_query, batch_data)
    
    # End the timer
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print(f"\tData storage completed in {elapsed_time:.4f} seconds")
