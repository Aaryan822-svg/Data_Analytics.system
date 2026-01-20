#Reading Sales Data With Encoding Handling
import csv

encodings = ['utf-8', 'latin-1', 'utf-16']  ## List of possible encodings


def read_sales_data(filename, encodings):
    data = []  # Initialize an empty list to store the data
    try:

        with open(filename, mode='r', encoding=encodings, newline='\n', errors='replace') as f:
            reader = csv.reader(f, delimiter='|')

            header = next(reader, None)  # Skip header row

            for row in reader:
                if row and any(field.strip() for field in row):  # Check for non-empty row
                    # Clean and store the row
                    data.append('|'.join(row).strip())
        return data

    except UnicodeEncodeError:
        print(
            f"Error: Could not decode file {filename} with encoding {encodings}.")
        return data
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return data
    
#Parsing and cleaning Data
def parse_transactions(raw_lines):
    data = []
    for line in raw_lines:
        try:
            transaction_id, date, product_id, product_name, quantity, unit_price, customerID, region = [
                f.strip() for f in line.split('|')]

            # Handle commas within product names
            cleaned_product_name = product_name.replace(",", " ").strip()

            # Remove commas from numeric fields and convert to appropriate types
            cleaned_unit_price = float(unit_price.replace(',', '').strip())
            cleaned_quantity = int(quantity.replace(',', '').strip())

            # Validate numeric fields
            if cleaned_quantity <= 0 or cleaned_unit_price <= 0:     
                continue

            # Validate TransactionID format
            if not transaction_id.startswith('T'):  
                continue

            data.append({
                'TransactionID': transaction_id,
                'Date': date,
                'ProductID': product_id,
                'ProductName': cleaned_product_name,
                'Quantity': cleaned_quantity,
                'UnitPrice': cleaned_unit_price,
                'CustomerID': customerID,
                'Region': region
            })
        except (ValueError, AttributeError):
            continue  # skip invalid numeric values
    return data

#Data Validation And Filtering
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
 """

    required_fields = [
        'TransactionID',
        'ProductID',
        'CustomerID',
        'Region',
        'Quantity',
        'UnitPrice'
    ]

    # ---------------- Initialization ----------------
    total_input = len(transactions)  
    invalid_count = 0  
    valid_transactions = []  
    # ---------------- Validation ----------------

    for txn in transactions:

        # Check required fields
        if not all(field in txn and txn[field] not in (None, '') for field in required_fields):
            invalid_count += 1
            continue

        # Validate ID formats
        
        if not str (txn['TransactionID']).startswith(('T')):     
            invalid_count += 1        
            continue
        if not str (txn['ProductID']).startswith(('P')):
            invalid_count += 1        
            continue
        if not str (txn['CustomerID']).startswith(('C')):
            invalid_count += 1        
            continue

        # Validate Quantity and UnitPrice
        if txn['Quantity'] <= 0 or txn['UnitPrice'] <= 0:
            invalid_count += 1
            continue

        valid_transactions.append(txn)

    # ---------------- Display Regions ----------------
    regions = sorted({txn['Region'] for txn in valid_transactions})
    print("Available Regions:", regions)

    # ---------------- Display Amount Range ----------------
    amounts = [txn['Quantity'] * txn['UnitPrice']
               for txn in valid_transactions]

    if amounts:
        print(
            f"Transaction Amount Range: Min={min(amounts)}, Max={max(amounts)}")
    else:
        print("Transaction Amount Range: No valid transactions")

    # ---------------- Filtering ----------------
    filtered_by_region = 0       ## Initialize counters
    filtered_by_amount = 0         
    filtered_transactions = valid_transactions

    # Region Filter
    if region:
        before = len(filtered_transactions)
        filtered_transactions = [
            txn for txn in filtered_transactions
            if txn['Region'] == region
        ]
        filtered_by_region = before - len(filtered_transactions)
        print("Records after region filter:", len(filtered_transactions))

    # Amount Filter
    if min_amount is not None or max_amount is not None:
        before = len(filtered_transactions)
        temp = []

        for txn in filtered_transactions:
            amount = txn['Quantity'] * txn['UnitPrice']

            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue

            temp.append(txn)

        filtered_transactions = temp
        filtered_by_amount = before - len(filtered_transactions)
        print("Records after amount filter:", len(filtered_transactions))

    # ---------------- Summary ----------------
    filter_summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered_transactions)
    }

    return filtered_transactions,  filter_summary