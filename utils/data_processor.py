#Calculate Total Revenue
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)

    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """
    total_revenue = 0.0        ## Initialize total revenue

    for txn in transactions:
        try:
            quantity = float(txn.get("Quantity", 0))        ## Get quantity
            unit_price = txn.get("UnitPrice", 0)

            # Remove commas from price if present (e.g., "1,916")
            if isinstance(unit_price, str):
                unit_price = unit_price.replace(",", "")      ## Clean commas

            unit_price = float(unit_price)        ## Convert to float
            total_revenue += quantity * unit_price    ## Accumulate revenue

        except (ValueError, TypeError, AttributeError):
            # Skip rows with invalid numeric data
            continue

    return round(total_revenue, 2)     ## Return rounded total revenue to 2 decimal places


#Region-Wise Sales Analysis
def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics

    Expected Output Format:
    {
        'North': {
            'total_sales': 450000.0,
            'transaction_count': 15,
            'percentage': 29.13
        },
        'South': {...},
        ...
    }

    Requirements:
    - Calculate total sales per region
    - Count transactions per region
    - Calculate percentage of total sales
    - Sort by total_sales in descending order
    """
    region_data = {}         ## Initialize storage for region data
    overall_sales = 0.0      ## Initialize overall sales

    # First pass: calculate total sales and transaction count per region
    for transaction in transactions:
        try:
            region = transaction.get("Region", "Unknown")        ## Get region
            quantity = float(transaction.get("Quantity", 0))     ## Get quantity
            unit_price = transaction.get("UnitPrice", 0)         ## Get unit price

            if isinstance(unit_price, str):
                unit_price = unit_price.replace(",", "")

            unit_price = float(unit_price)        ## Convert to float
            sale_amount = quantity * unit_price   ## Calculate sale amount

            if region not in region_data:         ## Initialize region entry
                region_data[region] = {
                    "total_sales": 0.0,
                    "transaction_count": 0
                }

            region_data[region]["total_sales"] += sale_amount       ## Update total sales
            region_data[region]["transaction_count"] += 1           ## Update transaction count
            overall_sales += sale_amount                            ## Update overall sales

        except (ValueError, TypeError):
            continue

    # Calculate percentage contribution
    for region in region_data:
        if overall_sales != 0:      ## Avoid division by zero
            region_data[region]["percentage"] = round(
                (region_data[region]["total_sales"] / overall_sales) * 100, 2     ## Calculate percentage
            )
        else:
            region_data[region]["percentage"] = 0.0        ## Set to 0 if no sales

    # Sort regions by total_sales (descending)
    sorted_region_data = dict(                          ## Sort dictionary
        sorted(
            region_data.items(),
            key=lambda item: item[1]["total_sales"],        ## Sort key
            reverse=True
        )
    )

    return sorted_region_data


#Top Selling Products
def top_selling_products(transactions, n=5): 
    """
    Finds top n products by total quantity sold

    Returns: list of tuples

    Expected Output Format:
    [
        ('Laptop', 45, 2250000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Mouse', 38, 19000.0),
        ...
    ]

    Requirements:
    - Aggregate by ProductName
    - Calculate total quantity sold
    - Calculate total revenue for each product
    - Sort by TotalQuantity descending
    - Return top n products
    """

    # Dictionary to store aggregated product data
    # Format:
    # {
    #   'Laptop': {'quantity': 10, 'revenue': 500000.0},
    #   'Mouse': {'quantity': 25, 'revenue': 12000.0}
    # }
    product_summary = {}            ## Initialize product summary

    # Looping through each transaction
    for txn in transactions:
        try:
            product_name = txn.get("ProductName", "Unknown")
            quantity = float(txn.get("Quantity", 0))        ## Convert to float
            unit_price = txn.get("UnitPrice", 0)
            # Remove commas from price (e.g., "1,916")
            if isinstance(unit_price, str):
                unit_price = unit_price.replace(",", "")     ## Clean commas

            unit_price = float(unit_price)      ## Convert to float
            revenue = quantity * unit_price     ## Calculate revenue

            # Initialize product if not already present
            if product_name not in product_summary:      ## Create new entry
                product_summary[product_name] = {
                    "quantity": 0,
                    "revenue": 0.0
                }

            # Aggregate quantity and revenue
            product_summary[product_name]["quantity"] += quantity        ## Update quantity
            product_summary[product_name]["revenue"] += revenue      ## Update revenue

        except (ValueError, TypeError):
            # Skip invalid rows
            continue

    #  Convert dictionary to list of tuples
    product_list = []                       ## Initialize product list
    for product, data in product_summary.items():
        product_list.append(
            (product, int(data["quantity"]), round(data["revenue"], 2))   ## Append tuple to list
        )

    # Sort products by total quantity sold (descending order)
    product_list.sort(key=lambda x: x[1], reverse=True)    

    # Return top n products
    return product_list[:n]

