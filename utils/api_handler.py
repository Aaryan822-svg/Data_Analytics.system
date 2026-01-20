#Fetching product data from DummyJSON API and enriching sales data
def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries
    """

    import requests

    url = "https://dummyjson.com/products?limit=100"    ## API endpoint

    # Initialize empty product list
    products = []

    try:
        # Send GET request to API
        response = requests.get(url, timeout=10)      ## Set timeout to 10 seconds

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()                    ## Parse JSON response
            products = data.get("products", [])      ## Extract product list
            print(" Products fetched successfully")

        else:
            print(" Failed to fetch products | Status Code:",
                  response.status_code)  ## Log failure

    except requests.exceptions.RequestException as e:
        #  Handle connection-related errors
        print(" API connection failed:", e)
        return []  ## Return empty list on failure

    #  Return product list (empty if failed)
    return products


# Create product mapping from API data
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters: api_products from fetch_all_products()

    Returns: dictionary mapping product IDs to info
    """

    #  Initialize empty mapping dictionary
    product_mapping = {}   ## Initialize empty mapping

    #  Iterate through API product list
    for product in api_products:
        try:
            product_id = product.get("id")   ## Get product ID
            if product_id is None:
                continue

            #   Extract required product fields
            product_mapping[product_id] = {    ## Map ID to info
                "title": product.get("title"),    ## Product title
                "category": product.get("category"),   ## Product category
                "brand": product.get("brand"),
                "rating": product.get("rating")
            }

        except (AttributeError, TypeError):
            continue

    #  Return final product mapping
    return product_mapping

create_product_mapping(fetch_all_products())   ## Test call


# Enrich sales data with API product info
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """

    import os

    #  Create output directory if it does not exist
    os.makedirs("data", exist_ok=True)

    enriched_transactions = []          ## Initialize enriched transaction list

    #  Process each transaction
    for txn in transactions:
        try:
            enriched = txn.copy()              ## Copy original transaction

            product_id = txn.get("ProductID", "")                  ## Get product ID
            #  Extract numeric product ID (e.g., P101 → 101)
            numeric_id = None
            if isinstance(product_id, str):
                numeric_part = "".join(filter(str.isdigit, product_id))    ## Extract digits
                if numeric_part:
                    numeric_id = int(numeric_part)         ## Convert to integer

            #  Enrich using product_mapping if match found
            if numeric_id in product_mapping:
                api_product = product_mapping[numeric_id]      ## Lookup product info
                enriched["API_Category"] = api_product.get("category")      ## Enrich category
                enriched["API_Brand"] = api_product.get("brand")
                enriched["API_Rating"] = api_product.get("rating")
                enriched["API_Match"] = True
            else:
                enriched["API_Category"] = None   ## No match found
                enriched["API_Brand"] = None
                enriched["API_Rating"] = None
                enriched["API_Match"] = False

            enriched_transactions.append(enriched)

        except Exception:
            continue

    #  Write enriched data to file (pipe-delimited)
    output_path = "data/enriched_sales_data.txt"

    if enriched_transactions:
        headers = enriched_transactions[0].keys()           ## Get headers from first record

        with open(output_path, "w", encoding="utf-8") as file:
            file.write("|".join(headers) + "\n")           ## Write header row

            for record in enriched_transactions:
                row = [str(record.get(h, "")) for h in headers]        ## Prepare row data
                file.write("|".join(row) + "\n")      ## Write data row

    #  Return enriched transaction list
    return enriched_transactions



#Helpers to save enriched data
def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    """

    import os

    # Ensure output directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Exit if there is no data to save
    if not enriched_transactions:
        return

    # Define header order (original + API fields)
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    #  Write data to file using pipe delimiter
    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(headers) + "\n")

        for txn in enriched_transactions:
            row = []         ## Initialize empty row list
            for header in headers:
                value = txn.get(header)

                #  Handle None values safely
                if value is None:
                    row.append("")
                else:
                    row.append(str(value))

            file.write("|".join(row) + "\n")     ## Write the row to file


