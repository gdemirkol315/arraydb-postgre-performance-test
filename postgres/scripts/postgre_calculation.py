from sqlalchemy import text
import logging

from sqlalchemy import text
import logging
from utils.performance_monitor import PerformanceMonitor

def execute_operations(engine, row_start=0, row_end=49, col_start=0, col_end=49):
    logger = logging.getLogger("PostgreSQL")
    monitor = PerformanceMonitor("PostgreSQL")

    # Define categories
    categories = [
        ('Low Range', 0, 30),
        ('Mid Range', 31, 60),
        ('High Range', 61, 100)
    ]

    try:
        with engine.connect() as conn:
            # Measure overall statistics calculation
            logger.info("\n=== Overall Statistics Performance ===")
            monitor.start_operation("Overall Statistics Calculation")
            
            overall_query = text("""
                SELECT SUM(value) AS total_sum, AVG(value) AS average
                FROM large_array
                WHERE row BETWEEN :row_start AND :row_end
                AND col BETWEEN :col_start AND :col_end;
            """).bindparams(row_start=row_start, row_end=row_end, col_start=col_start, col_end=col_end)

            overall_result = conn.execute(overall_query).fetchone()
            total_sum = overall_result[0]
            total_average = overall_result[1]
            
            monitor.end_operation("Overall Statistics Calculation")

            # Measure category-wise statistics calculation
            logger.info("\n=== Category-wise Statistics Performance ===")
            monitor.start_operation("Category-wise Statistics Calculation")
            
            category_stats = []
            for cat_name, min_val, max_val in categories:
                cat_query = text("""
                    SELECT 
                        COUNT(*) as count,
                        SUM(value) as sum,
                        AVG(value) as average
                    FROM large_array
                    WHERE row BETWEEN :row_start AND :row_end
                    AND col BETWEEN :col_start AND :col_end
                    AND value BETWEEN :min_val AND :max_val;
                """).bindparams(
                    row_start=row_start, 
                    row_end=row_end, 
                    col_start=col_start, 
                    col_end=col_end,
                    min_val=min_val,
                    max_val=max_val
                )

                cat_result = conn.execute(cat_query).fetchone()
                if cat_result[0] > 0:  # if count > 0
                    category_stats.append({
                        'name': cat_name,
                        'count': cat_result[0],
                        'sum': cat_result[1],
                        'average': cat_result[2]
                    })
            
            monitor.end_operation("Category-wise Statistics Calculation")

        # Log the results in consistent format
        logger.info("\n=== Results ===")
        logger.info("Overall Calculation Results:")
        logger.info(f"Total sum of all values: {total_sum}")
        logger.info(f"Overall average: {total_average}")
        logger.info("\nCategory-wise Results:")

        for stats in category_stats:
            logger.info(f"\n{stats['name']}:")
            logger.info(f"  Count: {stats['count']} numbers")
            logger.info(f"  Sum: {stats['sum']}")
            logger.info(f"  Average: {stats['average']:.2f}")

        logger.info("")
        
        return total_sum, total_average, category_stats
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        raise