#Region-Wise Customer Analysis
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics
    """

    # Initialize storage for customer data
    customers = {}     

    # Process each transaction
    for txn in transactions:
        try:
            customer_id = txn.get("CustomerID")
            if not customer_id:
                continue

            quantity = float(txn.get("Quantity", 0))        ## Convert to float
            unit_price = txn.get("UnitPrice", 0)     ## Get unit price

            if isinstance(unit_price, str):
                unit_price = unit_price.replace(",", "")

            unit_price = float(unit_price)
            amount = quantity * unit_price
            product = txn.get("ProductName", "Unknown")

            # 3. Create customer entry if not exists
            if customer_id not in customers:      ## Create new entry
                customers[customer_id] = {
                    "total_spent": 0.0,
                    "purchase_count": 0,
                    "products_bought": set()
                }

            # Update customer data
            customers[customer_id]["total_spent"] += amount     ## Update total spent
            customers[customer_id]["purchase_count"] += 1       ## Update purchase count
            customers[customer_id]["products_bought"].add(product)    ## Add product to set

        except (ValueError, TypeError):
            continue

    # Calculate average order value
    for customer in customers.values():      ## Iterate through customers
        customer["avg_order_value"] = round(                          
            customer["total_spent"] / customer["purchase_count"], 2     ## Calculate average order value
        )
        customer["products_bought"] = list(customer["products_bought"])     ## Convert set to list

    # Sort customers by total_spent (descending)
    sorted_customers = dict(
        sorted(
            customers.items(),
            key=lambda item: item[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_customers


#Date Based Sales Trend Analysis
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date
    """

    # Initialize dictionary to store daily data
    daily_data = {}

    # Process each transaction
    for txn in transactions:
        try:
            date = txn.get("Date")    
            if not date:
                continue

            quantity = float(txn.get("Quantity", 0))        ## Convert to float
            unit_price = txn.get("UnitPrice", 0)     ## Get unit price

            if isinstance(unit_price, str):
                unit_price = unit_price.replace(",", "")

            unit_price = float(unit_price)
            revenue = quantity * unit_price
            customer_id = txn.get("CustomerID")

            #  Create date entry if not exists
            if date not in daily_data:
                daily_data[date] = {
                    "revenue": 0.0,
                    "transaction_count": 0,
                    "unique_customers": set()
                }

            # Update daily metrics
            daily_data[date]["revenue"] += revenue          ## Update revenue
            daily_data[date]["transaction_count"] += 1      ## Increment transaction count

            if customer_id:
                daily_data[date]["unique_customers"].add(customer_id)

        except (ValueError, TypeError):
            continue

    #  Finalize unique customer count
    for date in daily_data:
        daily_data[date]["unique_customers"] = len(
            daily_data[date]["unique_customers"]
        )

    # 6. Sort by date (chronological order)
    sorted_daily_data = dict(
        sorted(daily_data.items(), key=lambda x: x[0])
    )

    return sorted_daily_data

#Peak Sales Day Identification
def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)
    """

    # Initialize storage for daily revenue data
    daily_summary = {}    

    #  Process each transaction
    for txn in transactions:
        try:
            date = txn.get("Date")
            if not date:
                continue

            quantity = float(txn.get("Quantity", 0))
            unit_price = txn.get("UnitPrice", 0)

            if isinstance(unit_price, str):
                unit_price = unit_price.replace(",", "")

            unit_price = float(unit_price)
            revenue = quantity * unit_price

            # Create date entry if not exists
            if date not in daily_summary:
                daily_summary[date] = {
                    "revenue": 0.0,
                    "transaction_count": 0
                }

            #  Update daily revenue and transaction count
            daily_summary[date]["revenue"] += revenue
            daily_summary[date]["transaction_count"] += 1

        except (ValueError, TypeError):
            continue

    #  Identify peak sales day
    peak_date = None                 ## Initialize peak date
    peak_revenue = 0.0              ## Initialize peak revenue
    peak_transactions = 0           ## Initialize peak transactions

    for date, data in daily_summary.items():
        if data["revenue"] > peak_revenue:     
            peak_revenue = data["revenue"]      ## Update peak revenue
            peak_transactions = data["transaction_count"]
            peak_date = date

    return (peak_date, round(peak_revenue, 2), peak_transactions)

#Low Performing Products identification
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples
    """

    # Initialize dictionary to store product-wise data
    product_data = {}

    #  Process each transaction
    for txn in transactions:
        try:
            product = txn.get("ProductName", "Unknown")
            quantity = float(txn.get("Quantity", 0))
            unit_price = txn.get("UnitPrice", 0)
            if isinstance(unit_price, str):
                unit_price = unit_price.replace(",", "")

            unit_price = float(unit_price)      ## Convert to float
            revenue = quantity * unit_price     ## Calculate revenue

            # Create product entry if not exists
            if product not in product_data:
                product_data[product] = {
                    "total_quantity": 0,
                    "total_revenue": 0.0
                }

            # Update quantity and revenue
            product_data[product]["total_quantity"] += quantity
            product_data[product]["total_revenue"] += revenue

        except (ValueError, TypeError):
            continue

    # Filter products below threshold
    low_products = []             ## Initialize low products list
    for product, data in product_data.items():
        if data["total_quantity"] < threshold:
            low_products.append(
                (
                    product,
                    int(data["total_quantity"]),      ## Convert quantity to int
                    round(data["total_revenue"], 2)    ## Round revenue to 2 decimal places
                )
            )

    #  Sort by total quantity (ascending)
    low_products.sort(key=lambda x: x[1])

    return low_products

