import time
import psycopg2
import os
import subprocess
import sys

def wait_for_postgres():
    """Wait for PostgreSQL to become available."""
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL environment variable is not set")
        return False
    max_retries = 30  # Maximum number of retries
    retry_interval = 2  # Time between retries in seconds

    for attempt in range(max_retries):
        try:
            print(f"Attempting to connect to PostgreSQL (attempt {attempt + 1}/{max_retries})...")
            conn = psycopg2.connect(db_url)
            conn.close()
            print("Successfully connected to PostgreSQL!")
            return True
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Connection failed: {str(e)}")
                print(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                print("Max retries reached. Could not connect to PostgreSQL.")
                return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

def main():
    """Main function to wait for PostgreSQL and then run the main script."""
    if wait_for_postgres():
        print("Running main application script...")
        try:
            # Run the main application script
            result = subprocess.run(["python", "/app/scripts/postgre-generate-array.py"], check=True)
            sys.exit(result.returncode)
        except subprocess.CalledProcessError as e:
            print(f"Error running main script: {e}")
            sys.exit(e.returncode)
        except Exception as e:
            print(f"Unexpected error running main script: {e}")
            sys.exit(1)
    else:
        print("Failed to connect to PostgreSQL. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
