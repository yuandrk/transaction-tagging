import sys
import logging
from database import setup_database, save_transactions_to_db
from parser import parse_ofx

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    if len(sys.argv) < 2:
        logging.error("Usage: python main.py <path_to_ofx_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    setup_database()  # Ensure the database is ready
    transactions = parse_ofx(file_path)
    save_transactions_to_db(transactions)

if __name__ == '__main__':
    main()
