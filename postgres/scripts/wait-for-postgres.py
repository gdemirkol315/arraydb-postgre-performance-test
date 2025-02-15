import time
import psycopg2
import os
import subprocess
import sys
import logging

def wait_for_postgres():
    """Wait for PostgreSQL to become available."""
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL environment variable is not set")
        return False
    max_retries = 30  # Maximum number of retries
    retry_interval = 2  # Time between retries in seconds
    logging.getLogger("PostgreSQL")
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(db_url)
            conn.close()
            logging.info("Successfully connected to PostgreSQL!")
            return True
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                logging.error(f"Connection failed: {str(e)}")
                logging.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                logging.error("Max retries reached. Could not connect to PostgreSQL.")
                return False
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return False

def main():
    logging.getLogger("PostgreSQL")
    """Main function to wait for PostgreSQL and then run the main script."""
    if wait_for_postgres():
        logging.info("Running main application script...")
        try:
            # Run the main application script
            result = subprocess.run(["python", "/app/scripts/main_postgre.py"], check=True)
            sys.exit(result.returncode)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running main script: {e}")
            sys.exit(e.returncode)
        except Exception as e:
            logging.error(f"Unexpected error running main script: {e}")
            sys.exit(1)
    else:
        logging.error("Failed to connect to PostgreSQL. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
