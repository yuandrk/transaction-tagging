from ofxparse import OfxParser
import sys
import pprint

def parse_ofx(file_path):
    with open(file_path, 'rb') as file:
        ofx = OfxParser.parse(file)
    
    transactions = {}
    for txn in ofx.account.statement.transactions:
        txn_id = getattr(txn, 'id', 'N/A')  # Use transaction ID or a placeholder if not present
        transactions[txn_id] = {
            'amount': txn.amount,
            'date': txn.date.strftime('%Y-%m-%d %H:%M:%S'),  # Format datetime object
            'payee': getattr(txn, 'payee', 'N/A')  # Safely get the payee if available
        }
    
    return transactions

def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_ofx_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    transactions = parse_ofx(file_path)
    
    print("Transactions Details:")
    for txn_id, details in transactions.items():
        pprint.pprint(f"ID: {txn_id}, Amount: {details['amount']}, Date: {details['date']}, Payee: {details['payee']}")

if __name__ == '__main__':
    main()

