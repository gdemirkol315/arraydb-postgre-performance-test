from sqlalchemy import text
import logging

def execute_operations(engine, row_start=0, row_end=49, col_start=0, col_end=49):
    logger = logging.getLogger("PostgreSQL")

    # Query to calculate the sum and mean within the slice
    query = text("""
        SELECT SUM(value) AS total_sum, AVG(value) AS average
        FROM large_array
        WHERE row BETWEEN :row_start AND :row_end
        AND col BETWEEN :col_start AND :col_end;
    """).bindparams(row_start=row_start, row_end=row_end, col_start=col_start, col_end=col_end)

    try:
        with engine.connect() as conn:
            result = conn.execute(query).fetchone()

        # Access the results using indices
        total_sum = result[0]
        average = result[1]

        # Log the results in consistent format
        logger.info("Calculation Results:")
        logger.info(f"Sum of values in slice: {total_sum}")
        logger.info(f"Mean of values in slice: {average}")
        logger.info("")
        
        
        return total_sum, average
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        raise
