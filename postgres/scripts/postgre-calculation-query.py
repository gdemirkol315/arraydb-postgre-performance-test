from sqlalchemy import create_engine, text
import time
import os

# Get database credentials from environment variables
DB_USER = os.getenv('POSTGRES_USER', 'testuser')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'testpassword')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('POSTGRES_DB', 'testdb')

# Create the PostgreSQL engine using environment variables
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Define the slice
row_start, row_end = 100, 200
col_start, col_end = 300, 400

# Query to calculate the sum and mean within the slice
query = text("""
    SELECT SUM(value) AS total_sum, AVG(value) AS average
    FROM large_array
    WHERE row BETWEEN {row_start} AND {row_end}
    AND col BETWEEN {col_start} AND {col_end};
""")

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
