import sys
import logging
from ofxparse import OfxParser
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def setup_database():
    """Create or connect to an SQLite database and set up the transactions table."""
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            amount INTEGER,
            date TEXT,
            payee TEXT
        )
    ''')
    conn.commit()
    conn.close()

def parse_ofx(file_path):
    """Parse the OFX file and extract transactions."""
    try:
        with open(file_path, 'rb') as file:
            ofx = OfxParser.parse(file)
    except Exception as e:
        logging.error(f"Failed to open or parse the OFX file: {e}")
        return {}

    transactions = {}
    for txn in ofx.account.statement.transactions:
        txn_id = getattr(txn, 'id', 'N/A')
        # Convert amount to integer representing the smallest currency unit
        amount_in_cents = int(txn.amount * 100)
        transactions[txn_id] = {
            'amount': amount_in_cents,
            'date': txn.date.strftime('%Y-%m-%d %H:%M:%S'),
            'payee': getattr(txn, 'payee', 'N/A')
        }
    return transactions

def save_transactions_to_db(transactions):
    """Save the parsed transactions to the SQLite database."""
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    for txn_id, txn_details in transactions.items():
        cursor.execute('''
            INSERT OR REPLACE INTO transactions (id, amount, date, payee)
            VALUES (?, ?, ?, ?)
        ''', (txn_id, txn_details['amount'], txn_details['date'], txn_details['payee']))
    conn.commit()
    conn.close()
    logging.info("Transactions have been saved to the database.")

def main():
    if len(sys.argv) < 2:
        logging.error("Usage: python script_name.py <path_to_ofx_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    setup_database()  # Ensure the database is ready
    transactions = parse_ofx(file_path)
    save_transactions_to_db(transactions)

if __name__ == '__main__':
    main()
