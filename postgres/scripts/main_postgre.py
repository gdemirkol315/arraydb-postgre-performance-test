#!/usr/bin/env python3

import sys
import os

# Add the scripts directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from postgre_generate_array import create_and_generate_array


def main():
    try:
        # Get database credentials from environment variables
        DB_USER = os.getenv('POSTGRES_USER', 'testuser')
        DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'testpassword')
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_NAME = os.getenv('POSTGRES_DB', 'testdb')

        # Create the PostgreSQL URL
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        
        create_and_generate_array(1000,1000)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
