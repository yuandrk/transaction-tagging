import sqlite3
import logging
from ia_parsing import create_category


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def setup_database():
    """Create or connect to an SQLite database and set up the transactions and categories tables."""
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            amount INTEGER,
            date TEXT,
            payee TEXT,
            category_id INTEGER  -- Add category_id column
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
    
def save_transactions_to_db(transactions):
    """Save the parsed transactions to the SQLite database."""
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    for txn_id, txn_details in transactions.items():
        payee = txn_details['payee']
        category = create_category(payee)
        cursor.execute('''
            INSERT OR REPLACE INTO transactions (id, amount, date, payee, category_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (txn_id, txn_details['amount'], txn_details['date'], payee, category))
    conn.commit()
    conn.close()
    logging.info("Transactions have been saved to the database.")
