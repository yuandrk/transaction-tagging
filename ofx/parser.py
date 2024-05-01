import logging
from ofxparse import OfxParser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

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
        amount_in_cents = int(txn.amount * 100)
        transactions[txn_id] = {
            'amount': amount_in_cents,
            'date': txn.date.strftime('%Y-%m-%d %H:%M:%S'),
            'payee': getattr(txn, 'payee', 'N/A')
        }
    return transactions