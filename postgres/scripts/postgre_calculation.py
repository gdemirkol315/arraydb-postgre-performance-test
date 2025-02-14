from sqlalchemy import text
import time

def execute_operations(engine, row_start=0, row_end=49, col_start=0, col_end=49):

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
    print("\tResults for Calculation:")
    print("\tSum of values in slice:", total_sum)
    print("\tMean of values in slice:", average)
    print(f"\tSlice calculation time: {end_time - start_time:.4f} seconds")
    
    return total_sum, average
