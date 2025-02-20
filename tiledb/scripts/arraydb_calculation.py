import tiledb
import numpy as np
import logging
from utils.performance_monitor import PerformanceMonitor

def calculate_category_stats(data, category_name, min_val, max_val):
    """Calculate statistics for a specific category of data."""
    mask = (data >= min_val) & (data <= max_val)
    category_data = data[mask]
    
    if len(category_data) > 0:
        return {
            'name': category_name,
            'count': len(category_data),
            'sum': np.sum(category_data),
            'average': np.mean(category_data)
        }
    return None

def execute_operations(array_name, row_start=0, row_end=49, col_start=0, col_end=49):
    logger = logging.getLogger("TileDB")
    
    # Define categories
    categories = [
        ('Low Range', 0, 30),
        ('Mid Range', 31, 60),
        ('High Range', 61, 100)
    ]
    
    try:
        with tiledb.DenseArray(array_name, mode="r") as array:
            data_slice = array[row_start:row_end+1, col_start:col_end+1]["a"]
            
            # Measure overall statistics calculation
            logger.info("\n=== Overall Statistics Performance ===")
            monitor = PerformanceMonitor("TileDB")
            monitor.start_operation("Overall Statistics Calculation")
            
            total_sum = np.sum(data_slice)
            total_average = np.mean(data_slice)
            
            monitor.end_operation("Overall Statistics Calculation")
            
            # Measure category-wise statistics calculation
            logger.info("\n=== Category-wise Statistics Performance ===")
            monitor.start_operation("Category-wise Statistics Calculation")
            
            category_stats = []
            for cat_name, min_val, max_val in categories:
                stats = calculate_category_stats(data_slice, cat_name, min_val, max_val)
                if stats:
                    category_stats.append(stats)
            
            monitor.end_operation("Category-wise Statistics Calculation")
                    
    except Exception as e:
        logger.error(f"Error querying array: {str(e)}")
        raise

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
    

if __name__ == "__main__":
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    array_name = os.path.join(current_dir, "large_tiledb_array")
    execute_operations(array_name)
